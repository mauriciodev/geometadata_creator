from rest_framework import serializers
from core.models import ProductType, GeospatialResource, MetadataFormField


class CadastroGeralSerializer(serializers.Serializer):
    metadata_fields = serializers.ListSerializer(child=serializers.CharField())


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


class MetadataFieldSerializer(serializers.ModelSerializer):
    value = serializers.JSONField()

    class Meta:
        model = MetadataFormField
        fields = ("iso_xml_path", "value")


class BuildMetadataSerializer(serializers.Serializer):
    metadata_fields = MetadataFieldSerializer(many=True)
    product_type = serializers.IntegerField()


class SendXMLSerializer(serializers.ModelSerializer):
    metadata_file = serializers.FileField()
    product_type = serializers.StringRelatedField()

    class Meta:
        model = GeospatialResource
        fields = ("metadata_file", "product_type")
