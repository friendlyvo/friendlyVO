
class ImageMetadata:

    COMPULSORY_KEYS = ('title', 'ra_center', 'dec_center', 'naxes', 'naxis', 'scale', 'format', 'image_url')
    #COMPULSORY_KEYS_TYPES = ('a', 'ra_center', 'dec_center', 'naxes', 'naxis', 'scale', 'format', 'image_url')

    def __init__(self, title=None, ra_center=None, dec_center=None, naxes=None, naxis=None, scale=None, format=None, image_url=None):
        self.title = title
        self.ra_center = ra_center
        self.dec_center = dec_center
        self.naxes = naxes
        self.naxis = naxis
        self.scale = scale
        self.format = format
        self.image_url = image_url

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

        return ImageMetadata(title=m['title'], ra_center=m['ra_center'], dec_center=m['dec_center'], naxes=m['naxes'], naxis=m['naxis'], scale=m['scale'], format=m['format'], image_url=m['image_url'])

    def as_array(self):
        return [self.title, self.ra_center, self.dec_center, self.naxes, self.naxis, self.scale, self.format, self.image_url]

