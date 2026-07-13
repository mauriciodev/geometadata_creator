"""Script exploratorio: identifica o catalogo de feicoes (ET-EDGV/MapTopoPE) de um GeoPackage.

Decompoe os nomes das camadas pela convencao `<categoria>_<classe>_<geometria>`
e compara com a lista de referencia do MapTopoPE, imprimindo um relatorio de
correspondencia. Nao depende do Django — e insumo para a fixture de
FeatureCatalog e para a futura extract_vector_metadata().

Uso:
    pixi run python scripts/identify_feature_catalog.py [caminho/para/arquivo.gpkg]
"""

import sys
from pathlib import Path

try:
    import fiona

    def list_layers(path: str) -> list[str]:
        return list(fiona.listlayers(path))

except ImportError:  # geopandas >= 1.x usa pyogrio; fiona nao vem no ambiente pixi
    import pyogrio

    def list_layers(path: str) -> list[str]:
        return [name for name, _geom in pyogrio.list_layers(path)]

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GPKG = REPO_ROOT / "examples" / "f100.gpkg"
REFERENCE_FILE = REPO_ROOT.parent / "classes_maptopope_conferencia.txt"

GEOMETRY_SUFFIXES = {"p": "ponto", "l": "linha", "a": "área"}


def load_reference(path: Path) -> dict[str, set[str]]:
    """Le a lista de referencia (linhas `categoria (n):` seguidas de classes indentadas).

    Retorna {categoria: {nome_de_classe_normalizado, ...}}.
    """
    catalog: dict[str, set[str]] = {}
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("TOTAL"):
            continue
        if not line.startswith(" ") and line.rstrip().endswith(":"):
            current = line.split("(")[0].strip()
            catalog[current] = set()
        elif current is not None:
            catalog[current].add(normalize(line.strip()))
    return catalog


def normalize(name: str) -> str:
    """Normaliza um nome de classe para comparacao (minusculas): Trecho_Drenagem -> trecho_drenagem."""
    return name.strip().lower()


def parse_layer(layer: str) -> tuple[str, str, str] | None:
    """Decompoe `<categoria>_<classe>_<geometria>` -> (categoria, classe, geometria).

    Retorna None se o nome nao segue a convencao.
    """
    parts = layer.split("_")
    if len(parts) < 3:
        return None
    category, *middle, suffix = parts
    if len(category) != 3 or suffix not in GEOMETRY_SUFFIXES:
        return None
    return category.lower(), "_".join(middle), suffix


def main() -> None:
    gpkg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_GPKG
    if not gpkg.exists():
        sys.exit(f"Arquivo nao encontrado: {gpkg}")
    if not REFERENCE_FILE.exists():
        sys.exit(f"Lista de referencia nao encontrada: {REFERENCE_FILE}")

    reference = load_reference(REFERENCE_FILE)
    total_ref_classes = sum(len(v) for v in reference.values())
    layers = list_layers(str(gpkg))

    recognized: dict[tuple[str, str], list[str]] = {}  # (categoria, classe) -> [camadas]
    unparsed: list[str] = []       # fora do padrao <cat>_<classe>_<geom>
    unknown: list[str] = []        # padrao ok, mas fora do catalogo

    for layer in layers:
        parsed = parse_layer(layer)
        if parsed is None:
            unparsed.append(layer)
            continue
        category, cls, _geom = parsed
        if category in reference and normalize(cls) in reference[category]:
            recognized.setdefault((category, normalize(cls)), []).append(layer)
        else:
            unknown.append(layer)

    matched_classes = set(recognized)
    missing = {
        (cat, cls)
        for cat, classes in reference.items()
        for cls in classes
        if (cat, cls) not in matched_classes
    }

    print(f"GeoPackage: {gpkg}")
    print(f"Referencia: {REFERENCE_FILE.name} ({total_ref_classes} classes, {len(reference)} categorias)")
    print()
    print(f"Total de camadas no arquivo:            {len(layers)}")
    print(f"Camadas reconhecidas no catalogo:       {sum(len(v) for v in recognized.values())}")
    print(f"Classes distintas reconhecidas:         {len(matched_classes)}")
    print(f"Camadas fora do padrao de nome:         {len(unparsed)}")
    print(f"Camadas fora do catalogo:               {len(unknown)}")
    print(f"Classes do catalogo ausentes no produto: {len(missing)}")
    print()
    pct_layers = 100 * sum(len(v) for v in recognized.values()) / len(layers) if layers else 0
    pct_catalog = 100 * len(matched_classes) / total_ref_classes if total_ref_classes else 0
    print(f"Correspondencia (camadas do arquivo reconhecidas):  {pct_layers:.1f}%")
    print(f"Cobertura do catalogo (classes presentes/total):    {pct_catalog:.1f}%")

    if unparsed:
        print("\nCamadas fora do padrao <categoria>_<classe>_<geometria>:")
        for layer in sorted(unparsed):
            print(f"   {layer}")
    if unknown:
        print("\nCamadas com padrao valido mas fora do catalogo:")
        for layer in sorted(unknown):
            print(f"   {layer}")
    if missing:
        print("\nClasses do catalogo ausentes no produto:")
        for cat, cls in sorted(missing):
            print(f"   {cat}_{cls}")


if __name__ == "__main__":
    main()
