from rest_framework import serializers
from core.models import ProductType


class GeoresourceUploadSerializer(serializers.Serializer):
    geodata_file = serializers.FileField()

    class Meta:
        fields = ("geodata_file",)


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        # fields = ('metadata_id', 'metadata_file', 'geodata_file', 'pdf_file',)
        fields = "__all__"
        depth = 1
