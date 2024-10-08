from rest_framework import status
from rest_framework.test import APITestCase
from file_handler.extractor import parse_file
from file_handler.schemas import FileExtractedFields
from core.models.producttype import ProductType
from core.models import GeospatialResource
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from core.views.georesouce_upload_views import ErrorMessages as EM
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

    def test_file_not_found_returns_404(self):
        """Assert that if the file is not found it will return a 404 error"""
        url = f"/geoproduct/{self.obj.id + 1}/build_metadata/"
        payload = {"metadata_fields": [], "product_type": self.product_type_id}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

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

    def test_validation_for_field_values(self):
        """
        Assert that sending values that are the wrong type (str) will be flagged
        """
        url = f"/geoproduct/{self.obj.id}/build_metadata/"
        payload = {
            "metadata_fields": [
                {"label": field.iso_xml_path, "value": "test"}
                for field in ProductType.objects.get(
                    pk=self.product_type_id
                ).metadata_fields.all()
            ],
            "product_type": self.product_type_id,
        }
        response = self.client.post(url, payload, format="json")
        response_data = response.data  # type: ignore

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.json()
        )
        self.assertEqual(response_data["error"], EM.missmatched_file_fields.value)
        self.assertIn(EM.missmatched_file_fields.name, response_data)

    def test_incorrect_file_values(self):
        """
        Assert that sending values that are incorrect if matched against the file will be flagged.
        """
        url = f"/geoproduct/{self.obj.id}/build_metadata/"
        wrong_fields = FileExtractedFields(
            north_bound_lat=1.0,
            west_bound_lon=1.0,
            east_bound_lon=1.0,
            south_bound_lat=1.0,
            epsg_code=2343,
            driver="Not IT",
            scale_denominator1=1,
            scale_denominator2=1,
            inom="not_it",
            mi="not_it",
            data_representation_type="Vetorial",
        ).dump_fields()
        middle_dict = (
            field.iso_xml_path
            for field in ProductType.objects.get(
                pk=self.product_type_id
            ).metadata_fields.all()
        )
        payload = {
            "metadata_fields": [
                {"label": label, "value": wrong_fields.get(label, "123")}
                for label in middle_dict
            ],
            "product_type": self.product_type_id,
        }
        response = self.client.post(url, payload, format="json")
        response_data = response.data  # type: ignore

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.json()
        )
        self.assertIn("error", response_data, msg=response_data)
        self.assertEqual(response_data["error"], EM.missmatched_file_fields.value)
        self.assertIn(EM.missmatched_file_fields.name, response_data)

    def test_the_creates_the_file(self):
        """
        Ensure we can upload a file.
        """
        url = f"/geoproduct/{self.obj.id}/build_metadata/"

        wrong_fields = parse_file(self.obj.geodata_file.path).dump_fields()
        middle_dict = (
            field.iso_xml_path
            for field in ProductType.objects.get(
                pk=self.product_type_id
            ).metadata_fields.all()
        )
        payload = {
            "metadata_fields": [
                {"label": label, "value": wrong_fields.get(label, "123")}
                for label in middle_dict
            ],
            "product_type": self.product_type_id,
        }
        response = self.client.post(url, payload, format="json")
        self.obj.refresh_from_db()

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.json()
        )
        self.assertTrue(len(self.obj.metadata_file) > 0)
