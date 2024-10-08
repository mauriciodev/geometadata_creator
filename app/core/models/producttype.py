from django.db import models
from owslib.etree import etree
from owslib.namespaces import Namespaces


class MetadataFormField(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=100, blank=True)
    iso_xml_path = models.CharField(max_length=200, blank=True)
    field_types = {
        "list": "list",
        "combobox": "combobox",
        "date": "date",
        "text": "text",
    }
    field_type = models.CharField(max_length=100, choices=field_types)
    is_static = models.BooleanField(default=False)
    possible_values = models.TextField()
    default_value = models.TextField()
    comments = models.TextField(blank=True)
    old_path = models.TextField(blank=True)

    def __str__(self):
        return f"{self.label}: {self.iso_xml_path}"


class ProductType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    metadata_fields = models.ManyToManyField(MetadataFormField)
    xml_template = models.FileField(
        "Geospatial metadata XML template.",
        null=True,
        upload_to="repository/xml_templates",
    )

    def __str__(self):
        return self.name

    def rewrite_xml_as_template(self):
        """This method replaces the current XML template with a version that has django template tags inside it."""
        namespaces = Namespaces().get_namespaces(keys=("gmd", "gco"))
        with self.xml_template.open("r") as f:
            s = f.read()
        xml_root = etree.fromstring(s.encode("utf8"))
        # md = MD_Metadata(xml_root)
        # mdelem = xml_root.find('.//' + util.nspath_eval(
        #    'gmd:MD_Metadata', namespaces))

        for form_field in self.metadata_fields.all():
            print(form_field.iso_xml_path, form_field.old_path)
            # xml_root.findall(".//gmd:MD_Metadata", namespaces)

            # use old_path to get the metadata element in the right position
            # replace the content with iso_xml_path
