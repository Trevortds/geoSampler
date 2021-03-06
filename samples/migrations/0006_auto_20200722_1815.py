# Generated by Django 3.0.5 on 2020-07-22 18:15

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0005_auto_20200705_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='sample',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
        migrations.AlterField(
            model_name='sample',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
    ]
