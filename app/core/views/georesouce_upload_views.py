from django.http import HttpRequest

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from file_handler.extractor import parse_file
from core.serializers import GeoresourceUploadSerializer
from core.models import ProductType, GeospatialResource


class GeoresourceUploadAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = GeoresourceUploadSerializer

    def post(self, request, *args, **kwargs):
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
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        georesource = GeospatialResource.objects.create(geodata_file=geodata_file)

        # Pegar os tipos de produtos
        product_type_names = [pd.name for pd in ProductType.objects.all()]

        return Response(
            {
                "file_id": georesource.id,
                "product_types": product_type_names,
                "file_fields": file_fields,
            },  # Adicionar os tipos de produto possível
            status=status.HTTP_201_CREATED,  # type: ignore
        )

    @action(detail=True, methods=["POST"], pk=None)
    def build_metadata(self, request: HttpRequest):
        fields = request.POST["fields"]

        # Validar os dados

        # Construir o XML

        # Validar o XML
