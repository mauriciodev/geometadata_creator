from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets
from core.views import (
    show_csw_metadata,
    metadata_responsible_individual,
    metadata_responsible_organization,
    metadata_project,
)
from core.models import GeospatialResource
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import GeoresourceUploadAPIView, ProductTypeViewSet, vertical_datum


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
# router.register(r"metadata_project", metadata_responsible_organization.as_view())


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("show_csw_metadata", show_csw_metadata),
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
        name="metadata_responsible_individual",
    ),
    path(
        "metadata_responsible_organization/",
        metadata_responsible_organization.as_view(),
        name="metadata_responsible_organization",
    ),
    path(
        "metadata_project",
        metadata_project.as_view(),
        name="metadata_project",
    ),
    path(
        "vertical_datum",
        vertical_datum.as_view(),
        name="vertical_datum",
    ),
]
