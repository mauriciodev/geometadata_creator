from pathlib import Path
from typing import Literal
from typing_extensions import Self
import rasterio
from pydantic import (
    BaseModel,
    model_serializer,
    model_validator,
)
from core.models import IndexMap
from rasterio.warp import transform_bounds

"""Trazer: 
            Formato do arquivo
    gmd:distributionFormat gmd:name gco:CharacterString
Extensão espacial (min x, min y, max x, max y)
    gmd:MD_DataIdentification gmd:northBoundLatitude gco:Decimal
    gmd:MD_DataIdentification gmd:westBoundLongitude gco:Decimal
    gmd:MD_DataIdentification gmd:southBoundLatitude gco:Decimal
    gmd:MD_DataIdentification gmd:eastBoundLongitude gco:Decimal
Tipo de representação espacial (Matricial/Vetorial)
    gmd:MD_DataIdentification gmd:spatialRepresentationType gco:CharacterString
Palavras-chave
    gmd:MD_DataIdentification gmd:descriptiveKeywords gmd:keyword gco:CharacterString
Sistema de referência (EPSG, descrição, DATUM)
    Código epsg: gmd:MD_ReferenceSystem gmd:referenceSystemIdentifier gmd:code gco:CharacterString
    Autoridade: gmd:MD_ReferenceSystem gmd:referenceSystemIdentifier gmd:authority gco:CharacterString
    Datum vertical: gmd:MD_DataIdentification gmd:verticalExtent gmd:verticalDatum gco:CharacterString
Resolução espacial X e Y
    row: gmd:spatialRepresentationInfo MD_Georectified gmd:axisDimensionProperties gmd:dimensionName gco:CharacterString
    Resolução da row: gmd:spatialRepresentationInfo MD_Georectified gmd:axisDimensionProperties gmd:resolution gco:Decimal
    column: gmd:spatialRepresentationInfo MD_Georectified gmd:axisDimensionProperties gmd:dimensionName gco:CharacterString
    Resolução da column: gmd:spatialRepresentationInfo MD_Georectified gmd:axisDimensionProperties gmd:resolution gco:Decimal
Quantidade de bits
Escala (opcional)
    gmd:MD_DataIdentification gmd:spatialResolution gmd:denominator gco:Integer"""


class RasterExtractableInfo(BaseModel):
    north_bound_lat: float
    south_bound_lat: float
    east_bound_lon: float
    west_bound_lon: float
    data_representation_type: Literal["Matricial"] = "Matricial"
    epsg_code: int
    driver: str
    scale_denominator1: int
    scale_denominator2: int
    inom: str
    mi: str
    spatial_resolution: int | None = None

    @model_validator(mode="after")
    def check_model_validation(self) -> Self:
        # Check that the driver is correct
        format_alias = {"GTif": "GeoTiff"}
        self.driver = (
            format_alias[self.driver]
            if self.driver in format_alias.keys()
            else self.driver
        )

        # Check that the ...
        contour_lines_height = {10000: 5, 25000: 10, 50000: 20, 100000: 50, 250000: 100}
        if self.spatial_resolution in contour_lines_height:
            self.spatial_resolution = contour_lines_height[self.spatial_resolution]
        else:
            self.spatial_resolution = None

        return self

    @model_serializer()
    def serializer(self):
        return {
            "MD_DataIdentification-extent-geographicElement1-northBoundLatitude": self.north_bound_lat,
            "MD_DataIdentification-extent-geographicElement1-southBoundLatitude": self.south_bound_lat,
            "MD_DataIdentification-extent-geographicElement1-eastBoundLongitude": self.east_bound_lon,
            "MD_DataIdentification-extent-geographicElement1-westBoundLongitude": self.west_bound_lon,
            "MD_DataIdentification-spatialRepresentationType": self.data_representation_type,
            "MD_ReferenceSystem-referenceSystemIdentifier-code": self.epsg_code,
            "MD_Distribution-distributionFormat-name": self.driver,
            "MD_DataIdentification-spatialResolution-equivalentScale-denominator1": self.scale_denominator1,
            "MD_DataIdentification-spatialResolution-equivalentScale-denominator2": self.scale_denominator2,
            "MD_Identification-citation-alternateTitle": self.inom,
            "MD_Identification-citation-alternateTitle": self.mi,
            "MD_DataIdentification-spatialResolution-distance": self.spatial_resolution,
        }


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
            response = RasterExtractableInfo(
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
            )
        return response
    except Exception as _:
        raise Exception("Erro na hora de ler o arquivo")
