import os

from django.urls import reverse
from django.test import TestCase

from core.models import IndexMap


class IndexMapTests(TestCase):
    fixtures = ["index_map"]

    def setUp(self):
        super().setUp()

    def test_loaded_fixture(self):
        """Ensure fixtures for IndexMap are being loaded."""
        self.assertGreater(IndexMap.objects.count(), 3000)

    def test_inomen_to_mi(self):
        """Ensure that MI is being computed correctly from INOM."""
        self.assertEqual(IndexMap.objects.get_mi("SC-22-Y-C"), "321")  # MIR 250k
        self.assertEqual(IndexMap.objects.get_mi("SC-22-Y-C-I"), "1761")  # MI 100k
        self.assertEqual(
            IndexMap.objects.get_mi("SD-21-X-B-III-2-NO"), "1873-2-NO"
        )  # MI 25k

    def test_mi_to_inomen(self):
        """Ensure that INOM is being computed correctly from MI."""
        self.assertEqual(
            IndexMap.objects.get_inomen_by_mi("321", is_mir=True), "SC-22-Y-C"
        )  # MIR 250k
        self.assertEqual(
            IndexMap.objects.get_inomen_by_mi("1761"), "SC-22-Y-C-I"
        )  # MI 100k
        self.assertEqual(
            IndexMap.objects.get_inomen_by_mi("1873-2-NO"), "SD-21-X-B-III-2-NO"
        )  # MI 25k

    def test_inomen_from_file(self):
        """Ensure that MI and INOM are being computed correctly from a raster file."""
        filename = "core/tests/test_data/recorte.tif"
        self.assertTrue(os.path.exists(filename))
        # Não sistemático
        self.assertEqual(
            IndexMap.objects.get_inomen_mi_from_rasterio(filename), ("", "")
        )

    def test_inomen_to_extent(self):
        """Ensure extent is being computed correctly from INomen."""
        grid_utm = IndexMap.objects.get_grid_utm()
        self.assertEqual(
            grid_utm.extentFromInomen("SF-23-Y-B-I-1-SE"),
            (-46.375, -22.250, -46.250, -22.125),
        )
        self.assertEqual(
            grid_utm.extentFromInomen("SF-23-A-B-I-1-SE"), (-48, -22, -45, -20)
        )

    def test_extent_to_inomen(self):
        """Ensure INomen is being computed correctly from extent."""
        grid_utm = IndexMap.objects.get_grid_utm()
        self.assertEqual(
            grid_utm.inomenFromExtent(-46.375, -22.250, -46.250, -22.125),
            "SF-23-Y-B-I-1-SE",
        )
        self.assertEqual(
            grid_utm.inomenFromExtent(-46.365, -22.230, -46.150, -22.125), ""
        )  # Not a whole product

