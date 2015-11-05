from flask import Blueprint, request
import json

ingest = Blueprint('ingest', __name__)

def success_tpl(message=''):
    return {'status': 'success', 'message': message}

def error_tpl(message=''):
    return {'status': 'error', 'message': message}

COMPULSORY_KEYS = ('title', 'ra_center', 'dec_center', 'naxes', 'naxis', 'scale', 'format', 'image_url')

@ingest.route('/ingest', methods=['GET', 'POST'])
def lets_ingest():
    if request.method != 'POST':
        s = 'Submit a <b>POST request</b> to ingest image metadata.<br/>'
        s += 'Example:<code>curl ...</code>'

        return s

    try:
        metadata_new_img = json.loads(request.data)
    except:
        return json.dumps(error_tpl(message='POSTed data does not look like JSON'))

    # convert keys to lowercase
    metadata_new_img = dict((k.lower(), v) for k,v in metadata_new_img.iteritems())
    m = metadata_new_img

    # check if we have compulsory keys
    for key in COMPULSORY_KEYS:
        if key not in m:
            return json.dumps(error_tpl(message='Key %s missing' % (key)))

    #return success_tpl(message='Image %s ingested!' % (m['image_url']))
    return 'HELLO'


