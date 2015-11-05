from flask import Blueprint, request

query = Blueprint('query', __name__)

@query.route('/sia')
def sia():
    ra = request.args.get('RA')
    dec = request.args.get('Dec')
    size = request.args.get('Size')
    return 'You asked for RA = {}, Dec = {}, Size = {}'.format(ra, dec, size)
