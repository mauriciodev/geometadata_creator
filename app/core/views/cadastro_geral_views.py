from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
