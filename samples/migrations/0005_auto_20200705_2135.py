# Generated by Django 3.0.5 on 2020-07-05 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0004_auto_20200705_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='sample_no',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]
