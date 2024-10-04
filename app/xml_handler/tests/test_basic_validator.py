from django.test import SimpleTestCase
from xml_handler.validator import validate_file_integrity


class ValidatorTests(SimpleTestCase):

    def test_simple_validators(self):
        self.assertTrue(
            validate_file_integrity(
                "xml_handler/tests/test_data/cfad8cc1-e710-4872-a139-bb6a57c4f1a1.xml"
            )
        )
