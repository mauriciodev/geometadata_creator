from rasterio.transform import from_bounds
from rasterio.io import MemoryFile
from file_handler.schemas import FileExtractedFields
from numpy import zeros, float64


def get_example_raster() -> tuple[bytes, FileExtractedFields]:
    # Define the metadata for the raster (e.g., GeoTIFF)
    north_bound, east_bound, west_bound, south_bound = 0.0, 1.0, 0.0, -1.0
    width, height = 256, 256
    data = zeros((height, width), dtype=float64)
    meta = {
        "driver": "GTiff",
        "dtype": float64,
        "width": width,
        "height": height,
        "count": 1,  # Number of bands
        "crs": "EPSG:4326",  # Coordinate Reference System
        "transform": from_bounds(
            west_bound, south_bound, east_bound, north_bound, width, height
        ),
    }
    fields = FileExtractedFields(
        north_bound_lat=north_bound,
        south_bound_lat=south_bound,
        east_bound_lon=east_bound,
        west_bound_lon=west_bound,
        epsg_code=4326,
        driver="GTiff",
    )

    # Use MemoryFile to create an in-memory raster
    with MemoryFile() as memfile:
        with memfile.open(**meta) as dataset:
            dataset.write(data, 1)  # Write the array to the first band

        # Get the binary data without writing it to disk
        binary_data = memfile.read()
    return binary_data, fields
