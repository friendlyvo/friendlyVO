from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales

from utils import ImageMetadata

def extract_image_metadata(header, title=None, image_url=None):
    """Return a dictionary of metadata pulled from a fits header."""
    wcs = WCS(header)
    center = 0.5*(header['NAXIS1'] - 1), 0.5*(header['NAXIS2'] - 1)
    center_wcs = wcs.wcs_pix2world([center[0]], [center[1]], 0)
    metadata = ImageMetadata(
        title=title,
        ra_center=center_wcs[0][0],
        dec_center=center_wcs[1][0],
        naxes=wcs.naxis,
        naxis='[{} {}]'.format(header['NAXIS1'], header['NAXIS2']),
        scale='[{} {}]'.format(*proj_plane_pixel_scales(wcs)),
        format='image/fits',
        image_url=image_url,
        crpix='[{} {}]'.format(*wcs.wcs.crpix),
        crval='[{} {}]'.format(*wcs.wcs.crval),
        cd_matrix='[{} {} {} {}]'.format(
            wcs.wcs.cd[0, 0], wcs.wcs.cd[0, 1],
            wcs.wcs.cd[1, 0], wcs.wcs.cd[1, 1]),
        reference_frame=wcs.wcs.radesys,
        )
    # metadata['inst'] = None # recommended
    # metadata['mjd_obs'] = None # recommended
    # metadata['equinox'] = wcs.wcs.equinox
    return metadata
