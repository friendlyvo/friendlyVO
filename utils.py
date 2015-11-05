
class ImageMetadata:

    COMPULSORY_KEYS = ('title', 'ra_center', 'dec_center', 'naxes', 'naxis', 'scale', 'format', 'image_url')
    
    COMPULSORY_KEYS_TYPES = ('S500', float, float, int, 'S500', float, 'S500', 'S500')

    OTHER_KEYS = ('instrument', 'description', 'mjd', 'reference_frame', 'projection', 'crpix', 'crval', 'cd_matrix', 'preview_url', 'fov_s', 'pub_ref', 'author')
    OTHER_KEYS_TYPES = ('S500', 'S500', 'S500', 'S500', 'S500', 'S500', 'S500', 'S500', 'S500', 'S500', 'S500', 'S500')

    def __init__(self, title=None, ra_center=None, dec_center=None, naxes=None, naxis=None, scale=None, format=None, image_url=None, instrument=None, description=None, mjd=None, reference_frame=None, projection=None, crpix=None, crval=None, cd_matrix=None, preview_url=None, fov_s=None, pub_ref=None, author=None):
        self.title = title
        self.ra_center = ra_center
        self.dec_center = dec_center
        self.naxes = naxes
        self.naxis = naxis
        self.scale = scale
        self.format = format
        self.image_url = image_url

        self.instrument = instrument
        self.description = description
        self.mjd = mjd
        self.reference_frame = reference_frame
        self.projection = projection
        self.crpix = crpix
        self.crval = crval
        self.cd_matrix = cd_matrix
        self.preview_url = preview_url
        self.fov_s = fov_s
        self.pub_ref = pub_ref
        self.author = author

    @classmethod
    def from_dict(cls, metadata_dict):
        """
        Create an ImageMetadata instance from a dictionary
        raise an Exception
        """
        # convert keys to lowercase
        m = metadata_dict
        m = dict((k.lower(), v) for k,v in m.iteritems())

        # check if we have compulsory keys
        for key in ImageMetadata.COMPULSORY_KEYS:
            if key not in m:
                raise Exception('Key %s missing' % (key))

        return ImageMetadata(title=m['title'], ra_center=m['ra_center'], dec_center=m['dec_center'], naxes=m['naxes'], naxis=m['naxis'], scale=m['scale'], format=m['format'], image_url=m['image_url'], instrument=m.get('instrument', None), description=m.get('description', None), mjd=m.get('mjd', None), reference_frame=m.get('reference_frame', None), projection=m.get('projection', None), crpix=m.get('crpix', None), crval=m.get('crval', None), cd_matrix=m.get('cd_matrix', None), preview_url=m.get('preview_url', None), fov_s=m.get('fov_s', None), pub_ref=m.get('pub_ref', None), author=m.get('author', None))

    def as_array(self):
        return [self.title, self.ra_center, self.dec_center, self.naxes, str(self.naxis), self.scale, self.format, self.image_url, self.instrument, self.description, self.mjd, self.reference_frame, self.projection, str(self.crpix), str(self.crval), str(self.cd_matrix), self.preview_url, self.fov_s, self.pub_ref, self.author]

