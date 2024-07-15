from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from gmd_creator_app.models import GeospatialResource
from django.contrib.auth import get_user_model


class GeospatialResourceTests(APITestCase):
    def setUp(self):
        super().setUp()

        self.user = get_user_model().objects.create(username="root")
        self.client.force_login(self.user)

    def test_upload_tif(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("upload-georesource")
        with open("gmd_creator_app/tests/test_data/recorte.tif", "rb") as fp:
            data = {"geodata_file": fp}
            response = self.client.post(url, data, format="multipart")
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GeospatialResource.objects.count(), 1)
        # self.assertEqual(GeospatialResource.objects.get().name, 'DabApps')

    def test_upload_shp(self):
        pass

    def test_upload_invalid(self):
        pass
