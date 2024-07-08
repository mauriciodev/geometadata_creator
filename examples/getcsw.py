from owslib import csw
import requests 

cswClient = csw.CatalogueServiceWeb('https://bdgex.eb.mil.br/csw')
metadataids = ['cfad8cc1-e710-4872-a139-bb6a57c4f1a1', #Porto alegre 25k
               '76482d38-c7e7-11df-b182-00270e07db9f' #brasilia 250k
               ]
outputschema = 'http://www.isotc211.org/2005/gmd'
cswClient.getrecordbyid(id=metadataids, outputschema=outputschema)

done = 0
for rec in cswClient.records:
    metadata = cswClient.records[rec]   
    
    print(metadata.identification[0].title)
    print(metadata.identifier)
    fname = f"{metadata.identifier}.xml"
    with open(fname, 'w') as f:
        f.write(metadata.xml.decode("utf-8"))
    
