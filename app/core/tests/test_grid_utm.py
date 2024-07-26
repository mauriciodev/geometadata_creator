import os

from django.urls import reverse
from django.test import TestCase

from core.models import IndexMap

class IndexMapTests(TestCase):
    fixtures = ["index_map"]
    def setUp(self):
        super().setUp()

    #checks if fixtures are being loaded
    def test_loaded_fixture(self):
        self.assertGreater(IndexMap.objects.count(),3000)

    def test_inomen_to_mi(self):
        self.assertEqual(IndexMap.objects.get_mi('SC-22-Y-C'),'321') #MIR 250k
        self.assertEqual(IndexMap.objects.get_mi('SC-22-Y-C-I'),'1761') #MI 100k
        self.assertEqual(IndexMap.objects.get_mi('SD-21-X-B-III-2-NO'),'1873-2-NO') #MI 25k

    def test_mi_to_inomen(self):
        self.assertEqual(IndexMap.objects.get_inomen_by_mi('321',is_mir=True),'SC-22-Y-C') #MIR 250k
        self.assertEqual(IndexMap.objects.get_inomen_by_mi('1761'),'SC-22-Y-C-I') #MI 100k
        self.assertEqual(IndexMap.objects.get_inomen_by_mi('1873-2-NO'),'SD-21-X-B-III-2-NO') #MI 25k

    def test_inomen_from_file(self):
        filename = 'core/tests/test_data/recorte.tif'
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(IndexMap.objects.get_inomen_mi_from_rasterio(filename),('SD-21-V-A-II-4-SO-C', '1863-4-SO-C'))
