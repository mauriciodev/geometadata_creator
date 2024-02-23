# urls.py
from django.urls import path
from gmd_creator_app.views import show_csw_metadata

urlpatterns = [
    path("show_csw_metadata", show_csw_metadata),
]
