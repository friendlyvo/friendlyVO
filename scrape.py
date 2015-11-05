from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales

def extract_image_metadata(header):
    """Return a dictionary of metadata pulled from a fits header."""
    wcs = WCS(header)
    metadata = {}
    metadata['title'] = None # required
    metadata['inst'] = None # recommended
    metadata['mjd_obs'] = None # recommended
    metadata['naxes'] = wcs.naxis
    metadata['naxis'] = (header['NAXIS1'], header['NAXIS2'])
    metadata['scale'] = proj_plane_pixel_scales(wcs)
    metadata['format'] = 'image/fits'
    metadata['crpix'] = wcs.wcs.crpix
    metadata['crval'] = wcs.wcs.crval
    metadata['cd'] = wcs.wcs.cd
    metadata['ref_frame'] = wcs.wcs.radesys
    metadata['equinox'] = wcs.wcs.equinox
    # There must surely be a tidier way of doing the next few lines
    centre = 0.5*(metadata['naxis'][0] - 1), 0.5*(metadata['naxis'][1] - 1)
    centre_wcs = wcs.wcs_pix2world([centre[0]], [centre[1]], 0)
    metadata['ra_cen'] = centre_wcs[0][0]
    metadata['dec_cen'] = centre_wcs[1][0]
    return metadata
