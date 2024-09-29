from rest_framework import serializers
from core.models import ProductType, GeospatialResource, MetadataFormField


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


class MetadataFieldsSerializer(serializers.ModelSerializer):
    value = serializers.Field()

    class Meta:
        model = MetadataFormField
        fields = ("label", "value")


class XMLSerializer(serializers.Serializer):
    xml_metadata_file = serializers.FileField()
