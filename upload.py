import contextlib

from flask import Blueprint, render_template, flash
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

import requests
from astropy.io import fits

from scrape import extract_image_metadata
from db import add_image

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
                header = get_remote_header(url)
            except requests.exceptions.MissingSchema:
                continue
            if not header:
                continue
            metadata = extract_image_metadata(header, image_url=url)
            add_image(metadata)
            result_list.append(metadata)
        return 'Successfully found this data:<br/>' + '<br/>'.join(
            ['RA: {} Dec: {} url: {}'.format(
                meta.ra_center, meta.dec_center, meta.image_url)
             for meta in result_list])
        # return redirect('/index')
    return render_template('new.html', title='Add new data', form=form)

def get_remote_header(url):
    with contextlib.closing(requests.get(url, stream=True)) as response:
        if response.status_code != 200:
            print 'Bad status code: {}'.format(response.status_code)
            return None
        header_str = ''
        buff = ''
        end = False
        for chunk in response.iter_content(chunk_size=80):
            if len(header_str) > 80000:
                print 'Reached 1000 lines!!!'
                return None
            buff = buff + chunk
            while len(buff) >= 80:
                line, buff = buff[:80], buff[80:]
                header_str = header_str + line
                if line == 'END' + ' '*77:
                    end = True
                    break
            if end:
                break
    header = fits.Header.fromstring(header_str)
    return header
