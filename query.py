from flask import Blueprint, request
from sia import handleSiaRequest

query = Blueprint('query', __name__)

@query.route('/sia')
def sia():
    
    
    posString = request.args.get('POS')
    if posString is None:
        posString = ""
    sizeString = request.args.get('SIZE')
    if sizeString is None:
        sizeString = ""
    formatString = request.args.get('FORMAT')
    
    print "pos = {}, size = {}, format = {}".format(posString, sizeString, formatString)
    resp = handleSiaRequest(posString, sizeString, formatString)
    
    return resp
