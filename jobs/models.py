from django.db import models

# Create your models here.


class Job(models.Model):
    job_no = models.CharField(verbose_name="Job #", max_length=120, unique=True)
    job_name = models.CharField(verbose_name="Job Name", max_length=120)

    class Meta:
        permissions = (
            ('view_this_job', 'View Job In Website'),
        )