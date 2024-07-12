from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
from django.conf import settings

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import authentication, permissions, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import GeoresourceUploadSerializer, ProductTypeSerializer
from .models import ProductType
from osgeo import gdal,ogr, osr
import rasterio
# Create your views here.


def show_csw_metadata(request):

    try:
        #question = Question.objects.get(pk=question_id)
        metadataid = 'uuid'
    except Question.DoesNotExist:
        raise Http404("Metadata not found.")
    context = {"metadataid": metadataid,
               "csw_server_url": settings.CSW_SERVER_URL
               }
    #return HttpResponse("You're voting on question %s." % metadataid)
    return render(request, "gmd_creator/show_csw_metadata.html", context)

class hello_world(APIView):
    """
    Can be accessed read only.
    """
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        response= {
            "gmd:distributionFormat gmd:name gco:CharacterString": "Shape File",
        }
        return Response(response)

class GeoresourceUploadAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = GeoresourceUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            metadata_response = {}
            
            # if georesource was uploaded, extract geoinfo with gdal/ogr
            geodata_file = serializer.validated_data["geodata_file"].temporary_file_path()
            with rasterio.open(geodata_file) as img_ds:
                metadata_response['gmd:MD_ReferenceSystem gmd:referenceSystemIdentifier gmd:code gco:CharacterString'] = str(img_ds.crs)
                img_ds.bounds #metadata
                img_ds.driver #metadata
                img_ds.dtypes #metadata
                img_ds.get_transform()[1] #metadata (resolution x)
                img_ds.get_transform()[5] #metadata (resolution y)
                #metadata : test if it's vector or raster
            
            # if metadata XML was uploaded, return it's content
            # if pdf was uploaded, return the URL

            """Trazer: 
                Formato do arquivo
        gmd:distributionFormat gmd:name gco:CharacterString
    Extensão espacial (min x, min y, max x, max y)
        gmd:MD_DataIdentification gmd:northBoundLatitude gco:Decimal
        gmd:MD_DataIdentification gmd:westBoundLongitude gco:Decimal
        gmd:MD_DataIdentification gmd:southBoundLatitude gco:Decimal
        gmd:MD_DataIdentification gmd:eastBoundLongitude gco:Decimal
    Tipo de representação espacial (Matricial/Vetorial)
        gmd:MD_DataIdentification gmd:spatialRepresentationType gco:CharacterString
    Palavras-chave
        gmd:MD_DataIdentification gmd:descriptiveKeywords gmd:keyword gco:CharacterString
    Sistema de referência (EPSG, descrição, DATUM)
        Código epsg: gmd:MD_ReferenceSystem gmd:referenceSystemIdentifier gmd:code gco:CharacterString
        Autoridade: gmd:MD_ReferenceSystem gmd:referenceSystemIdentifier gmd:authority gco:CharacterString
        Datum vertical: gmd:MD_DataIdentification gmd:verticalExtent gmd:verticalDatum gco:CharacterString
    Resolução espacial X e Y
        row: gmd:spatialRepresentationInfo MD_Georectified gmd:axisDimensionProperties gmd:dimensionName gco:CharacterString
        Resolução da row: gmd:spatialRepresentationInfo MD_Georectified gmd:axisDimensionProperties gmd:resolution gco:Decimal
        column: gmd:spatialRepresentationInfo MD_Georectified gmd:axisDimensionProperties gmd:dimensionName gco:CharacterString
        Resolução da column: gmd:spatialRepresentationInfo MD_Georectified gmd:axisDimensionProperties gmd:resolution gco:Decimal
    Quantidade de bits
    Escala (opcional)
        gmd:MD_DataIdentification gmd:spatialResolution gmd:denominator gco:Integer"""
            serializer.save()
            return Response(
                serializer.data | metadata_response,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer