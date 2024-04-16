from rest_framework import serializers
from .models import UploadedFile, GeospatialResource

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file', 'uploaded_on',)

class GeoresourceUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeospatialResource
        fields = ('metadata_id', 'metadata_file', 'geodata_file', 'pdf_file',)