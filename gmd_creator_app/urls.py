# urls.py
from django.urls import path, include
from django.conf import settings
from rest_framework import routers, serializers, viewsets
from gmd_creator_app.views import show_csw_metadata
from gmd_creator_app.models import geospatial_resource


# Serializers define the API representation.
class geospatial_resource_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = geospatial_resource
        fields = ['metadata_id', 'title', 'published_on_csw']

# ViewSets define the view behavior.
class geospatial_resource_ViewSet(viewsets.ModelViewSet):
    queryset = geospatial_resource.objects.all()
    serializer_class = geospatial_resource_Serializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'georesources', geospatial_resource_ViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("show_csw_metadata", show_csw_metadata),
    path('', include(router.urls)),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
