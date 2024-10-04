""" File containing the code for constructing the an iso xml file based on its fields """

from lxml import etree as et
from re import findall
from core.models import MetadataFormField


def old_path_to_search_string(old_path: str) -> str:
    return "./" + "/".join("{*}" + t for _, t in findall(r"/(\w+):(\w+)", old_path)[1:])


def fill_xml_template(
    template_tree: et._ElementTree, field_value_map: list[tuple[str, str]]
) -> tuple[et._ElementTree, list[str], list[str]]:
    fields_not_in_template, fields_not_registered = [], []
    for field_name, value in field_value_map:
        try:
            field = MetadataFormField.objects.get(name=field_name)
        except MetadataFormField.DoesNotExist:
            fields_not_registered.append(field_name)
        else:
            element = template_tree.find(old_path_to_search_string(field.old_path))
            if element is None:
                fields_not_in_template.append(field_name)
            else:
                element.text = value

    return template_tree, fields_not_in_template, fields_not_registered
