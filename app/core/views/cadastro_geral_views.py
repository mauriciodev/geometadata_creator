from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from core.serializers import CadastroGeralSerializer


class metadata_responsible_individual(GenericAPIView):
    """
    Can be accessed read only.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CadastroGeralSerializer

    def get(self, request, format=None):
        # Entrada: "MD_Metadata-contact-individualName": "Han Solo",
        response = [
            {
                "MD_Metadata-contact-individualName": "Han Solo",
                "MD_Metadata-contact-positionName": "Chefe de Subdivisão Técnica",
                "MD_Metadata-contact-organisationName": "1º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.1cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            },
            {
                "MD_Metadata-contact-individualName": "Meo Two",
                "MD_Metadata-contact-positionName": "Chefe de Subdivisão Técnica",
                "MD_Metadata-contact-organisationName": "2º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.1cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            },
            {
                "MD_Metadata-contact-individualName": "Naruto Uzumaki",
                "MD_Metadata-contact-positionName": "Chefe de Subdivisão Técnica",
                "MD_Metadata-contact-organisationName": "3º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.1cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            },
            {
                "MD_Metadata-contact-individualName": "Michael Jordan",
                "MD_Metadata-contact-positionName": "Chefe de Subdivisão Técnica",
                "MD_Metadata-contact-organisationName": "4º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.1cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            },
            {
                "MD_Metadata-contact-individualName": "Vinícius Junior",
                "MD_Metadata-contact-positionName": "Chefe de Subdivisão Técnica",
                "MD_Metadata-contact-organisationName": "5º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.1cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            },
        ]
        return Response(response)


class metadata_responsible_organization(GenericAPIView):
    """
    Can be accessed read only.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CadastroGeralSerializer

    def get(self, request, format=None):
        # Entrada: "MD_Metadata-contact-organisationName": "1º Centro de Geoinformação",
        response = {
            "1": {
                "MD_Metadata-contact-organisationName": "1º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.1cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            },
            "2": {
                "MD_Metadata-contact-organisationName": "2º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.2cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            },
            "3": {
                "MD_Metadata-contact-organisationName": "3º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.3cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            },
            "4": {
                "MD_Metadata-contact-organisationName": "4º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.4cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            },
            "5": {
                "MD_Metadata-contact-organisationName": "5º Centro de Geoinformação",
                "MD_Metadata-contact-contactInfo-onlineResource-linkage": "http://www.5cgeo.eb.mil.br/",
                "MD_Metadata-contact-role": "owner",
            },
        }
        return Response(response)


class metadata_project(GenericAPIView):
    """
    Can be accessed read only.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CadastroGeralSerializer

    def get(self, request, format=None):
        # Entrada:
        response = {
            "1": {
                "MD_Identification-citation-collectiveTitle": "Radiografia da Amazônia",
            },
            "2": {
                "MD_Identification-citation-collectiveTitle": "Viagem ao centro da Terra",
            },
            "3": {
                "MD_Identification-citation-collectiveTitle": "Projeto X",
            },
        }
        return Response(response)


class vertical_datum(GenericAPIView):
    """
    Can be accessed read only.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CadastroGeralSerializer

    def get(self, request, format=None):
        # Não tem entrada
        response = {
            "1": {
                "MD_DataIdentification-extent-verticalExtent-verticalDatum": "Datum de Imbituba - SC",
            }
        }
        return Response(response)
