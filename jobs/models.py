from django.db import models

# Create your models here.


class Job(models.Model):
    job_no = models.CharField(verbose_name="Job #", max_length=120, unique=True)
    job_name = models.CharField(verbose_name="Job Name", max_length=120, blank=True)

    class Meta:
        permissions = (
            ('view_this_job', 'View Job In Website'),
        )

    def __str__(self):
        return f"{self.job_name} - {self.job_no}" if self.job_name else f"{self.job_no}"