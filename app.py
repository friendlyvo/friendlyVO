import os
from flask import Flask, request
from flask import render_template

from query import query
from ingest import ingest

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World! I can deploy automatically :)'

@app.route('/test')
def test():
    page_title = 'the Friendly VO'
    page_content = 'Yo, I got the stuff working.'
    return render_template('index.html', 
			   title = 'test page',
			   page_title = page_title,
 			   page_content = page_content)

app.register_blueprint(query, url_prefix='/query')

app.register_blueprint(ingest, url_prefix='/images')
