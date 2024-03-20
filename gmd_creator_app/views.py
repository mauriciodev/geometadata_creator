from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
from django.conf import settings

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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
