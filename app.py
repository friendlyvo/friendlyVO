import os
from flask import Flask, request, Markup
from flask import render_template

from query import query
from ingest import ingest
from upload import upload

app = Flask(__name__)
app.debug = True
app.config.from_object('config')

@app.route('/')
def hello():
    return render_template('index.html',
                           page_content = page_stuff())
def page_stuff():
    return Markup(render_template('frontpage.html'))

app.register_blueprint(query, url_prefix='/query')

app.register_blueprint(ingest, url_prefix='/images')

app.register_blueprint(upload, url_prefix='/upload')
