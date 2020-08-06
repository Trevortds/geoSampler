from django.contrib.gis import admin
from import_export import resources

# Register your models here.
from .models import Sample


class SampleResource(resources.ModelResource):
    class Meta:
        model = Sample
        import_id_fields = ["sample_no"]


class SampleAdmin(admin.ModelAdmin):
    list_display = ["__str__", "sample_no"]
    search_fields = ["sample_no", "job_name"]
    class Meta:
        model = Sample


class SampleGeoAdmin(admin.OSMGeoAdmin):
    list_display = ["__str__", "sample_no"]

    class Meta:
        model = Sample


admin.site.register(Sample, SampleGeoAdmin)
