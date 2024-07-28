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
    wb, sb, eb, nb = 0, 0, 1, 1
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
        transform=rasterio.Affine(resx, 0.0, wb, 0.0, resy, nb),
    ) as dst:
        dst.write(Z, 1)

    # Return the correct value
    return RasterExtractableInfo(
        north_bound_lat=nb,
        south_bound_lat=sb,
        east_bound_lon=eb,
        west_bound_lon=wb,
        driver=driver,
        epsg_code=4326,
        scale_denominator1=100000,
        scale_denominator2=100000,
        inom="",
        mi="",
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
        # self.assertEqual(response, self.solution)
        self.assertDictEqual(response.model_dump(), self.solution.model_dump())

    def tearDown(self) -> None:
        remove(RASTEREXAMPLE)
        return super().tearDown()
