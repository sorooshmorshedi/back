# Generated by Django 2.2 on 2020-09-19 12:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20200919_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='modules',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), default=list, size=None),
        ),
    ]