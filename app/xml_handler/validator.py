""" File containing the function for validating an geo metadata xml file """

from pathlib import Path
from owslib.iso import MD_Metadata
from xml.etree import ElementTree as et


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
