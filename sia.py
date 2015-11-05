from astropy.io.votable.tree import VOTableFile, Resource, Table as TableInVo, Field
from astropy.io.votable import from_table
from astropy.table import Table
from flask import Response
import StringIO

def handleSiaRequest(request):
    #pos = request.args.get('POS')
    #size = request.args.get('SIZE')
    #formatVal = request.args.get('FORMAT')
    #meta = 'You asked for POS = {}, SIZE = {}, FORMAT = {}'.format(pos, size, formatVal)

    # Get the image database table
    db = getDb()
    meta = str(db.colnames)
    dbvotable = from_table(db)

    firstTable = dbvotable.get_first_table()
    
    # Fix the arraysize values (they were numbers instead of *)
    for f in firstTable.fields:
        if f.arraysize is not None:
            f.arraysize = "*"
            
            
    # Remove rows that don't match the query.
    
    # Set the UCDs for the columns.
    
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
