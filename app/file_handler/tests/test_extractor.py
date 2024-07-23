from pathlib import Path
from django.test import TestCase
from numpy import float64, zeros
from file_handler.extractor import RasterExtractableInfo, parse_file
import rasterio
from os import remove

RASTEREXAMPLE = Path("core/tests/test_data/example.tif")


def create_example() -> RasterExtractableInfo:
    # Create the example

    driver = "GTiff"
    resx, resy = 1.0, -1.0
    left, bottom, right, top = 0, 0, 1, 1
    Z = zeros((1, 1), dtype=float64)

    # Write the example to disk
    with rasterio.open(
        RASTEREXAMPLE,
        "w",
        driver="GTiff",
        height=Z.shape[0],
        width=Z.shape[1],
        count=1,
        dtype=Z.dtype,
        crs="+proj=latlong",
        transform=rasterio.Affine(resx, 0.0, left, 0.0, resy, top),
    ) as dst:
        dst.write(Z, 1)

    # Return the correct value
    return RasterExtractableInfo(
        extensao_espacial=(left, bottom, right, top),
        driver=driver,
        resolucao_espacial=(resx, resy),
    )


class GMDExtractorTests(TestCase):
    def setUp(self) -> None:
        self.solution = create_example()
        return super().setUp()

    def test_response(self):
        """
        Ensure we get a dict from using the extract raster method
        """
        response = parse_file("core/tests/test_data/example.tif")
        self.assertIsInstance(response, RasterExtractableInfo)

    def test_value_acuracy(self):
        """
        Ensure that the values collected are correct
        """
        response = parse_file("core/tests/test_data/example.tif")
        self.assertEqual(response.model_dump(), self.solution.model_dump())

    def tearDown(self) -> None:
        remove(RASTEREXAMPLE)
        return super().tearDown()
