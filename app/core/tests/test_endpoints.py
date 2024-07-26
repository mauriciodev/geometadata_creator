from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import GeospatialResource
from django.contrib.auth import get_user_model


class GeospatialResourceTests(APITestCase):
    fixtures = ["index_map"]
    def setUp(self):
        super().setUp()

        self.user = get_user_model().objects.create(username="root")
        self.client.force_login(self.user)

    def test_upload_tif(self):
        """
        Ensure we can upload a file.
        """
        url = reverse("upload-georesource")
        with open("core/tests/test_data/recorte.tif", "rb") as fp:
            data = {"geodata_file": fp}
            response = self.client.post(url, data, format="multipart")
            #print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GeospatialResource.objects.count(), 1)
        # self.assertEqual(GeospatialResource.objects.get().name, 'DabApps')

    def test_upload_shp(self):
        "Not implemented: Ensure that we can upload vector files."
        pass

    def test_upload_invalid(self):
        "Not implemented: ensure that the upload is a valid file."
        pass
