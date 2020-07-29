import decimal

from django.contrib.gis.db import models

# Create your models here.
from django.contrib.gis.geos import Point
from django.core.validators import MinValueValidator
from django.db.models import F
from django.db.models.signals import pre_save

SOIL_TYPE_CHOICES = (
    ('clay_blue_gray', 'Clay (blue-gray)'),
    ('clay_stone', 'Clay/Stone'),
    ('clay', 'Clay'),
    ('silt', 'Silt'),
    ('sand', 'Sand')
)


# TODO make color and texture searchable like text.


PRES_ABS_CHOICES = (
    ('present', 'Present'),
    ('absent', 'Absent'),
)

# TODO round inputs with wrong precision, don't throw errors

#
# class SampleManager(models.Manager):
#     # idea from https://stackoverflow.com/questions/17682567/how-to-add-a-calculated-field-to-a-django-model
#     def get_queryset(self):
#         """ Overrides models.Manager method """
#         qs = super(SampleManager, self).get_queryset().annotate(awwa=F('get_awwa_rating'))

class Sample(models.Model):
    sample_no = models.CharField(max_length=120, unique=True)
    job_no = models.CharField(max_length=120)
    job_name = models.CharField(max_length=120)
    latitude = models.DecimalField(decimal_places=9, max_digits=20)
    longitude = models.DecimalField(decimal_places=9, max_digits=20)
    depth = models.DecimalField(verbose_name="Depth (feet)", decimal_places=2, max_digits=5)
    soil_type = models.CharField(max_length=32, choices=SOIL_TYPE_CHOICES)
    texture = models.CharField(max_length=32)
    color = models.CharField(max_length=32)
    ph = models.DecimalField(verbose_name="pH", decimal_places=2, max_digits=10)
    redox_potential = models.DecimalField(decimal_places=2, max_digits=10)
    conductivity = models.DecimalField(decimal_places=3, max_digits=10)
    chloride = models.DecimalField(decimal_places=2, max_digits=10)
    sulfate = models.DecimalField(decimal_places=1, max_digits=10)
    salinity = models.DecimalField(decimal_places=2, max_digits=10)
    resistivity_as_collected = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(
        decimal.Decimal('0.001'))])
    resistivity_saturated = models.DecimalField(decimal_places=2, max_digits=10)
    carbonate = models.CharField(max_length=32, choices=PRES_ABS_CHOICES)
    sulfide = models.CharField(max_length=32, choices=PRES_ABS_CHOICES)
    moisture_content = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    awwa = models.CharField(max_length=32, blank=True, null=True)

    # mpoly = models.MultiPolygonField()
    point = models.PointField(blank=True, null=True)

    # objects = SampleManager()

    def __str__(self):
        return self.sample_no + " " + self.job_name

    def get_point(self):
        return Point(float(self.latitude), float(self.longitude))

    @property
    def get_awwa_rating(self):
        # =IF(H8>9.9,"Severe",IF(H8>1,"Moderate",IF(H8>=0,"Mild",IF(H8>-1,"Type in Results"))))
        print(self.ph)
        print(self.get_redox())
        print(self.get_resistivity_simplified())
        print(self.get_sulfide_simplified())
        print(self.sulfide)
        score = decimal.Decimal(self.ph) + decimal.Decimal(self.get_redox()) + \
                decimal.Decimal(self.get_resistivity_simplified()) + decimal.Decimal(self.get_sulfide_simplified())

        if score > 9.9:
            return "Severe"
        elif score > 1:
            return "Moderate"
        elif score > 0:
            return "Mild"
        else:
            return "Type In results"

    def get_redox(self):
        # =IF($Results.K10>100.1,"0",IF($Results.K10>50,"3.5",IF($Results.K10>0,"4",IF($Results.K10<0,"5",IF($Results.K10>-1000,"Type in Results")))))
        if self.redox_potential > 100.1:
            return 0
        elif self.redox_potential > 50:
            return 3.5
        elif self.redox_potential > 0:
            return 4
        elif self.redox_potential <= 0:
            return 5
        elif self.redox_potential > -1000:
            return "Type In Results"

    def get_resistivity_simplified(self):
        # =IF($Results.P8>3, "0", IF($Results.P8>2.5, "1", IF($Results.P8>2.1, "2", IF($Results.P8>1.8, "5", IF($Results.P8>=1.5, "8",IF($Results.P8>0, "10",IF($Results.P8>-1, "Type in Results",“Error”))))))))))))))
        if self.resistivity_as_collected > 3:
            return 0
        elif self.resistivity_as_collected > 2.5:
            return 1
        elif self.resistivity_as_collected > 2.1:
            return 2
        elif self.resistivity_as_collected > 1.8:
            return 5
        elif self.resistivity_as_collected > 1.5:
            return 8
        elif self.resistivity_as_collected > 0:
            return 10
        elif self.resistivity_as_collected > -1:
            return "Type In Result"

    def get_sulfide_simplified(self):
        # =IF($Results.S8="Present",3.5,IF($Results.S8="Trace",2,IF($Results.S8="Absent",0,IF($Results.S8=0,"Type in Results"))))
        if self.sulfide == "present":
            return 3.5
        elif self.sulfide == "trace":
            return 2
        elif self.sulfide == "absent":
            return 0


def pre_save_sample_reciever(sender, instance, *args, **kwargs):
    instance.awwa = instance.get_awwa_rating
    instance.point = instance.get_point()


pre_save.connect(pre_save_sample_reciever, sender=Sample)

