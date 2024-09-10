from django.shortcuts import render
from django.http import Http404
from django.conf import settings

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import GeoresourceUploadSerializer, ProductTypeSerializer
from .models import ProductType
from file_handler.extractor import parse_file

# Create your views here.


def show_csw_metadata(request):

    try:
        # question = Question.objects.get(pk=question_id)
        metadataid = "uuid"
    except Question.DoesNotExist:  # type: ignore
        raise Http404("Metadata not found.")
    context = {"metadataid": metadataid, "csw_server_url": settings.CSW_SERVER_URL}
    # return HttpResponse("You're voting on question %s." % metadataid)
    return render(request, "gmd_creator/show_csw_metadata.html", context)


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
        try:
            metadata_response = parse_file(geodata_file).model_dump()
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        metadata_response["MD_Metadata-fileIdentifier"] = serializer.data["metadata_id"]  # type: ignore

        return Response(
            {"serializer_data": serializer.data, "metadata": metadata_response},
            status=status.HTTP_201_CREATED,  # type: ignore
        )


class ProductTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class metadata_responsible_individual(APIView):
    """
    Can be accessed read only.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        # Entrada: "MD_Metadata-contact-individualName": "Han Solo",
        response = {
            "1": {
                "MD_Metadata-contact-individualName": "Han Solo",
                "MD_Metadata-contact-positionName": "Chefe de Subdivisão Técnica",
                "MD_Metadata-contact-organisationName": "1º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.1cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            }
        }
        return Response(response)


class metadata_responsible_organization(APIView):
    """
    Can be accessed read only.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        # Entrada: "MD_Metadata-contact-organisationName": "1º Centro de Geoinformação",
        response = {
            "1": {
                "MD_Metadata-contact-organisationName": "1º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.1cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            }
        }
        return Response(response)


class metadata_project(APIView):
    """
    Can be accessed read only.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        # Entrada:
        response = {
            "1": {
                "MD_Identification-citation-collectiveTitle": "Radiografia da Amazônia",
            }
        }
        return Response(response)


class vertical_datum(APIView):
    """
    Can be accessed read only.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        # Não tem entrada
        response = {
            "1": {
                "MD_DataIdentification-extent-verticalExtent-verticalDatum": "Datum de Imbituba - SC",
            }
        }
        return Response(response)
