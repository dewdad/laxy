# Generated by Django 2.1.5 on 2019-02-12 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laxy_backend', '0003_auto_20190212_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='deleted_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
