import os
from flask import Flask, request

from .query import query

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World! I can deploy automatically :)'

app.register_blueprint(query)
