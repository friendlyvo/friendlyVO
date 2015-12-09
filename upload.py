import contextlib

from flask import Blueprint, render_template, flash
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

import requests
from astropy.io import fits
import numpy as np

from scrape import extract_image_metadata, ScrapeException
from db import add_image

FITS_BLOCK = 2880  # Number of bytes in each FITS block
FITS_HEADER_LINE = 80  # Number of bytes in each FITS header line

upload = Blueprint('upload', __name__)

class NewForm(Form):
    user_name = StringField('user_name', validators=[DataRequired()])
    dataset_name = StringField('dataset_name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    url_list = TextAreaField('url_list', validators=[DataRequired()])

@upload.route('/new', methods=['GET', 'POST'])
def new():
    form = NewForm()
    if form.validate_on_submit():
        url_list = form.url_list.data.replace('\r', '').split('\n')
        # Strip \r and the last empty item. Terrible coding here.
        # url_list = [url[:-1] for url in url_list[:-1]]
        result_list = []
        for url in url_list:
            try:
                metadata = get_remote_metadata(url)
            except requests.exceptions.MissingSchema:
                # Malformed URL given
                continue
            if metadata is None:
                # No valid metadata found in the file
                continue
            add_image(metadata)
            result_list.append(metadata)
        return 'Successfully found this data:<br/>' + '<br/>'.join(
            ['RA: {} Dec: {} url: {}'.format(
                meta.ra_center, meta.dec_center, meta.image_url)
             for meta in result_list])
        # return redirect('/index')
    return render_template('new.html', title='Add new data', form=form)

def get_remote_metadata(url):
    """Return WCS information from the FITS file at the URL."""
    if check_for_partial(url):
        header_iter = get_remote_headers(url, trust_partial=True)
    else:
        # Server doesn't support partial ranges, so we can only get the
        # primary header
        header_iter = [get_first_header(url)]
    for idx, header in enumerate(header_iter):
        if idx > 0 and header.get('XTENSION', None) != 'IMAGE':
            # This is not an image HDU; continue to next header
            continue
        try:
            metadata = extract_image_metadata(header, image_url=url)
            return metadata
        except ScrapeException:
            # No WCS information found; continue to next header
            continue

def get_first_header(url, limit=1000*FITS_HEADER_LINE):
    """Return the first header from the FITS file at the URL."""
    with contextlib.closing(requests.get(url, stream=True)) as response:
        if response.status_code != requests.codes.OK:
            raise UploadException(
                'Unexpected status code: {}'.format(response.status_code))
        header_str = ''
        buff = ''
        end = False
        for chunk in response.iter_content(chunk_size=FITS_BLOCK):
            buff = buff + chunk
            while len(buff) >= FITS_HEADER_LINE:
                line, buff = buff[:FITS_HEADER_LINE], buff[FITS_HEADER_LINE:]
                header_str = header_str + line
                if line == 'END' + ' '*77:
                    end = True
                    break
            if end:
                break
            if len(header_str) >= limit:
                raise UploadException('No end to the header found')
    header = fits.Header.fromstring(header_str)
    return header

def get_remote_headers(url, trust_partial=False):
    """Yield successive headers from the FITS file at the URL."""
    start = 0
    if not trust_partial and not check_for_partial(url):
        raise UploadException('Server does not support partial ranges')
    while True:
        try:
            header_str = get_remote_header_str(url, start)
        except UploadException as exception:
            if exception.message.endswith('416'):
                # Requested a bytes range beyond the file end
                raise StopIteration()
            # Some other, unexpected error
            raise
        start += len(header_str)
        header = fits.Header.fromstring(header_str)
        start += data_length_bytes(header)
        yield header

def get_remote_header_str(url, start=0, limit=1000*FITS_HEADER_LINE):
    """
    Get a FITS header as a string from the given URL.

    If specified, `start` is an offset within the file, in bytes.
    No more than `limit` bytes will be read.
    """
    header_str = ''
    for i_block, block in enumerate(get_remote_blocks(url, start)):
        header_str += block
        for idx in xrange(FITS_BLOCK / FITS_HEADER_LINE):
            line = block[idx*FITS_HEADER_LINE:(idx+1)*FITS_HEADER_LINE]
            if line == 'END' + ' '*77:
                return header_str
        if (i_block + 1) * FITS_BLOCK >= limit:
            raise UploadException('No end to the header found')

def get_remote_blocks(url, start=0, chunk_size=10):
    """
    Yield FITS blocks from a given URL.

    If specified, `start` is an offset within the file, in bytes.
    `chunk_size` specifies how many blocks to download at a time.
    """
    data = ''
    chunk_data_size = chunk_size*FITS_BLOCK
    while True:
        if not data:
            data = get_remote_bytes(url, start, start+chunk_data_size-1)
            start += chunk_data_size
        next_block, data = data[:FITS_BLOCK], data[FITS_BLOCK:]
        yield next_block

def get_remote_bytes(url, start=0, finish=None):
    """Get the specified range of bytes from a given URL."""
    # Format the range for the HTTP GET headers
    start_str = str(start)
    finish_str = '' if finish is None else str(finish)
    headers = {'Range': 'bytes={}-{}'.format(start_str, finish_str)}
    # Get the data
    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.PARTIAL_CONTENT:
        raise UploadException(
            'Unexpected status code: {}'.format(response.status_code))
    return response.content

def check_for_partial(url):
    """Return True if the server supports partial ranges"""
    headers = {'Range': 'bytes=0-1'}
    check = requests.head(url, headers=headers)
    return check.status_code == requests.codes.PARTIAL_CONTENT

def data_length_bytes(header, round_block=True):
    """
    Return number of bytes of data associated with the header.

    If `round_block` is True, round up to the next complete FITS block.
    """
    naxis = header['NAXIS']
    if naxis == 0:
        return 0
    naxis_list = [header['NAXIS{}'.format(i+1)] for i in xrange(naxis)]
    bitpix = header['BITPIX']
    gcount = header.get('GCOUNT', 1)
    pcount = header.get('PCOUNT', 0)
    n_bytes = abs(bitpix) * gcount * (pcount + np.product(naxis_list)) / 8
    if round_block:
        blocks, extra = divmod(n_bytes, FITS_BLOCK)
        if extra:
            blocks += 1
        n_bytes = FITS_BLOCK * blocks
    return n_bytes



class UploadException(Exception):
    pass


