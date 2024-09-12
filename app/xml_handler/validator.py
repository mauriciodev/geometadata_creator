""" File containing the function for validating an geo metadata xml file """

from pathlib import Path
from owslib.iso import MD_Metadata
from xml_handler.constructor import to_seach_string
from core.models import ProductType, MetadataFormField
from lxml.etree import _ElementTree
from lxml import etree as et
from enum import Enum


class MissingFieldsScenarios(Enum):
    case_1 = "Path was found."
    case_2 = "Field was not found."
    case_3 = "Field search string was malformed."
    case_4 = "Product type not registered."
    case_5 = "File doesn't have the product type field."


def get_product_type(xml_tree: _ElementTree) -> ProductType | MissingFieldsScenarios:
    product_type_field = MetadataFormField.objects.get(
        iso_xml_path="MD_Identification-citation-series-name"
    )
    try:
        element = xml_tree.find(to_seach_string(product_type_field.old_path))
    except:
        return MissingFieldsScenarios.case_3
    else:
        if element is None:
            return MissingFieldsScenarios.case_3

        product_type = ProductType.objects.get(name=element.text)
        if product_type is None:
            return product_type
        else:
            return MissingFieldsScenarios.case_4


def collect_fields(
    xml_tree: _ElementTree, product_type: ProductType
) -> tuple[dict, dict]:

    collected_fields, missing_fields = {}, {}
    for field in product_type.metadata_fields.all():
        try:
            element = xml_tree.find(to_seach_string(field.old_path))
        except Exception as _:
            missing_fields[field.iso_xml_path] = MissingFieldsScenarios.case_3
        else:
            if element is None:
                missing_fields[field.iso_xml_path] = MissingFieldsScenarios.case_2
            else:
                collected_fields[field.iso_xml_path] = element.text

    return collected_fields, missing_fields


def basic_validator(xml_path: str | Path) -> bool | Exception:
    """Verifica se o arquivo existe, se ele é um xml válido e se pode ser aberto pela owslib"""

    # Verifica se o arquivo existe e se possui a extensão xml
    xml_path = Path(xml_path) if isinstance(xml_path, str) else xml_path
    if not xml_path.exists():
        return Exception("Arquivo não encontrado")
    elif xml_path.suffix != ".xml":
        return Exception("Arquivo não é xml")

    # Verifica se o arquivo possui uma estrutura xml válida
    try:
        with open(xml_path) as file:
            xml = et.parse(file)
    except Exception as _:
        return Exception("Problema com a estrutura do xml.")

    # Verifica se o arquivo pode ser lido pela owslib
    try:
        metadata = MD_Metadata(xml)
    except Exception as _:
        return Exception("O arquivo não pode ser lido pela owslib")

    return True
