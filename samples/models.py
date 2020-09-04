import os
from decimal import Decimal
import random

from django.contrib.gis.db import models

# Create your models here.
from django.contrib.gis.geos import Point
from django.core.validators import MinValueValidator
from django.db.models import F
from django.db.models.signals import pre_save
from django.urls import reverse
from guardian.shortcuts import get_objects_for_user

from jobs.models import Job

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

def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1, 912345912345)
    name, ext = get_filename_ext(filename)
    return f"samples/{new_filename}/{new_filename}{ext}"


class SampleManager(models.Manager):
    # idea from https://stackoverflow.com/questions/17682567/how-to-add-a-calculated-field-to-a-django-model
    # def get_queryset(self):
    #     """ Overrides models.Manager method """
    #     qs = super(SampleManager, self).get_queryset().annotate(awwa=F('get_awwa_rating'))
    def get_samples_for_user(self, user):
        job_qs = get_objects_for_user(user, 'jobs.view_this_job')
        return super(SampleManager, self).get_queryset().filter(job__in=job_qs)

    def get_by_id(self, pk):
        qs = self.get_queryset().filter(pk=pk)
        if qs.count() == 1:
            return qs.first()
        return None

# TODO add date (nullable)?
# possibly making another table for field data
# and another for stray current
# and another for the CIS (close interval survey)
# relate via job number

class Sample(models.Model):
    sample_no                = models.CharField(verbose_name="Sample #", max_length=120, unique=True)
    job                      = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_name                 = models.CharField(verbose_name="Job Name", max_length=120)
    latitude                 = models.DecimalField(verbose_name="Latitude", decimal_places=9, max_digits=20)
    longitude                = models.DecimalField(verbose_name="Longitude", decimal_places=9, max_digits=20)
    altitude = models.DecimalField(verbose_name="Altitude (ft above sea level)", decimal_places=2, max_digits=10,
                                   blank=True, null=True)
    depth                    = models.DecimalField(verbose_name="Depth (feet)", decimal_places=2, max_digits=5,
                                                   null=True, blank=True)
    soil_type                = models.CharField(verbose_name="Soil Type", max_length=32, choices=SOIL_TYPE_CHOICES,
                                                null=True, blank=True)
    texture                  = models.CharField(verbose_name="Texture", max_length=32, null=True, blank=True)
    color                    = models.CharField(verbose_name="Color", max_length=32, null=True, blank=True)
    ph                       = models.DecimalField(verbose_name=u"\u00A0pH", decimal_places=2, max_digits=10,
                                                   null=True, blank=True)
    redox_potential          = models.DecimalField(verbose_name="Redox Potential (mV)", decimal_places=2, max_digits=10,
                                                   null=True, blank=True)
    conductivity             = models.DecimalField(verbose_name="Conductivity (µS/cm)", decimal_places=3, max_digits=10,
                                                   null=True, blank=True)
    chloride                 = models.DecimalField(verbose_name="Chloride (ppm)", decimal_places=2, max_digits=10,
                                                   null=True, blank=True)
    sulfate                  = models.DecimalField(verbose_name="Sulfate (ppm", decimal_places=1, max_digits=10,
                                                   null=True, blank=True)
    salinity                 = models.DecimalField(verbose_name="Salinity (%)", decimal_places=2, max_digits=10,
                                                   null=True, blank=True)
    resistivity_as_collected = models.DecimalField(verbose_name="Resistivity As Collected (KΩ-cm)", decimal_places=2,
                                                   max_digits=10,
                                                   validators=[MinValueValidator(Decimal('0.001'))],
                                                   null=True, blank=True)
    resistivity_saturated    = models.DecimalField(verbose_name="Resistivity Saturated (KΩ-cm)", decimal_places=2,
                                                   max_digits=10, null=True, blank=True)
    field_resistivity        = models.DecimalField(verbose_name="Field Resistivity", decimal_places=5, max_digits=15,
                                                   blank=True, null=True)
    carbonate                = models.CharField(verbose_name="Carbonate", max_length=32, choices=PRES_ABS_CHOICES,
                                                null=True, blank=True)
    sulfide                  = models.CharField(verbose_name="Sulfide", max_length=32, choices=PRES_ABS_CHOICES,
                                                null=True, blank=True)
    moisture_content         = models.DecimalField(verbose_name="Moisture Content (%)", decimal_places=2, max_digits=10,
                                                   blank=True, null=True)
    comments                 = models.TextField(verbose_name="Comments", blank=True, null=True)
    awwa                     = models.CharField(verbose_name="AWWA Rating", max_length=32, blank=True, null=True)
    wssc                     = models.CharField(verbose_name="WSSC Rating", max_length=32, blank=True, null=True)

    # new additions 2020-09-03
    stray_current_graph = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    resistivity_chart = models.ImageField(upload_to=upload_image_path, null=True, blank=True)



    point                    = models.PointField(geography=True, blank=True, null=True)

    objects = SampleManager()

    def __str__(self):
        return self.sample_no + " " + self.job_name

    def get_point(self):
        """used by frontend map, which expects lat ang long backwards"""
        return Point(float(self.latitude), float(self.longitude))

    # @property
    def get_absolute_url(self):
        # f"/products/{self.slug}"
        return reverse("samples:detail", kwargs={"sample_no": self.sample_no})

    @property
    def geom(self):
        """I don't think this should be necessary, but I can't figure out how to make leaflet look at "point" """
        return Point(self.point.y, self.point.x)

    def get_wssc_rating(self):
        """=IF(H3>15.5,"Severe",IF(H3>9.9,"Appreciable",IF(H3>4.9,"Moderate",IF(H3>=0,"Mild",IF(H3>-1,
        "Type in Results")))))"""
        score = self.get_wssc_ph_score() + self.get_chloride_content() + self.get_redox_potential() + self.soil_rating()
        if score > 15:
            return "Severe"
        elif score > 9.9:
            return "Appreciable"
        elif score > 4.9:
            return "Moderate"
        elif score >= 0:
            return "Mild"
        elif score > -1:
            raise ValueError("Invalid WSSC score")


    def get_wssc_ph_score(self):
        """=IF($Results.J5>0, "5", IF($Results.J5>1.9, "3", IF($Results.J5>3.9, "0", IF($Results.J5>8.5, "0",
        IF($Results.J5>-1, "Type in Results", “Error”))))))))))"""
        # I think the above formula is actually wrong, but it is reproduced exactly below.
        if self.ph > 14:
            raise ValueError("Invalid pH: higher than 15")
        elif self.ph > 8.5:
            return 0
        elif self.ph > 3.9:
            return 0
        elif self.ph > 1.9:
            return 3
        elif self.ph >= 0:
            return 5
        else:
            raise ValueError("Invalid pH: less than 0")


    def get_chloride_content(self):
        """=IF($Results.M5>1000, "10", IF($Results.M5>499, "6", IF($Results.M5>199, "4", IF($Results.M5>49, "2",
        IF($Results.M5>0, "0", IF($Results.M5>-1, "Type in Results", “Error”))))))))))))"""
        if self.chloride > 1000:
            return 10
        elif self.chloride > 499:
            return 6
        elif self.chloride > 199:
            return 4
        elif self.chloride > 49:
            return 2
        elif self.chloride > 0:
            return 0
        elif self.chloride > -1:
            raise ValueError("Invalid chloride content")

    def soil_rating(self):
        """
        =IF($Calculator.M6="Clay (blue-gray)", "10", IF($Calculator.M6="Clay/Stone", "5", IF($Calculator.M6="Clay", "3",
        IF($Calculator.M6="Silt", "2", IF($Calculator.M6="Clean Sand", "0")))))"""
        SOIL_TYPE_CHOICES = (
            ('clay_blue_gray', 'Clay (blue-gray)'),
            ('clay_stone', 'Clay/Stone'),
            ('clay', 'Clay'),
            ('silt', 'Silt'),
            ('sand', 'Sand')
        )
        if self.soil_type == "clay_blue_gray":
            return 10
        elif self.soil_type == "clay_stone":
            return 5
        elif self.soil_type == "clay":
            return 3
        elif self.soil_type == "silt":
            return 2
        elif self.soil_type == "sand":
            return 0


    def get_awwa_rating(self):
        # =IF(H8>9.9,"Severe",IF(H8>1,"Moderate",IF(H8>=0,"Mild",IF(H8>-1,"Type in Results"))))
        score = self.get_awwa_ph_score() + self.get_redox() + self.get_resistivity_simplified() + \
                self.get_sulfide_simplified()

        if score > 9.9:
            return "Severe"
        elif score > 1:
            return "Moderate"
        elif score >= 0:
            return "Mild"
        else:
            raise ValueError("Invalid AWWA Score")

    def get_awwa_ph_score(self):
        # =IF($Results.J2>8.5,"3",IF($Results.J2>4,"0",IF($Results.J2>2,"3",IF($Results.J2>0,"5",
        # IF($Results.J2>-1,"Type in Results","Error")))))
        if self.ph > 14:
            raise ValueError("Invalid pH: greater than 15")
        elif self.ph > 8.5:
            return 3
        elif self.ph > 4:
            return 0
        elif self.ph > 2:
            return 3
        elif self.ph >= 0:
            return 5
        else:
            raise ValueError("Invalid pH: less than 0")

    def get_redox(self):
        # =IF($Results.K10>100.1,"0",IF($Results.K10>50,"3.5",IF($Results.K10>0,"4",IF($Results.K10<0,"5",
        # IF($Results.K10>-1000,"Type in Results")))))
        if self.redox_potential > 100.1:
            return 0
        elif self.redox_potential > 50:
            return 3.5
        elif self.redox_potential > 0:
            return 4
        elif self.redox_potential <= 0:
            return 5
        else:
            raise ValueError("Invalid Redox Potential")

    def get_redox_potential(self):
        # =IF($Results.K10>100.1,"0",IF($Results.K10>50,"3.5",IF($Results.K10>0,"4",IF($Results.K10<0,"5",
        # IF($Results.K10>-1000,"Type in Results")))))
        if self.redox_potential > 100.1:
            return 0
        elif self.redox_potential > 0:
            return 4
        elif self.redox_potential <= 0:
            return 5
        else:
            raise ValueError("Invalid Redox Potential")

    def get_resistivity_simplified(self):
        # =IF($Results.P8>3, "0", IF($Results.P8>2.5, "1", IF($Results.P8>2.1, "2", IF($Results.P8>1.8, "5",
        # IF($Results.P8>=1.5, "8",IF($Results.P8>0, "10",IF($Results.P8>-1, "Type in Results",“Error”))))))))))))))
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
        elif self.resistivity_as_collected >= 0:
            return 10
        else:
            raise ValueError("Invalid Resistivity As Collected")

    def get_sulfide_simplified(self):
        # =IF($Results.S8="Present",3.5,IF($Results.S8="Trace",2,IF($Results.S8="Absent",0,IF($Results.S8=0,
        # "Type in Results"))))
        if self.sulfide == "present":
            return 3.5
        elif self.sulfide == "trace":
            return 2
        elif self.sulfide == "absent":
            return 0


def pre_save_sample_reciever(sender, instance, *args, **kwargs):
    try:
        instance.awwa = instance.get_awwa_rating()
    except (ValueError, TypeError):
        print("Failed to calculate awwa")
    try:
        instance.wssc = instance.get_wssc_rating()
    except (ValueError, TypeError):
        print("failed to calculat wssc")
    instance.point = instance.get_point()
    # if instance.job_id is None:
    #     instance.job_id = instance.job.job_no
    #     instance.job_title = instance.job.job_name


pre_save.connect(pre_save_sample_reciever, sender=Sample)

