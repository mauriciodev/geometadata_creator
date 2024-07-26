from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=100, blank=True)
    metadata_fields = models.ManyToManyField("MetadataFormField")

    def __str__(self):
        return self.name


class MetadataFormField(models.Model):
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
    default_value = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)
    old_path = models.TextField(blank=True)

    def __str__(self):
        return f"{self.label}: {self.iso_xml_path}" 
