from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import Job
# Register your models here.


class JobAdmin(GuardedModelAdmin):
    list_display = ["__str__", "job_no", "job_name"]


admin.site.register(Job, JobAdmin)
