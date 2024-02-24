from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import geospatial_resource

admin.site.register(geospatial_resource, SimpleHistoryAdmin)
