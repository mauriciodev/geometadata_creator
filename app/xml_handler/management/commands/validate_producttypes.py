from django.core.management.base import BaseCommand
from xml_handler.validator import collect_fields
from core.models import ProductType
from lxml import etree as et
from enum import Enum


class ProductTypeValidationOptions(Enum):
    case_1 = "Product Type Template is Valid."
    case_2 = "Product Type Template has errors."
    case_3 = "Product Type Doesn't have template."


class Command(BaseCommand):
    help = """
    If you need Arguments, please check other modules in 
    django/core/management/commands.
    """

    def handle(self, **options):
        results = self.validate_product_types_templates()
        self.print_results(results)

    def validate_product_types_templates(self):
        results = {}
        for product_type in ProductType.objects.all():
            if str(product_type.xml_template) != "":
                tree = et.parse(product_type.xml_template)
                _, missing_fields = collect_fields(tree, product_type)
                if len(missing_fields) == 0:
                    results[product_type] = (
                        ProductTypeValidationOptions.case_1,
                        missing_fields,
                    )
                else:
                    results[product_type] = (
                        ProductTypeValidationOptions.case_2,
                        missing_fields,
                    )
            else:
                results[product_type] = (ProductTypeValidationOptions.case_3, {})
        return results

    def print_results(self, missing_fields: dict):
        for pt, (sc, fields) in missing_fields.items():
            match sc:
                case ProductTypeValidationOptions.case_1:
                    print(f"- {pt}: {sc.value}")
                case ProductTypeValidationOptions.case_2:
                    print(f"- {pt}: {sc.value}")
                    for field, message in fields.items():
                        print("     " + f"{field}: {message.value};")
                case ProductTypeValidationOptions.case_3:
                    print(f"- {pt}: {sc.value}")
