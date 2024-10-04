from rest_framework import status
from rest_framework.test import APITestCase
from core.models import GeospatialResource
from django.contrib.auth import get_user_model
from django.core.files.base import File


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

    def test_the_endpoint_works(self):
        """
        Ensure we can upload a file.
        """
        with open("core/tests/test_data/recorte.tif", "rb") as fp:
            obj = GeospatialResource.objects.create(geodata_file=File(fp))
        url = f"/geoproduct/{obj.id}/build_metadata/"
        payload = {"metadata_fields": [], "product_type": 1}
        response = self.client.post(url, payload, format="json")
        obj.refresh_from_db()

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.json()
        )
        self.assertTrue(len(obj.metadata_file) > 0)
