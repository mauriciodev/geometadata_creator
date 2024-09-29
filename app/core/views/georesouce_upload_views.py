from django.http import HttpRequest

from rest_framework import status
from rest_framework.parsers import (
    FormParser,
    JSONParser,
    MultiPartParser,
)
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from file_handler.extractor import parse_file
from core.serializers import (
    GeoresourceUploadSerializer,
    XMLSerializer,
    BuildMetadataSerializer,
)
from core.models import ProductType, GeospatialResource
from core.fields import UniversalFields as UF


class GeoresourceUploadAPIView(mixins.CreateModelMixin, GenericViewSet):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]
    serializer_class = GeoresourceUploadSerializer
    queryset = GeospatialResource.objects.all()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        geodata_file = serializer.validated_data[  # type: ignore
            "geodata_file"
        ].temporary_file_path()

        # Validate the georesource file
        try:
            file_fields = parse_file(geodata_file).model_dump()
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        georesource = GeospatialResource.objects.create(geodata_file=geodata_file)

        # Pegar os tipos de produtos
        product_types = [
            {"id": pd.id, "name": pd.name} for pd in ProductType.objects.all()
        ]

        return Response(
            {
                "file_id": georesource.id,
                "product_types": product_types,
                "file_fields": file_fields,
            },  # Adicionar os tipos de produto possível
            status=status.HTTP_201_CREATED,  # type: ignore
        )

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=BuildMetadataSerializer,
        parser_classes=(JSONParser,),
    )
    def build_metadata(self, request: HttpRequest, pk=None):
        """
        Pass the metadata fields with its respective values:
            - Validate the them against the file's information;
            - Validate the contact information agaist the logged databases;
            - Create the XML metadata file;
        """
        # Validate the sent information is in the format and that the labels exists
        serializer = BuildMetadataSerializer(data=getattr(request, "data"))
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.validated_data["metadata_fields"])  # type: ignore
        recived_fields = {field["label"]: field["value"] for field in serializer.validated_data["metadata_fields"]}  # type: ignore

        # Get the field that contains the type of product
        product_type = ProductType.objects.get(
            label=next(
                iso_path
                for iso_path in recived_fields
                if iso_path == UF.product_type.value
            )
        )
        correct_fields = {pt.label for pt in product_type.metadata_fields.all()}

        # Check if the fields sent are correct
        error_fields = {}
        error_fields.update(
            {
                label: "Fields missing but was expected."
                for label in correct_fields
                if label not in recived_fields.keys()
            }
        )
        error_fields.update(
            {
                label: "Field does not belong to this product type."
                for label in recived_fields.keys()
                if label not in correct_fields
            }
        )
        if len(error_fields) > 0:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Check for the file related fields

        # Check for the cadastro geral fields

        return Response({}, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=XMLSerializer,
        parser_classes=(MultiPartParser, FormParser),
    )
    def send_xml_metadata(self, request: HttpRequest, id=None):
        return Response({}, status=status.HTTP_201_CREATED)
