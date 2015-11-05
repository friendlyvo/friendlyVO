from astropy.io.votable.tree import VOTableFile, Resource, Table as TableInVo, Field
from astropy.io.votable import from_table
from astropy.table import Table
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

def handleSiaRequest(request):
    #pos = request.args.get('POS')
    #size = request.args.get('SIZE')
    #formatVal = request.args.get('FORMAT')
    #meta = 'You asked for POS = {}, SIZE = {}, FORMAT = {}'.format(pos, size, formatVal)

    # Get the image database table
    db = getDb()
    meta = str(db.colnames)
    dbvotable = from_table(db)
    
    # Get rid of the fixed size arrays
    fixArraysize(dbvotable)
    
    # Set the UCDs for the columns.
    mapUcds(dbvotable)

  
    # Remove rows that don't match the query.
    

    
    # Write the VOTABLE xml to a string, then use that to create the response object with
    # content-type of xml.
    xmlStringObj = StringIO.StringIO()
    dbvotable.to_xml(xmlStringObj)
    xmlString = xmlStringObj.getvalue()
    resp = Response(xmlString, mimetype='text/xml')
    
    return resp
    #return meta

def getDb():
    #db = ascii.read("static/db/m101_r_0_HLA.csv", format='Csv')
    db = Table.read('static/db/m101_r_0_HLA.csv', format='ascii.csv')
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
            
          
    
    
    
