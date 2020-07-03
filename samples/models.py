from django.db import models

# Create your models here.
from django.db.models import F
from django.db.models.signals import pre_save

SOIL_TYPE_CHOICES = (
    ('clay', 'Clay'),
    ('silty_clay', 'Silty Clay'),
    ('silt', 'Silt'),
    ('clean_sand', 'Clean Sand')
)

TEXTURE_CHOICES = (
    ('fine', 'Fine'),
    ('fine_coarse', 'Fine-coarse'),
    ('granular_fine', 'Granular Fine'),
    ('med_fine', 'Med Fine'),
    ('med_fine_coarse', 'Med Fine-coarse'),
    ('coarse', 'Coarse'),
    ('very_fine', 'Very Fine'),
)

COLOR_CHOICES = (
    ('dark_brwn', 'Dark Brown'),
    ('med_brwn', 'Med Brown'),
    ('redish_brwn', 'Redish Brown'),
    ('brown_beige', 'Brown Beige'),
    ('light_brown', 'Light Brown'),
    ('tan', 'Tan'),
    ('dark_light_brown', 'Dark brown/light brown'),
    ('med_brown_tan', 'Med Brown/Tan'),
    ('brown_grey', 'Brown/grey'),
    ('brown', 'Brown'),
    ('beige', 'Beige'),
    ('pink', 'pink'),
)

SULFIDE_CHOICES = (
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('trace', 'Trace'),
)

#
# class SampleManager(models.Manager):
#     # idea from https://stackoverflow.com/questions/17682567/how-to-add-a-calculated-field-to-a-django-model
#     def get_queryset(self):
#         """ Overrides models.Manager method """
#         qs = super(SampleManager, self).get_queryset().annotate(awwa=F('get_awwa_rating'))

class Sample(models.Model):
    sample_no = models.CharField(max_length=120)
    job_no = models.CharField(max_length=120)
    job_name = models.CharField(max_length=120)
    latitude = models.DecimalField(decimal_places=6, max_digits=10)
    longitude = models.DecimalField(decimal_places=6, max_digits=10)
    depth = models.DecimalField(decimal_places=2, max_digits=5)
    soil_type = models.CharField(max_length=32, choices=SOIL_TYPE_CHOICES)
    texture = models.CharField(max_length=32, choices=TEXTURE_CHOICES)
    color = models.CharField(max_length=32, choices=COLOR_CHOICES)
    ph = models.DecimalField(decimal_places=2, max_digits=10)
    redox_potential = models.DecimalField(decimal_places=2, max_digits=10)
    conductivity = models.DecimalField(decimal_places=3, max_digits=10)
    chloride = models.DecimalField(decimal_places=2, max_digits=10)
    sulfate = models.DecimalField(decimal_places=1, max_digits=10)
    salinity = models.DecimalField(decimal_places=2, max_digits=10)
    resistivity_as_collected = models.DecimalField(decimal_places=2, max_digits=10)
    resistivity_saturated = models.DecimalField(decimal_places=2, max_digits=10)
    carbonate = models.BooleanField()
    sulfide = models.CharField(max_length=32, choices=SULFIDE_CHOICES)
    moisture_content = models.DecimalField(decimal_places=2, max_digits=10, blank=True)
    comments = models.TextField(blank=True)
    awwa = models.CharField(max_length=32, blank=True)

    # objects = SampleManager()

    @property
    def get_awwa_rating(self):
        # =IF(H8>9.9,"Severe",IF(H8>1,"Moderate",IF(H8>=0,"Mild",IF(H8>-1,"Type in Results"))))
        print(self.ph)
        print(self.get_redox())
        print(self.get_resistivity_simplified())
        print(self.get_sulfide_simplified())
        print(self.sulfide)
        score = self.ph + self.get_redox() + self.get_resistivity_simplified() + self.get_sulfide_simplified()

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
        elif self.redox_potential < 0:
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


pre_save.connect(pre_save_sample_reciever, sender=Sample)

