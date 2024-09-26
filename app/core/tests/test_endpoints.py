from rest_framework import status
from rest_framework.test import APITestCase
from core.models import GeospatialResource
from django.contrib.auth import get_user_model


class GeospatialResourceUploadEndpointTests(APITestCase):
    fixtures = ["index_map"]
    response_data = {}
    """The upload endpoint for georesources"""

    def setUp(self):
        super().setUp()

        self.user = get_user_model().objects.create(username="root")
        self.client.force_login(self.user)

    def test_upload_endpoint_works(self):
        """
        Ensure we can upload a file.
        """
        with open("core/tests/test_data/recorte.tif", "rb") as fp:
            payload = {"geodata_file": fp}
            response = self.client.post("/geoproduct/", payload, format="multipart")

        response_data: dict = response.data  # type: ignore
        self.response_data.update(response_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GeospatialResource.objects.count(), 1)

    def test_upload_response_contains_id(self):
        """
        Ensures that the response contains the FILE ID
        """
        self.assertIn("file_id", self.response_data.keys())

    def test_upload_response_contains_product_types(self):
        """
        Ensures that the response contains the list of POSSIBLE PRODUCT TYPES
        """
        self.assertIn("product_types", self.response_data.keys())
        self.assertIsInstance(self.response_data["product_types"], list)
        # TODO: escrever mais um teste para garantir que a resposta é uma lista de product_types

    def test_upload_response_contains_file_fields(self):
        """
        Ensures that the response contains the EXTRACTED FILE FIELDS
        """
        self.assertIn("file_fields", self.response_data)
        # TODO: escrever mais um teste para garantir que a resposta é uma lista de product_types
