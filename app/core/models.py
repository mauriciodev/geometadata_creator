import uuid
from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
from owslib import csw, iso


class GeospatialResource(models.Model):
    metadata_id = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=True)
    metadata_file = models.FileField(
        "Geospatial metadata XML.", null=True, blank=True, upload_to="repository"
    )
    geodata_file = models.FileField(
        "Geospatial data file.", null=True, blank=True, upload_to="repository"
    )
    pdf_file = models.FileField(
        "PDF file for printing.", null=True, blank=True, upload_to="repository"
    )
    published_on_csw = models.BooleanField(default=False)
    history = HistoricalRecords()

    def csw_insert(self):  # publish
        pass

    def csw_get(self, metadataid, csw_url=""):
        if csw_url == "":
            csw_url = settings.CSW_SERVER_URL

    def get_metadata_as_object(self):
        pass

    def set_metadata_from_object(self):
        pass

    def csw_delete(self):
        pass

    def fill_metadata_with_geodata(self):
        pass

    def check_metadata_xml(self):
        pass

    def import_geo_data(self):
        pass


class ProductType(models.Model):
    name = models.CharField(max_length=100, blank=True)
    metadata_fields = models.ManyToManyField("MetadataFormField")

    def __str__(self):
        return self.name


class MetadataFormField(models.Model):
    label = models.CharField(max_length=100, blank=True)
    iso_xml_path = models.CharField(max_length=200, blank=True)
    field_types = {
        "list": "list",
        "combobox": "combobox",
        "date": "date",
        "text": "text",
    }
    field_type = models.CharField(max_length=100, choices=field_types)
    is_static = models.BooleanField(default=False)
    possible_values = models.TextField()
    default_value = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)
    old_path = models.TextField(blank=True)

    def __str__(self):
        return f"{self.label}: {self.iso_xml_path}"

#class that implements table behavior to IndexMap.objects
class IndexMapManager(models.Manager):
    def get_mi(self,inomen:str): 
        parts = inomen.split('-')
        sufix=''
        
        if len(parts) > 4: #1000000
            scale_denominator=100000
            if len(parts)>5: #50k or more
                sufix = '-'+'-'.join(parts[5:])
                inomen= '-'.join(parts[:5])
        elif len(parts) == 4:
            scale_denominator=250000
        else: 
            return ''
        rows = IndexMap.objects.filter(scale_denominator=scale_denominator, inomen=inomen)

        if len(rows)>0:
            return f"{rows[0].mi}{sufix}"
        return ''
    def get_inomen_by_mi(self, mi:str, is_mir=False):
        parts = mi.split('-')
        sufix=''
        
        if is_mir: 
            scale_denominator=250000
        else:
            scale_denominator=100000

        if len(parts) > 1: #50k or more
            sufix = '-'+'-'.join(parts[1:])

        rows = IndexMap.objects.filter(scale_denominator=scale_denominator, mi=parts[0])

        if len(rows)>0:
            return f"{rows[0].inomen}{sufix}"
        return ''

class IndexMap(models.Model):
    scale_denominator = models.IntegerField()
    mi = models.CharField(max_length=10)
    inomen = models.CharField(max_length=20)
    objects = IndexMapManager()
    def __str__(self):
        return f"{self.mi} - {self.inomen} ({self.scale_denominator})"
