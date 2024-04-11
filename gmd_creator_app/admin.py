import requests, os

from django.contrib import admin, messages
from django.contrib.auth import get_permission_codename
from django.core.files.base import ContentFile, File
from simple_history.admin import SimpleHistoryAdmin
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.conf import settings

from django.core.files import File
from owslib import csw

from .models import GeospatialResource

class geospatial_resource_Admin(ExtraButtonsMixin, SimpleHistoryAdmin):
    def has_metadata(self, obj):
        return True if obj.metadata_file else False
    has_metadata.boolean = True

    def has_geodata(self, obj):
        return True if obj.geodata_file else False
    has_geodata.boolean = True

    def has_pdf(self, obj):
        return True if obj.pdf_file else False
    has_pdf.boolean = True

    #@admin.action(description="Get examples of free geodata from BDGEx's CSW.")
    @button(#permission='demo.add_demomodel1',
            #change_form=True,
            #html_attrs={'style': 'background-color:#88FF88;color:black'}
            )
    def get_examples(self, request):#, queryset):
        
        cswClient = csw.CatalogueServiceWeb('http://bdgex.eb.mil.br/csw')
        metadataids = ['ce253e42-c7e7-11df-94c5-00270e07db9f','a5569dda-c7e7-11df-819e-00270e07db9f', '7b22c2aa-c7e7-11df-b1f5-00270e07db9f']
        outputschema = 'http://www.isotc211.org/2005/gmd'
        cswClient.getrecordbyid(id=metadataids, outputschema=outputschema)
        
        #BDGEx anonymous login
        session = requests.Session()
        session.post('https://bdgex.eb.mil.br/mediador/?modulo=Login&acao=VisitanteExterno')
        done = 0
        for rec in cswClient.records:
            metadata = cswClient.records[rec]
            
            new_resource = GeospatialResource()
            new_resource.title = metadata.identification[0].title
            new_resource.metadata_id = metadata.identifier

            xml_file_name = os.path.join(settings.MEDIA_ROOT, 'repository', f"{new_resource.metadata_id}.xml")
            tif_file_name = os.path.join(settings.MEDIA_ROOT, 'repository', f"{new_resource.metadata_id}.tif")
            pdf_file_name = os.path.join(settings.MEDIA_ROOT, 'repository', f"{new_resource.metadata_id}.pdf")
            
            
            new_resource.metadata_file.save(xml_file_name, ContentFile(metadata.xml.decode('UTF-8')))
            """with open(xml_file_name, "w") as f:
                xmlfile = File(f)
                xmlfile.write(metadata.xml.decode('UTF-8'))
            
            with open(xml_file_name, "r") as f:
                xmlfile = File(f)
                new_resource.metadata_file = xmlfile"""
            
            file_url = f'https://bdgex.eb.mil.br/mediador/index.php?modulo=download&acao=baixar&identificador={new_resource.metadata_id}'
            pdf_url = f"https://bdgex.eb.mil.br/mediador/index.php?modulo=download&acao=baixarpdf&identificador={new_resource.metadata_id}"
            
            resp = session.get(file_url, stream=True)
            if resp.status_code == 200:
                with open(tif_file_name, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk: f.write(chunk)
                            
            resp = session.get(pdf_url, stream=True)
            if resp.status_code == 200:
                with open(tif_file_name, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk: f.write(chunk)
            
            try:
                new_resource.save()
                done += 1
            except:
                pass
        return HttpResponseRedirectToReferrer(request)

    @admin.action(description="Publish selected resources on CSW.", permissions=["publish"])
    def authorize_publish_csw(self, request, queryset):
        published_count = 0
        to_publish_count = queryset.count()
        for obj in queryset:
            if obj.csw_insert():
                obj.published_on_csw = True
            published_count += 1
        self.message_user(request,f"{published_count} of {to_publish_count} products published.", messages.SUCCESS)


    @admin.action(description="Unpublish selected resources on CSW.", permissions=["publish"])
    def unpublish_csw(self, request, queryset):
        published_count = 0
        to_publish_count = queryset.count()
        for obj in queryset:
            if obj.csw_insert():
                obj.published_on_csw = False
            published_count += 1
        self.message_user(request,f"{published_count} of {to_publish_count} products unpublished.", messages.SUCCESS)

    def has_publish_permission(self, request):
        """Does the user have the publish permission?"""
        opts = self.opts
        codename = get_permission_codename("publish", opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

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

admin.site.register(GeospatialResource, geospatial_resource_Admin)

