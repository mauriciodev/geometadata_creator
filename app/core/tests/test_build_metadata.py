from rest_framework import status
from rest_framework.test import APITestCase
from core.models import GeospatialResource
from django.contrib.auth import get_user_model
from django.core.files.base import File
from core.views.georesouce_upload_views import ErrorMessages as EM


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
        with open("core/tests/test_data/recorte.tif", "rb") as fp:
            self.obj = GeospatialResource.objects.create(geodata_file=File(fp))
        self.product_type_id = 1

    def test_missing_fields(self):
        """
        Assert that an error and a list of missing fields is recived after sending an empty fields list.
        """
        url = f"/geoproduct/{self.obj.id}/build_metadata/"
        payload = {"metadata_fields": [], "product_type": self.product_type_id}
        response = self.client.post(url, payload, format="json")
        response_data = response.data  # type: ignore

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.json()
        )
        self.assertEqual(response_data["error"], EM.missing_fields.value)
        self.assertIn(EM.missing_fields.name, response_data)

    def test_the_creates_the_file(self):
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
