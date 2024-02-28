from django.contrib import admin, messages
from simple_history.admin import SimpleHistoryAdmin
from .models import geospatial_resource




class geospatial_resource_Admin(SimpleHistoryAdmin):
    def has_metadata(self, obj):
        return True if obj.metadata_file else False
    has_metadata.boolean = True

    def has_geodata(self, obj):
        return True if obj.geodata_file else False
    has_geodata.boolean = True

    def has_pdf(self, obj):
        return True if obj.pdf_file else False
    has_pdf.boolean = True

    @admin.action(description="Publish selected resources on CSW.")
    def authorize_publish_csw(self, request, queryset):
        published_count = 0
        to_publish_count = queryset.count()
        for obj in queryset:
            if obj.csw_insert():
                obj.published_on_csw = True
            published_count += 1
        self.message_user(request,f"{published_count} of {to_publish_count} products published.", messages.SUCCESS)


    @admin.action(description="Unpublish selected resources on CSW.")
    def unpublish_csw(self, request, queryset):
        published_count = 0
        to_publish_count = queryset.count()
        for obj in queryset:
            if obj.csw_insert():
                obj.published_on_csw = False
            published_count += 1
        self.message_user(request,f"{published_count} of {to_publish_count} products unpublished.", messages.SUCCESS)

    list_display = ["metadata_id", "title", 'has_metadata', 'has_geodata', 'has_pdf', 'published_on_csw']
    ordering = ["title"]
    actions = [authorize_publish_csw, unpublish_csw]
    #filter_vertical
    list_filter = ['published_on_csw',
                   ("metadata_file", admin.EmptyFieldListFilter),
                   ("geodata_file", admin.EmptyFieldListFilter),
                   ("pdf_file", admin.EmptyFieldListFilter),
    ]
    search_fields = ["metadata_id","title"]

admin.site.register(geospatial_resource, geospatial_resource_Admin)

