from django.contrib import admin
from .models import Registro, CSVUpload

# Register your models here.
class RegistrotAdmin(admin.ModelAdmin):
    list_display = ('cidade', 'data', 'suspeitos', 'confirmados', 'descartados', 'recuperados', 'obitos')
    list_filter = ('cidade', 'data', 'suspeitos', 'confirmados', 'descartados', 'recuperados', 'obitos')
    search_fields = ['cidade', 'data']
    ordering = ['cidade', 'data']

admin.site.register(Registro, RegistrotAdmin)


class CSVUploadsAdmin(admin.ModelAdmin):
    model = CSVUpload
    list_display= ('nome',)

admin.site.register(CSVUpload, CSVUploadsAdmin)