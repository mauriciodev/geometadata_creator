"""Gera a fixture app/core/fixtures/feature_catalogs.json a partir da lista de conferencia.

Le ../classes_maptopope_conferencia.txt (relativo a raiz do repo) e produz, em UTF-8:
  - 1 registro core.featurecatalog (ET-EDGV 3.0 / perfil MapTopoPE);
  - 1 registro core.featurecatalogclass por classe, com name no formato
    Trecho_Drenagem e category com o prefixo de 3 letras (hid, rel, ...).

Gerar programaticamente elimina erro de digitacao nas ~107 classes.

Uso:
    pixi run python scripts/generate_feature_catalog_fixture.py
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_FILE = REPO_ROOT.parent / "classes_maptopope_conferencia.txt"
OUTPUT_FILE = REPO_ROOT / "app" / "core" / "fixtures" / "feature_catalogs.json"

CATALOG_PK = 1
CATALOG = {
    "model": "core.featurecatalog",
    "pk": CATALOG_PK,
    "fields": {
        "title": "ET-EDGV 3.0",
        "abreviation": "ET-EDGV 3.0",
        "date": "2018-05-20",
        "edition": "3.0",
        "edition_date": "2018-05-20",
        "series": "Perfil MapTopoPE - Mapeamento Topografico de Pequena Escala",
    },
}


def class_name(raw: str) -> str:
    """trecho_drenagem -> Trecho_Drenagem (capitaliza cada segmento)."""
    return "_".join(part.capitalize() for part in raw.strip().split("_"))


def main() -> None:
    objects = [CATALOG]
    category = None
    pk = 0
    counts: dict[str, int] = {}
    for line in REFERENCE_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("TOTAL"):
            continue
        if not line.startswith(" ") and line.rstrip().endswith(":"):
            category = line.split("(")[0].strip()
        elif category is not None:
            pk += 1
            counts[category] = counts.get(category, 0) + 1
            objects.append(
                {
                    "model": "core.featurecatalogclass",
                    "pk": pk,
                    "fields": {
                        "feature_catalog": CATALOG_PK,
                        "name": class_name(line),
                        "category": category,
                        "description": "",
                    },
                }
            )

    OUTPUT_FILE.write_text(
        json.dumps(objects, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Fixture gravada em {OUTPUT_FILE}")
    print(f"1 catalogo + {pk} classes em {len(counts)} categorias:")
    for cat, n in sorted(counts.items()):
        print(f"   {cat}: {n}")


if __name__ == "__main__":
    main()
