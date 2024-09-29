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


class MetadataFieldSerializer(serializers.ModelSerializer):
    value = serializers.JSONField()

    class Meta:
        model = MetadataFormField
        fields = ("label", "value")

    def validate(self, attrs):
        """Validate that the labels are in the table"""
        label = attrs["label"]
        if not ProductType.objects.filter(name=label).exists():
            serializers.ValidationError(
                f"'{label}' is not registreered as a valid product type."
            )
        return super().validate(attrs)


class BuildMetadataSerializer(serializers.Serializer):
    metadata_fields = MetadataFieldSerializer(many=True)


class XMLSerializer(serializers.Serializer):
    xml_metadata_file = serializers.FileField()
