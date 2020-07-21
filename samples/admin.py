from django.contrib.gis import admin
from import_export import resources

# Register your models here.
from .models import Sample

class SampleResource(resources.ModelResource):
    class Meta:
        model = Sample

class SampleAdmin(admin.ModelAdmin):
    list_display = ["__str__", "sample_no"]

    class Meta:
        model = Sample

admin.site.register(Sample, admin.OSMGeoAdmin)