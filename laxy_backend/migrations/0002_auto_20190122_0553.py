# Generated by Django 2.1.5 on 2019-01-22 05:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laxy_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='type_tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, null=True, size=None),
        ),
    ]
