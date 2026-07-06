from pathlib import Path
import zipfile
import rasterio
from core.models import IndexMap
from rasterio.warp import transform_bounds
from file_handler.schemas import FileExtractedFields
import geopandas as gpd
from shapely.geometry import box


def parse_file(geodata_file: str) -> FileExtractedFields:
    suffix = Path(geodata_file).suffix
    match suffix:
        case ".tiff" | ".tif":
            return extract_raster_metadata(geodata_file)
        case ".gpkg" | ".zip":
            # TODO: PFC2026
            return extract_vector_metadata(geodata_file)   
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
    except Exception as e:
        raise e

def extract_vector_metadata(geodata_file: str):
    bounds = None
    layer_names = []

    if geodata_file.endswith(".gpkg"):
        layer_names = gpd.list_layers(geodata_file)[1]
    elif geodata_file.endswith(".zip"):
        with zipfile.ZipFile(geodata_file) as z:
            for name in z.namelist():
                if name.endswith(".shp"):
                    layer_names.append(name)

    for layer_name in layer_names:
        if geodata_file.endswith(".gpkg"):
            gdf = gpd.read_file(geodata_file, layer=layer_name)
        else:
            gdf = gpd.read_file(f"zip://{geodata_file}!{layer_name}")

        current_bounds = gdf.total_bounds
        if bounds is None:
            bounds = current_bounds.copy()
        else:
            bounds[0] = min(bounds[0], current_bounds[0])
            bounds[1] = min(bounds[1], current_bounds[1])
            bounds[2] = max(bounds[2], current_bounds[2])
            bounds[3] = max(bounds[3], current_bounds[3])

    if bounds is None:
        raise ValueError("Nenhuma camada vetorial encontrada")

    west, south, east, north = bounds
    return FileExtractedFields(
        north_bound_lat=north,
        west_bound_lon=west,
        east_bound_lon=east,
        south_bound_lat=south,
        epsg_code=int(gdf.crs.to_epsg()) if gdf.crs is not None else None,
        driver="GeoPackage" if geodata_file.endswith(".gpkg") else "ESRI Shapefile",
        scale_denominator1=None,
        scale_denominator2=None,
        data_representation_type="Vetorial",
    )
