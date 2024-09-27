from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from rest_framework import viewsets

from core.serializers import ProductTypeSerializer
from core.models import ProductType


def show_csw_metadata(request):

    try:
        # question = Question.objects.get(pk=question_id)
        metadataid = "uuid"
    except Question.DoesNotExist:  # type: ignore
        raise Http404("Metadata not found.")
    context = {"metadataid": metadataid, "csw_server_url": settings.CSW_SERVER_URL}
    # return HttpResponse("You're voting on question %s." % metadataid)
    return render(request, "gmd_creator/show_csw_metadata.html", context)


class ProductTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
