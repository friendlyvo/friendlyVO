from flask import Blueprint, request
import json

from utils import ImageMetadata
import db

ingest = Blueprint('ingest', __name__)

def success_tpl(message=''):
    return {'status': 'success', 'message': message}

def error_tpl(message=''):
    return {'status': 'error', 'message': message}


@ingest.route('/ingest', methods=['GET', 'POST'])
def lets_ingest():
    if request.method != 'POST':
        s = 'Submit a <b>POST request</b> to ingest image metadata.<br/>'
        s += 'Example:<code>curl ...</code>'

        return s

    try:
        metadata_dict = json.loads(request.data)
    except:
        return json.dumps(error_tpl(message='POSTed data does not look like JSON'))

    try:
        img_metadata = ImageMetadata.from_dict(metadata_dict)
    except:
        return json.dumps(error_tpl(message='A key is missing'))

    db.add_image(img_metadata)
    return json.dumps(success_tpl(message='Image %s ingested!' % (img_metadata.image_url)))
