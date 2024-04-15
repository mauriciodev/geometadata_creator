# urls.py
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets
from gmd_creator_app.views import show_csw_metadata, hello_world
from gmd_creator_app.models import GeospatialResource
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import FileUploadAPIView


# Serializers define the API representation.
class geospatial_resource_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeospatialResource
        fields = ["metadata_id", "title", "published_on_csw"]


# ViewSets define the view behavior.
class geospatial_resource_ViewSet(viewsets.ModelViewSet):
    queryset = GeospatialResource.objects.all()
    serializer_class = geospatial_resource_Serializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"georesources", geospatial_resource_ViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("show_csw_metadata", show_csw_metadata),
    path("hello_world", hello_world.as_view()),
    path("", include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path("upload-file/", FileUploadAPIView.as_view(), name="upload-file"),
]
