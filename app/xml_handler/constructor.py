""" File containing the code for constructing the an iso xml file based on its fields """

from lxml import etree as et
from re import findall
from core.models.producttype import ProductType


def old_path_to_search_string(old_path: str) -> str:
    return "./" + "/".join("{*}" + t for _, t in findall(r"/(\w+):(\w+)", old_path)[1:])


def fill_xml_template(
    product_type: ProductType, field_value_map: list[tuple[str, str]]
) -> tuple[et._ElementTree, list[str]]:
    template_tree = et.parse(str(product_type.xml_template))
    label_path_map = {
        field.iso_xml_path: field.old_path
        for field in product_type.metadata_fields.all()
    }
    fields_not_registered = []
    for field_name, value in field_value_map:
        old_path = label_path_map.get(field_name, None)
        if old_path is None:
            fields_not_registered.append(field_name)
        else:
            element = template_tree.find(old_path_to_search_string(old_path))
            if element is not None:
                element.text = str(value)

    return template_tree, fields_not_registered
