from rest_framework.test import APITestCase
from core.models import GeospatialResource
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from file_handler.utils import get_example_raster


class GeospatialResourceUploadEndpointTests(APITestCase):
    fixtures = [
        "index_map",
        "metadata_fields",
        "product_types",
    ]
    """The upload endpoint for georesources"""

    def setUp(self):
        super().setUp()

        self.user = get_user_model().objects.create(username="root")
        self.client.force_login(self.user)
        binary_data, fields = get_example_raster()
        self.obj = GeospatialResource.objects.create(
            geodata_file=ContentFile(binary_data, "name.tif")
        )
        self.file_fields = fields
        self.obj.refresh_from_db()
        self.product_type_id = 1

    def tearDown(self):
        self.obj.delete()
        return super().tearDown()
