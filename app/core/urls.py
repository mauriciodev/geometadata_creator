from django.urls import path, include
from rest_framework import routers
from core.views import (
    GeoresourceUploadAPIView,
    ProductTypeViewSet,
    show_csw_metadata,
    metadata_responsible_individual,
    metadata_responsible_organization,
    metadata_project,
    vertical_datum,
)
from core.fields import UniversalFields as UF


urlpatterns = []

router = routers.DefaultRouter()
router.register(r"product_types", ProductTypeViewSet)
urlpatterns.append(path("", include(router.urls)))


urlpatterns += [
    path(
        "geoproduct/",
        GeoresourceUploadAPIView.as_view(),
        name="geoproduct",
    ),
    path("show_csw_metadata", show_csw_metadata),
    path(
        f"cadastro_geral/{UF.metadata_responsible_individual.value}",
        metadata_responsible_individual.as_view(),
    ),
    path(
        f"cadastro_geral/{UF.metadata_responsible_organization.value}",
        metadata_responsible_organization.as_view(),
    ),
    path(f"cadastro_geral/{UF.metadata_project.value}", metadata_project.as_view()),
    path(f"cadastro_geral/{UF.vertical_datum.value}", vertical_datum.as_view()),
]
