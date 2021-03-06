# Generated by Django 3.0.7 on 2020-09-03 20:08

from django.db import migrations, models
import samples.models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0012_auto_20200820_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='altitude',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Altitude (ft above sea level)'),
        ),
        migrations.AddField(
            model_name='sample',
            name='field_resistivity',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True, verbose_name='Field Resistivity'),
        ),
        migrations.AddField(
            model_name='sample',
            name='resistivity_chart',
            field=models.ImageField(blank=True, null=True, upload_to=samples.models.upload_image_path),
        ),
        migrations.AddField(
            model_name='sample',
            name='stray_current_graph',
            field=models.ImageField(blank=True, null=True, upload_to=samples.models.upload_image_path),
        ),
    ]
