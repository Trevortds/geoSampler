# Generated by Django 3.0.7 on 2020-08-20 18:49

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0011_auto_20200820_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='carbonate',
            field=models.CharField(blank=True, choices=[('present', 'Present'), ('absent', 'Absent')], max_length=32, null=True, verbose_name='Carbonate'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='chloride',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Chloride (ppm)'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='color',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='conductivity',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Conductivity (µS/cm)'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='depth',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Depth (feet)'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='ph',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='\xa0pH'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='redox_potential',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Redox Potential (mV)'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='resistivity_as_collected',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.001'))], verbose_name='Resistivity As Collected (KΩ-cm)'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='resistivity_saturated',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Resistivity Saturated (KΩ-cm)'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='salinity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Salinity (%)'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='soil_type',
            field=models.CharField(blank=True, choices=[('clay_blue_gray', 'Clay (blue-gray)'), ('clay_stone', 'Clay/Stone'), ('clay', 'Clay'), ('silt', 'Silt'), ('sand', 'Sand')], max_length=32, null=True, verbose_name='Soil Type'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sulfate',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True, verbose_name='Sulfate (ppm'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sulfide',
            field=models.CharField(blank=True, choices=[('present', 'Present'), ('absent', 'Absent')], max_length=32, null=True, verbose_name='Sulfide'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='texture',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Texture'),
        ),
    ]