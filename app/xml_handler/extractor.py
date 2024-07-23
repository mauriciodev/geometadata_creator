from enum import Enum
from xml.etree import ElementTree


class RasterVariables(Enum):
    file_identifier = ".//{*}fileIdentifier/{*}CharacterString"
    product_name = ".//{*}CI_Series/{*}name/{*}CharacterString"
    nbt = ".//{*}extent//{*}northBoundLatitude/{*}Decimal"
    sbt = ".//{*}extent//{*}southBoundLatitude/{*}Decimal"
    wbt = ".//{*}extent//{*}westBoundLongitude/{*}Decimal"
    ebt = ".//{*}extent//{*}eastBoundLongitude/{*}Decimal"
    format = ".//{*}distributionInfo//{*}MD_Format/{*}name/{*}CharacterString"


class VariableXPaths(Enum):
    file_identifier = ".//{*}fileIdentifier/{*}CharacterString"
    product_name = ".//{*}CI_Series/{*}name/{*}CharacterString"
    nbt = ".//{*}extent//{*}northBoundLatitude/{*}Decimal"
    sbt = ".//{*}extent//{*}southBoundLatitude/{*}Decimal"
    wbt = ".//{*}extent//{*}westBoundLongitude/{*}Decimal"
    ebt = ".//{*}extent//{*}eastBoundLongitude/{*}Decimal"
    format = ".//{*}distributionInfo//{*}MD_Format/{*}name/{*}CharacterString"


class FileTypes(Enum):
    raster = "tiff"


def parse_xml(xml: ElementTree.ElementTree):
    # Validate the file

    # Get the type of product

    # Get other information
    pass
