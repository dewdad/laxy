# Generated by Django 2.1.5 on 2019-02-12 05:12

from django.db import migrations, models
import laxy_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('laxy_backend', '0004_file_deleted_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='expiry_time',
            field=models.DateTimeField(blank=True, default=laxy_backend.models._job_expiry_datetime, null=True),
        ),
    ]
