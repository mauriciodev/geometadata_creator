from owslib.iso import MD_Metadata
from owslib.etree import etree
import xmlschema



xml_filename = '/home/mauricio/Desktop/Doutorado_psq/PFC_2024/geometadata_creator/examples/cfad8cc1-e710-4872-a139-bb6a57c4f1a1.xml'



#validating against ISO
iso19115_schema = xmlschema.XMLSchema('http://www.isotc211.org/2005/gmd/gmd.xsd')
iso19115_schema.validate(xml_filename)
iso19115_schema.all_errors


#reading xml with owslib
with open(xml_filename, 'r') as f:
    s = f.read()
    xml = etree.fromstring(s)
    md = MD_Metadata(xml)
    #do something