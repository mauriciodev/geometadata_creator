from django.core.files.base import ContentFile
from django.http import HttpRequest

from rest_framework import status
from rest_framework.parsers import (
    FormParser,
    JSONParser,
    MultiPartParser,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.files import File

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from xml_handler.constructor import fill_xml_template
from file_handler.extractor import parse_file
from core.serializers import (
    GeoresourceUploadSerializer,
    SendXMLSerializer,
    BuildMetadataSerializer,
)
from core.models import ProductType, GeospatialResource
from tempfile import NamedTemporaryFile
from lxml import etree as et
from file_handler.extractor import parse_file
from xml_handler.validator import (
    validate_file_integrity,
    find_product_type_from_xml,
    validate_fields_based_on_product_type,
)
from core.fields import FileGeoDataFields as FEF


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
            file_fields = parse_file(geodata_file).dump_fields()
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
        # Find the geodata_file that is beeing patched
        geodata_file = GeospatialResource.objects.get(pk=pk)
        if geodata_file is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Validate the sent information is in the format and that the labels exists
        serializer = BuildMetadataSerializer(data=getattr(request, "data"))
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        recived_fields = [(field["label"], field["value"]) for field in serializer.validated_data["metadata_fields"]]  # type: ignore

        # Get the product type
        pt_id = int(serializer.validated_data["product_type"])  # type: ignore
        product_type = ProductType.objects.get(pk=pt_id)
        if product_type is None:
            return Response(
                {"error": "Product type not suported"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get build the xml file
        result_tree, fields_not_in_template, fields_not_registered = fill_xml_template(
            et.parse(str(product_type.xml_template)), recived_fields
        )

        with NamedTemporaryFile(suffix=".xml", delete=False) as temp_file:
            result_tree.write(
                temp_file, pretty_print=True, xml_declaration=True, encoding="UTF-8"
            )
            temp_file.seek(0)
            geodata_file.metadata_file.save(
                "temp_name.xml", File(temp_file)
            )  # TODO: get a real file name

        return Response({}, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=SendXMLSerializer,
        parser_classes=(MultiPartParser, FormParser),
    )
    def send_xml_metadata(self, request: HttpRequest, pk=None):
        """Endpoint para construção e validação do XML a partir dos dados do arquivo"""

        # Find the geodata_file that is beeing patched
        geodata_file = GeospatialResource.objects.get(pk=pk)
        if geodata_file is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if the request is in the correct format
        serializer = SendXMLSerializer(
            geodata_file, data=getattr(request, "data"), partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        xml_file = serializer.validated_data["metadata_file"]  # type: ignore

        # Check the file integrity and save the file
        try:
            xml_tree = validate_file_integrity(xml_file)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Finds the product_type based on the xml field
        try:
            product_type = find_product_type_from_xml(xml_tree)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Get the fields from the file
        collected_fields, missing_fields = validate_fields_based_on_product_type(
            xml_tree, product_type
        )

        # TODO: Adicionar validação com dados do arquivo

        return Response(
            {"missing_fields": missing_fields},
            status=status.HTTP_201_CREATED,
        )
