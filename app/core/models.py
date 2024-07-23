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
