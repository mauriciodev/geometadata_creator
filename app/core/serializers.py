from rest_framework import serializers
from core.models import ProductType, GeospatialResource


class GeoresourceUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeospatialResource
        fields = ("geodata_file",)
        depth = 1


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"
        depth = 1
