from rest_framework import serializers
from .models import GeospatialResource, ProductType, MetadataFormField


class GeoresourceUploadSerializer(serializers.Serializer):
    geodata_file = serializers.FileField()

    class Meta:
        model = GeospatialResource
        fields = ("geodata_file",)


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        # fields = ('metadata_id', 'metadata_file', 'geodata_file', 'pdf_file',)
        fields = "__all__"
        depth = 1


class MetadataFormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataFormField
        fields = "__all__"
