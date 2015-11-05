import os
from flask import Flask, request
from flask import render_template

from query import query
from ingest import ingest
from upload import upload

app = Flask(__name__)
app.debug = True
app.config.from_object('config')

@app.route('/')
def hello():
    return 'Hello World! I can deploy automatically :)'

@app.route('/test')
def test():
    page_title = 'the Friendly VO'
    page_content = 'Yo, I got the stuff working.'
    return render_template('index.html', 
			   title = 'test page',
 			   page_content = page_content)

app.register_blueprint(query, url_prefix='/query')

app.register_blueprint(ingest, url_prefix='/images')

app.register_blueprint(upload, url_prefix='/upload')
