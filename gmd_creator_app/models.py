from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
from owslib import csw

class geospatial_resource(models.Model):
    metadata_id = models.UUIDField()
    title = models.CharField(max_length=200, blank=True)
    metadata_file = models.FileField('Geospatial metadata XML.')
    geodata_file = models.FileField('Geospatial data file.', null=True, blank=True)
    pdf_file = models.FileField('PDF file for printing.', null=True, blank=True)
    published_on_csw = models.BooleanField(default=True)
    history = HistoricalRecords()

    def csw_insert(self): #publish
        pass

    def csw_get(self):
        settings.CSW_SERVER_URL
        pass
    
    def csw_delete(self):
        pass

    def fill_metadata_with_geodata(self):
        pass

    def check_metadata_xml(self):
        pass

    

