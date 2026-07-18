 
import uuid
from django.db import models
#from django.conf import settings

class FeatureCatalog(models.Model):
    """
    Stores the Feature Catalogs that describes the classes for each product. It is used to fill the metadata with the information of the geodata file and to check if the metadata is correct.
    """

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    abreviation = models.CharField(max_length=20)
    date = models.DateField()
    edition = models.CharField(max_length=20)
    edition_date = models.DateField()
    series = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.abreviation} {self.edition}"

class FeatureCatalogClass(models.Model):
    """
    Stores the classes of the Feature Catalogs. It is used to fill the metadata with the information of the geodata file and to check if the metadata is correct.
    """

    id = models.BigAutoField(primary_key=True)
    feature_catalog = models.ForeignKey(FeatureCatalog, on_delete=models.CASCADE, related_name="classes")
    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=10,
        blank=True,
        default="",
        help_text="Layer name prefix for the class category (e.g. hid, rel, tra).",
    )
    description = models.TextField()

    def __str__(self):
        return f"{self.category} - {self.name}"
