""" File containing the code for constructing the an iso xml file based on its fields """

from lxml import etree
from re import split


def to_seach_string(old_path: str) -> str:
    return "./{*}" + "/{*}".join(
        x
        for x in split(r"/\w+:", old_path.replace(" ", "_"))
        if x not in {"", "MD_Metadata"}
    )


def construct_xml(template_path: str, old_paths: list[str], values: list[str]) -> bytes:
    tree = etree.parse(template_path)
    for old_path, value in zip(old_paths, values):
        element = tree.find(to_seach_string(old_path))
        if element is None:
            pass
        else:
            element.text = value

    return etree.tostring(tree)
