from pathlib import Path
import rasterio
from pydantic import BaseModel

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
    try:
        with rasterio.open(geodata_file) as img_ds:
            response = RasterExtractableInfo(
                extensao_espacial=img_ds.bounds,  # metadata
                driver=img_ds.driver,
                resolucao_espacial=(
                    img_ds.get_transform()[1],
                    img_ds.get_transform()[5],
                ),
            )
        return response
    except Exception as _:
        raise Exception("Erro na hora de ler o arquivo")
