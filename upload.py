from StringIO import StringIO

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
        url_list = form.url_list.data.split('\n')
        for url in url_list:
            response = requests.get(url)
            if response.status_code != 200:
                continue
            header = fits.getheader(StringIO(response.content))
            metadata = extract_image_metadata(header, image_url=url)
            add_image(metadata)
        return 'Tried to upload these URLs:<br/>' + '<br/>'.join(url_list)
        # return redirect('/index')
    return render_template('new.html', title='Add new data', form=form)
