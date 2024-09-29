from pathlib import Path
import rasterio
from core.models import IndexMap
from rasterio.warp import transform_bounds
from file_handler.schemas import FileExtractedFields


def parse_file(geodata_file: str):
    suffix = Path(geodata_file).suffix
    match suffix:
        case ".tiff" | ".tif":
            return extract_raster_metadata(geodata_file)
        case _:
            raise TypeError("Arquivo não é do tipo geoespacial")


def extract_raster_metadata(geodata_file: str):
    try:
        inom, mi = IndexMap.objects.get_inomen_mi_from_rasterio(geodata_file)  # type: ignore
        grid_utm = IndexMap.objects.get_grid_utm()  # type: ignore
        scale = int(grid_utm.getScale(inom))

        with rasterio.open(geodata_file) as img_ds:
            WGS84_crs = rasterio.CRS.from_epsg(4326)  # WGS84
            extent = transform_bounds(img_ds.crs, WGS84_crs, *img_ds.bounds)
            response = FileExtractedFields(
                north_bound_lat=extent[3],
                west_bound_lon=extent[0],
                east_bound_lon=extent[2],
                south_bound_lat=extent[1],
                epsg_code=img_ds.crs.to_epsg(),
                driver=img_ds.driver,
                scale_denominator1=scale,
                scale_denominator2=scale,
                inom=inom,
                mi=mi,
                data_representation_type="Matricial",
            )
        return response
    except Exception as _:
        raise Exception("Erro na hora de ler o arquivo")
