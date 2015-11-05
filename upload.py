from flask import Blueprint, render_template, flash
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

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
        return 'Tried to upload these URLs:<br/>' + '<br/>'.join(url_list)
        # return redirect('/index')
    return render_template('new.html', title='Add new data', form=form)
