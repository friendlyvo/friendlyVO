from flask import Blueprint, request
from sia import handleSiaRequest

query = Blueprint('query', __name__)

@query.route('/sia')
def sia():
    resp = handleSiaRequest(request)
    return resp
