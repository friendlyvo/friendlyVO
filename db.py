"""
Minimal interface for our database (currently backed up by a CSV file)
"""

import os
import fcntl

from utils import ImageMetadata
from astropy.table import Table
from astropy.io import ascii

CSV_PATH = 'static/db/images.csv'

def add_image(img_metadata):
    """
    add an image description to our database
    img_metadata in an instance of ImageMetadata class
    """

    try:
        if not os.path.exists(CSV_PATH):
            table = Table(dtype=ImageMetadata.COMPULSORY_KEYS_TYPES + ImageMetadata.OTHER_KEYS_TYPES, names=ImageMetadata.COMPULSORY_KEYS + ImageMetadata.OTHER_KEYS)
        else:
            table = ascii.read(CSV_PATH, format='csv')

        table.add_row(img_metadata.as_array())

        table.write(CSV_PATH, format='csv')

    finally:
        pass
        # unlock file
        #fcntl.lockf(h, fcntl.LOCK_UN)
        #h.close()


    
    
    
