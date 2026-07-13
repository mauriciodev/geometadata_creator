"""Cria os MetadataFormField exclusivos dos produtos vetoriais e os associa aos ProductTypes.

Idempotente (get_or_create + M2M add): pode ser rodado quantas vezes for preciso.
O campo "Catálogo de feições" é um combobox cujas opções vêm dos FeatureCatalog
cadastrados (fixture feature_catalogs.json); o valor é gravado no title da
featureCatalogueCitation do bloco MD_FeatureCatalogueDescription do template.

Uso (da raiz do repo):
    pixi run python scripts/create_vector_form_fields.py

A lógica fica em create_catalog_field() para poder ser importada pelos testes
(core/tests/test_vector_product_support.py) sem refazer o bootstrap do Django.
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

VECTOR_PRODUCT_TYPE_PKS = (3, 4)  # SCN Carta Topografica Vetorial (completa e sumarizada)

CATALOG_FIELD = {
    "iso_xml_path": "MD_FeatureCatalogueDescription-featureCatalogueCitation-title",
    "defaults": {
        "label": "Catálogo de feições",
        "field_type": "combobox",
        "is_static": False,
        "default_value": "ET-EDGV 3.0",
        "comments": (
            "Catálogo de feições (ET-EDGV) que rege as classes do produto vetorial. "
            "Opções vêm dos FeatureCatalog cadastrados. Futuramente pré-preenchido "
            "pela extração automática (extract_vector_metadata)."
        ),
        "old_path": (
            "/gmd:MD_Metadata/gmd:contentInfo[2]/gmd:MD_FeatureCatalogueDescription"
            "/gmd:featureCatalogueCitation/gmd:CI_Citation/gmd:title/gco:CharacterString"
        ),
    },
}


def create_catalog_field(verbose: bool = True):
    """Cria/atualiza o campo "Catálogo de feições" e o associa aos PTs vetoriais.

    Requer Django já configurado (django.setup() ou ambiente de teste).
    Retorna o MetadataFormField.
    """
    from core.models.feature_catalog import FeatureCatalog
    from core.models.producttype import MetadataFormField, ProductType

    titles = list(FeatureCatalog.objects.values_list("title", flat=True).order_by("id"))
    if not titles:
        raise RuntimeError(
            "Nenhum FeatureCatalog cadastrado. Rode antes: "
            "pixi run python manage.py loaddata core/fixtures/feature_catalogs.json"
        )
    possible_values = ", ".join(titles)  # o frontend faz split(',') + trim

    field, created = MetadataFormField.objects.get_or_create(
        iso_xml_path=CATALOG_FIELD["iso_xml_path"],
        defaults={**CATALOG_FIELD["defaults"], "possible_values": possible_values},
    )
    if not created and field.possible_values != possible_values:
        field.possible_values = possible_values
        field.save(update_fields=["possible_values"])
        if verbose:
            print(f"possible_values atualizado: {possible_values!r}")
    if verbose:
        print(f"Campo {'criado' if created else 'ja existia'}: {field}")

    for pk in VECTOR_PRODUCT_TYPE_PKS:
        pt = ProductType.objects.get(pk=pk)
        pt.metadata_fields.add(field)
        if verbose:
            print(f"PT {pk} ({pt.name}): {pt.metadata_fields.count()} campos")

    return field


def main() -> None:
    sys.path.insert(0, str(REPO_ROOT / "app"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geometadata_creator.settings")

    import django

    django.setup()
    create_catalog_field()


if __name__ == "__main__":
    main()
