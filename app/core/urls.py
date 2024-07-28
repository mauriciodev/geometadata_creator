from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets
from core.views import show_csw_metadata, hello_world, metadata_responsible_individual
from core.models import GeospatialResource
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import GeoresourceUploadAPIView, ProductTypeViewSet


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
router.register(r"product_type_form", ProductTypeViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("show_csw_metadata", show_csw_metadata),
    path("hello_world", hello_world.as_view()),
    path("", include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path(
        "upload-georesource/",
        GeoresourceUploadAPIView.as_view(),
        name="upload-georesource",
    ),
    path(
        "metadata_responsible_individual/", 
        metadata_responsible_individual.as_view(),
        name="metadata_responsible_individual"
    ),

]
