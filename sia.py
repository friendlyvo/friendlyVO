from astropy.io.votable.tree import VOTableFile, Resource, Table as TableInVo, Field
from astropy.io.votable import from_table
from astropy.table import Table
from spherical_geometry.polygon import SphericalPolygon
from flask import Response
import StringIO

columnUcdMap = {
    'title': 'VOX:Image_Title',
    'ra_center': 'POS_EQ_RA_MAIN',
    'dec_center': 'POS_EQ_DEC_MAIN',
    'naxes': 'VOX:Image_Naxes',
    'naxis': 'VOX:Image_Naxis',
    'scale': 'VOX:Image_Scale',
    'format': 'VOX:Image_Format',
    'image_url': 'VOX:Image_AccessReference'
}

def handleSiaRequest(posString, sizeString, formatString):
    info = 'You asked for POS = {}, SIZE = {}, FORMAT = {}'.format(posString, sizeString, formatString)
    
    ra, dec = parsePos(posString)
    size = parseSize(sizeString)
    
    if ra is None:
        return Response(status="Invalid RA from POS: " + posString)
    elif dec is None:
        return Response(status="Invalid Dec from POS: " + posString)
    elif size[0] is None:
        return Response(status="Invalid Size from SIZE: " + sizeString)
        
    queryRegion = makeQueryRegion(ra, dec, size)
 

    # Get the image database table
    db = getDb()
    
    # Remove rows that don't match the query.
    intersectedTable = findIntersectedRows(queryRegion, db)
    
    dbvotable = from_table(intersectedTable)
    
    # Get rid of the fixed size arrays
    fixArraysize(dbvotable)
    
    # Set the UCDs for the columns.
    mapUcds(dbvotable)
    

    
    # Write the VOTABLE xml to a string, then use that to create the response object with
    # content-type of xml.
    xmlStringObj = StringIO.StringIO()
    dbvotable.to_xml(xmlStringObj)
    xmlString = xmlStringObj.getvalue()
    resp = Response(xmlString, mimetype='text/xml')
    
    return resp
    #return meta

def getDb():
    # for testing:  db = Table.read('static/db/m101_r_0_HLA.csv', format='ascii.csv')
    db = Table.read('static/db/images.csv', format='ascii.csv')
    return db

def mapUcds(vot):
    firstTable = vot.get_first_table()
    
    for f in firstTable.fields:
        ucd = columnUcdMap.get(f.ID, None)
        if ucd is not None:
            f.ucd = ucd
    
    return

def fixArraysize(vot):
    firstTable = vot.get_first_table()
    
    # Fix the arraysize values (they were numbers instead of *)
    for f in firstTable.fields:
        if f.arraysize is not None:
            f.arraysize = "*"
    
    return

def parsePos(posString):
    ra = None
    dec = None
    if posString is not None:
        a = string.split(posString, ',')
        if a.length == 2:
            # Get the numeric values for ra and dec
            a = 'x'
            try:
                ra = float(a[0])
                dec = float(a[1])
            except ValueError:
                print "ra or dec is not a float"
                
    return ra, dec


def parsePos(posString):
    ra = None
    dec = None
    if posString is not None:
        a = posString.split(',')
        if len(a) == 2:
            # Get the numeric values for ra and dec
            try:
                ra = float(a[0])
                dec = float(a[1])
            except ValueError:
                print "ra or dec is not a float"
                
    return ra, dec


def parseSize(sizeString):
    size = [None, None]
    if sizeString is not None:
        a = sizeString.split(',')
        if len(a) == 2:
            # Get the 2 size parameters
            try:
                size[0] = float(a[0])
                size[1] = float(a[1])
            except ValueError:
                print "one of the size values is not a float"
                
        elif len(a) == 1:
            # Get the radius
            try:
                size[0] = float(a[0])
            except ValueError:
                print "the radius is not a float"
            
    return size

def makeQueryRegion(ra, dec, size):
    region = None
    
    if size[1] is None:
        # Then we have a radius, not a box.
        radius = size[0]
        region = SphericalPolygon.from_cone(ra, dec, radius)
    else:
        # Make a box.
        radius = None
        # Figure out this stupid shape later...
       
    return region

def findIntersectedRows(queryRegion, table):
    
    tableCopy = table.copy()
    toRemove = []
    for r in table:
        if (not intersects(queryRegion, r)):
            toRemove.append(r.index)
    
    tableCopy.remove_rows(toRemove)
    
    return tableCopy
    
def intersects(region, imageRow):
    result = False
    imageRegion = getRegionForImageRow(imageRow)
    if imageRegion is not None:
        result = region.intersects_poly(imageRegion)
    return result
    
def getRegionForImageRow(imageRow):
    region = getWcsRegion(imageRow)
    if (region is None):
        region = getBasicRegion(imageRow)
        
    return region

def getWcsRegion(imageRow):
    region = None
    stcs = imageRow["regionSTCS"]
    if (stcs is not None):
        a = stcs.split(' ')
        if len(a) == 10:
            ras = [float(a[2]), float(a[4]), float(a[6]), float(a[8]), float(a[2])]
            decs = [float(a[3]), float(a[5]), float(a[7]), float(a[9]), float(a[3])]
            print ras
            print decs
            region = SphericalPolygon.from_radec(ras, decs)
            
    return region

def getBasicRegion(imageRow):
    region = None
    
    return region

            
          
    
    
    
