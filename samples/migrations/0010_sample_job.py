# Generated by Django 3.0.7 on 2020-08-06 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20200806_1810'),
        ('samples', '0009_auto_20200805_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jobs.Job'),
            preserve_default=False,
        ),
    ]
