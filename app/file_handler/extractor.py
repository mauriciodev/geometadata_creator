from pathlib import Path
import rasterio
from pydantic import BaseModel
from core.models import IndexMap

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
    extensao_espacial: tuple[float, float, float, float]
    driver: str
    resolucao_espacial: tuple[float, float]


def parse_file(geodata_file: str):
    suffix = Path(geodata_file).suffix
    match suffix:
        case ".tiff" | ".tif":
            return extract_raster_metadata(geodata_file)
        case _:
            raise TypeError("Arquivo não é do tipo geoespacial")


def extract_raster_metadata(geodata_file: str):
    contour_lines_height = {10000:5, 25000: 10, 50000: 20, 100000: 50, 250000: 100}
    format_map = {'GTif': 'GeoTiff'}
    try:
        with rasterio.open(geodata_file) as img_ds:
            WGS84_crs = rasterio.CRS.from_epsg(4326)  # WGS84
            extent = rasterio.warp.transform_bounds(img_ds.crs, WGS84_crs, *img_ds.bounds)
            response = {
                'MD_DataIdentification-extent-geographicElement1-northBoundLatitude': extent[3],
                'MD_DataIdentification-extent-geographicElement1-westBoundLongitude': extent[0],
                'MD_DataIdentification-extent-geographicElement1-eastBoundLongitude': extent[2],
                'MD_DataIdentification-extent-geographicElement1-southBoundLatitude': extent[1],
                'MD_DataIdentification-spatialRepresentationType': 'Matricial',
                'MD_ReferenceSystem-referenceSystemIdentifier-code': img_ds.crs.to_epsg(),
            }
            if img_ds.driver in format_map:
                response['MD_Distribution-distributionFormat-name']: format_map[img_ds.driver]
            else:
                response['MD_Distribution-distributionFormat-name']: img_ds.driver
        
        #closing file to open on IndexMap
        inom, mi = IndexMap.objects.get_inomen_mi_from_rasterio(geodata_file)
        grid_utm = IndexMap.objects.get_grid_utm()
        scale = grid_utm.getScale(inom)

        response['MD_DataIdentification-spatialResolution-equivalentScale-denominator1']= scale
        response['MD_DataIdentification-spatialResolution-equivalentScale-denominator2']= scale
        response['MD_Identification-citation-alternateTitle']= inom
        response['MD_Identification-citation-alternateTitle']= mi
        if int(scale) in contour_lines_height:
            response['MD_DataIdentification-spatialResolution-distance'] = contour_lines_height[int(scale)]

        return response
    except Exception as _:
        raise Exception("Erro na hora de ler o arquivo")
