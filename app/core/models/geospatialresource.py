import uuid
from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
from owslib import csw


class GeospatialResource(models.Model):
    """
    Stores the geoproduct(geodata_file), the metadata (metadata_file) and the pdf
    """

    id = models.BigAutoField(primary_key=True)
    metadata_id = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=True)
    metadata_file = models.FileField(
        "Geospatial metadata XML.", null=True, blank=True, upload_to="repository"
    )  # adicionar extrair uuid do metadata_file
    geodata_file = models.FileField(
        "Geospatial data file.", null=True, blank=True, upload_to="repository"
    )
    pdf_file = models.FileField(
        "PDF file for printing.", null=True, blank=True, upload_to="repository"
    )
    published_on_csw = models.BooleanField(default=False)
    history = HistoricalRecords()

    def csw_insert(self):  # publish
        csw_url = "http://localhost:8088/csw"
        cswClient = csw.CatalogueServiceWeb(csw_url)

        fname = str(self.metadata_file)
        f = open(fname)
        try:
            cswClient.transaction(
                ttype="insert",
                typename="gmd:MD_Metadata",
                record=f.read().encode("utf-8"),
            )
            return "Done."
        except:
            return "Error saving metadata."

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
