""" File containing the code for constructing the an iso xml file based on its fields """

from lxml import etree as et
from re import findall


def old_path_to_search_string(old_path: str) -> str:
    return "./" + "/".join("{*}" + t for _, t in findall(r"/(\w+):(\w+)", old_path)[1:])


def construct_xml(template_path: str, old_paths: list[str], values: list[str]) -> bytes:
    tree = etree.parse(template_path)
    for old_path, value in zip(old_paths, values):
        element = tree.find(to_seach_string(old_path))
        if element is None:
            pass
        else:
            element.text = value

    return etree.tostring(tree)
