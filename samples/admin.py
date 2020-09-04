from django.contrib.gis import admin
from import_export import resources, fields

# Register your models here.
from import_export.widgets import ForeignKeyWidget

from jobs.models import Job
from .models import Sample

class JobWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        """https://github.com/django-import-export/django-import-export/issues/1157"""
        if not value:
            return None
        else:
            obj, _ = Job.objects.update_or_create(
                # pk=value,
                job_no=value,
                defaults={
                    'job_no': row.get('job_no'),
                    # 'job_name': row.get('job_name'),
                }
            )
        return obj


class SampleResource(resources.ModelResource):
    job_no = fields.Field(
        column_name='job_no',
        attribute='job_no',
        widget=JobWidget(Job, 'job_no')
    )
    class Meta:
        model = Sample
        import_id_fields = ["sample_no"]

        fields = ('sample_no',
                  'job_no',
                  'job_name',
                  'latitude',
                  'longitude',
                  'altitude',
                  'depth',
                  'soil_type',
                  'texture',
                  'color',
                  'ph',
                  'redox_potential',
                  'conductivity',
                  'chloride',
                  'sulfate',
                  'salinity',
                  'resistivity_as_collected',
                  'resistivity_saturated',
                  'field_resistivity',
                  'carbonate',
                  'sulfide',
                  'moisture_content',
                  'comments',)

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
