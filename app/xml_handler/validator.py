from pathlib import Path
from core.fields import UniversalFields as UF
from lxml import etree as et
from xml_handler.constructor import old_path_to_search_string
from core.models import ProductType


def validate_file_integrity(xml_path: str | Path) -> et._ElementTree:
    """
    Vefify if the file exists and if it is a valid xml file.
    If it is, returns the etree object.
    """

    # Verifica se o arquivo existe e se possui a extensão xml
    xml_path = Path(xml_path) if isinstance(xml_path, str) else xml_path
    if not xml_path.exists():
        raise FileNotFoundError("File was not found.")

    et.parse(xml_path)
    # Verifica se o arquivo possui uma estrutura xml válida

    try:
        xml_tree = et.parse(xml_path)
    except Exception as _:
        raise ValueError("O arquivo não é um xml válido.")

    return xml_tree


def find_product_type_from_xml(xml_tree: et._ElementTree) -> ProductType:
    # Find the product type for the file field
    product_type_element = xml_tree.find(
        old_path_to_search_string(UF.product_type.value)
    )
    if product_type_element is None:
        raise ValueError("Could not get the product type from the metadata.")
    product_type_name = product_type_element.text

    # Find the product type
    product_type = ProductType.objects.filter(name=product_type_name).first()
    if product_type is None:
        raise ValueError("Product type not suported.")

    return product_type


def validate_fields_based_on_product_type(
    xml_tree: et._ElementTree, product_type: ProductType
) -> tuple[dict, set]:
    """
    - Collect the fields from the product type;
    - Collect the value of the fields that where found;
    - Maps the fields that where missing;
    """
    collected_fields, missing_fields = {}, set()
    for field in product_type.metadata_fields.all():
        element = xml_tree.find(old_path_to_search_string(field.old_path))
        if element is None:
            missing_fields.add(field.iso_xml_path)
        else:
            collected_fields[field.iso_xml_path] = element.text

    return collected_fields, missing_fields
