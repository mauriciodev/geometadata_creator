"""Testes do suporte a produtos vetoriais (PFC 2026).

Um bloco de testes por alteração:
  1. FeatureCatalogClassCategoryTests   -> campo `category` no model (migration 0002)
  2. FeatureCatalogFixtureTests         -> fixture feature_catalogs.json (ET-EDGV 3.0, 107 classes)
  3. TemplateFeatureCatalogueBlockTests -> bloco MD_FeatureCatalogueDescription no template XML
  4. CreateVectorFormFieldsScriptTests  -> campo "Catálogo de feições" + associação aos PTs 3 e 4
  5. VectorFormFieldEndToEndTests       -> valor do formulário chega ao XML (fill_xml_template)
  6. IdentifyFeatureCatalogScriptTests  -> decomposição de nomes de camada (script exploratório)
  7. GenerateFixtureScriptTests         -> formatação de nomes do gerador da fixture
"""

import importlib.util
import tempfile
from datetime import date
from pathlib import Path

from django.db.models import Count
from django.test import SimpleTestCase, TestCase
from lxml import etree as et

from core.models.feature_catalog import FeatureCatalog, FeatureCatalogClass
from core.models.producttype import MetadataFormField, ProductType
from xml_handler.constructor import fill_xml_template, old_path_to_search_string

APP_DIR = Path(__file__).resolve().parent.parent.parent  # .../app
SCRIPTS_DIR = APP_DIR.parent / "scripts"
TEMPLATE_RELATIVE = "core/fixtures/pt_templates/PORTO ALEGRE - valido.xml"
TEMPLATE_PATH = APP_DIR / TEMPLATE_RELATIVE

CATALOG_ISO_PATH = "MD_FeatureCatalogueDescription-featureCatalogueCitation-title"

# Contagens por categoria do classes_maptopope_conferencia.txt (total 107)
EXPECTED_CATEGORY_COUNTS = {
    "aer": 1, "dut": 2, "eco": 3, "enc": 14, "fer": 3, "hdv": 6, "hid": 19,
    "lml": 15, "pto": 4, "rel": 14, "rod": 1, "snb": 2, "tra": 12, "veg": 11,
}


def load_script(name: str):
    """Importa um módulo de scripts/ (que não é pacote) pelo caminho do arquivo."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FeatureCatalogClassCategoryTests(TestCase):
    """Alteração 1: campo `category` em FeatureCatalogClass."""

    def setUp(self):
        self.catalog = FeatureCatalog.objects.create(
            title="ET-EDGV 3.0",
            abreviation="ET-EDGV 3.0",
            date=date(2018, 5, 20),
            edition="3.0",
            edition_date=date(2018, 5, 20),
            series="Perfil MapTopoPE",
        )

    def test_category_is_persisted_and_queryable(self):
        FeatureCatalogClass.objects.create(
            feature_catalog=self.catalog,
            name="Trecho_Drenagem",
            category="hid",
            description="",
        )
        stored = FeatureCatalogClass.objects.get(name="Trecho_Drenagem")
        self.assertEqual(stored.category, "hid")
        self.assertEqual(FeatureCatalogClass.objects.filter(category="hid").count(), 1)

    def test_category_defaults_to_blank(self):
        cls = FeatureCatalogClass.objects.create(
            feature_catalog=self.catalog, name="Sem_Categoria", description=""
        )
        cls.refresh_from_db()
        self.assertEqual(cls.category, "")


class FeatureCatalogFixtureTests(TestCase):
    """Alteração 2: fixture feature_catalogs.json com o catálogo ET-EDGV 3.0/MapTopoPE."""

    fixtures = ["feature_catalogs"]

    def test_catalog_record_matches_norm(self):
        catalog = FeatureCatalog.objects.get()
        self.assertEqual(catalog.title, "ET-EDGV 3.0")
        self.assertEqual(catalog.edition, "3.0")
        self.assertEqual(catalog.edition_date, date(2018, 5, 20))
        self.assertIn("MapTopoPE", catalog.series)

    def test_all_107_classes_loaded_with_expected_counts(self):
        self.assertEqual(FeatureCatalogClass.objects.count(), 107)
        counts = {
            row["category"]: row["n"]
            for row in FeatureCatalogClass.objects.values("category").annotate(
                n=Count("id")
            )
        }
        self.assertEqual(counts, EXPECTED_CATEGORY_COUNTS)

    def test_class_names_follow_convention(self):
        self.assertTrue(
            FeatureCatalogClass.objects.filter(
                name="Trecho_Drenagem", category="hid"
            ).exists()
        )
        # nenhum nome em minúsculas puras (formato deve ser Nome_Com_Maiusculas)
        for name in FeatureCatalogClass.objects.values_list("name", flat=True):
            self.assertEqual(name, "_".join(p.capitalize() for p in name.split("_")))


class TemplateFeatureCatalogueBlockTests(SimpleTestCase):
    """Alteração 3: bloco MD_FeatureCatalogueDescription no template XML."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tree = et.parse(str(TEMPLATE_PATH))

    def find(self, old_path: str):
        return self.tree.find(old_path_to_search_string(old_path))

    def test_template_is_valid_xml_with_catalog_title(self):
        title = self.find(
            "/gmd:MD_Metadata/gmd:contentInfo[2]/gmd:MD_FeatureCatalogueDescription"
            "/gmd:featureCatalogueCitation/gmd:CI_Citation/gmd:title/gco:CharacterString"
        )
        self.assertIsNotNone(title, "bloco MD_FeatureCatalogueDescription ausente")
        self.assertEqual(title.text, "ET-EDGV 3.0")

    def test_block_has_date_edition_and_included_flag(self):
        base = (
            "/gmd:MD_Metadata/gmd:contentInfo[2]/gmd:MD_FeatureCatalogueDescription"
        )
        edition = self.find(
            base + "/gmd:featureCatalogueCitation/gmd:CI_Citation/gmd:edition/gco:CharacterString"
        )
        cit_date = self.find(
            base + "/gmd:featureCatalogueCitation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date"
        )
        included = self.find(base + "/gmd:includedWithDataset/gco:Boolean")
        self.assertEqual(edition.text, "3.0")
        self.assertEqual(cit_date.text, "2018-05-20")
        self.assertEqual(included.text, "true")


class CreateVectorFormFieldsScriptTests(TestCase):
    """Alteração 4: campo "Catálogo de feições" criado e associado só aos PTs vetoriais."""

    fixtures = ["feature_catalogs"]

    def setUp(self):
        self.script = load_script("create_vector_form_fields")
        self.pt_matricial = ProductType.objects.create(
            pk=1, name="SCN Carta Topografica Matricial", xml_template=TEMPLATE_RELATIVE
        )
        self.pt_vetorial = ProductType.objects.create(
            pk=3, name="SCN Carta Topografica Vetorial", xml_template=TEMPLATE_RELATIVE
        )
        self.pt_vetorial_sum = ProductType.objects.create(
            pk=4,
            name="SCN Carta Topografica Vetorial (sumarizada)",
            xml_template=TEMPLATE_RELATIVE,
        )

    def test_creates_combobox_with_catalog_options(self):
        field = self.script.create_catalog_field(verbose=False)
        self.assertEqual(field.label, "Catálogo de feições")
        self.assertEqual(field.field_type, "combobox")
        self.assertIn(field.field_type, MetadataFormField.field_types)
        self.assertEqual(field.possible_values, "ET-EDGV 3.0")
        self.assertEqual(field.iso_xml_path, CATALOG_ISO_PATH)

    def test_associates_only_vector_product_types(self):
        field = self.script.create_catalog_field(verbose=False)
        self.assertTrue(self.pt_vetorial.metadata_fields.filter(pk=field.pk).exists())
        self.assertTrue(
            self.pt_vetorial_sum.metadata_fields.filter(pk=field.pk).exists()
        )
        self.assertFalse(self.pt_matricial.metadata_fields.filter(pk=field.pk).exists())

    def test_is_idempotent(self):
        self.script.create_catalog_field(verbose=False)
        self.script.create_catalog_field(verbose=False)
        self.assertEqual(
            MetadataFormField.objects.filter(iso_xml_path=CATALOG_ISO_PATH).count(), 1
        )
        self.assertEqual(self.pt_vetorial.metadata_fields.count(), 1)

    def test_possible_values_refresh_when_new_catalog_is_added(self):
        self.script.create_catalog_field(verbose=False)
        FeatureCatalog.objects.create(
            title="ET-EDGV 2.1.3",
            abreviation="ET-EDGV 2.1.3",
            date=date(2010, 1, 1),
            edition="2.1.3",
            edition_date=date(2010, 1, 1),
            series="EDGV Defesa F Ter",
        )
        field = self.script.create_catalog_field(verbose=False)
        self.assertEqual(field.possible_values, "ET-EDGV 3.0, ET-EDGV 2.1.3")

    def test_raises_when_no_catalog_registered(self):
        FeatureCatalog.objects.all().delete()
        with self.assertRaises(RuntimeError):
            self.script.create_catalog_field(verbose=False)


class VectorFormFieldEndToEndTests(TestCase):
    """Alteração 5 (integração): o valor escolhido no formulário chega ao XML final."""

    fixtures = ["feature_catalogs"]

    def setUp(self):
        self.script = load_script("create_vector_form_fields")
        for pk in (3, 4):
            ProductType.objects.create(
                pk=pk, name=f"PT vetorial {pk}", xml_template=TEMPLATE_RELATIVE
            )
        self.field = self.script.create_catalog_field(verbose=False)

    def test_fill_xml_template_writes_catalog_title(self):
        pt = ProductType.objects.get(pk=3)
        tree, not_registered = fill_xml_template(
            pt, [(CATALOG_ISO_PATH, "ET-EDGV 3.0")]
        )
        self.assertEqual(not_registered, [])
        element = tree.find(old_path_to_search_string(self.field.old_path))
        self.assertIsNotNone(element)
        self.assertEqual(element.text, "ET-EDGV 3.0")


class IdentifyFeatureCatalogScriptTests(SimpleTestCase):
    """Alteração 6: decomposição <categoria>_<classe>_<geometria> do script exploratório."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.script = load_script("identify_feature_catalog")

    def test_parses_conforming_layer_names(self):
        cases = {
            "hid_trecho_drenagem_l": ("hid", "trecho_drenagem", "l"),
            "rel_curva_nivel_l": ("rel", "curva_nivel", "l"),
            "veg_veg_area_contato_a": ("veg", "veg_area_contato", "a"),
            "pto_pto_est_med_fenomenos_p": ("pto", "pto_est_med_fenomenos", "p"),
        }
        for layer, expected in cases.items():
            self.assertEqual(self.script.parse_layer(layer), expected, msg=layer)

    def test_rejects_nonconforming_layer_names(self):
        for layer in ("layer_styles", "msf100_wgs84", "hid_x", "abcd_classe_l"):
            self.assertIsNone(self.script.parse_layer(layer), msg=layer)

    def test_load_reference_parses_conference_format(self):
        sample = "hid (2):\n   trecho_drenagem\n   massa_dagua\nrel (1):\n   curva_nivel\nTOTAL: 3\n"
        with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", encoding="utf-8", delete=False
        ) as f:
            f.write(sample)
            path = Path(f.name)
        try:
            reference = self.script.load_reference(path)
        finally:
            path.unlink()
        self.assertEqual(
            reference,
            {"hid": {"trecho_drenagem", "massa_dagua"}, "rel": {"curva_nivel"}},
        )


class GenerateFixtureScriptTests(SimpleTestCase):
    """Alteração 7: formatação de nomes de classe do gerador da fixture."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.script = load_script("generate_feature_catalog_fixture")

    def test_class_name_capitalizes_each_segment(self):
        self.assertEqual(self.script.class_name("trecho_drenagem"), "Trecho_Drenagem")
        self.assertEqual(self.script.class_name("casa_de_forca"), "Casa_De_Forca")
        self.assertEqual(self.script.class_name("ilha"), "Ilha")
