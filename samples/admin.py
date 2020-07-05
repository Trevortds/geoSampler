from django.contrib import admin

# Register your models here.
from .models import Sample


class SampleAdmin(admin.ModelAdmin):
    list_display = ["__str__", "sample_no"]

    class Meta:
        model = Sample

admin.site.register(Sample, SampleAdmin)