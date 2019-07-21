# Generated by Django 2.2 on 2019-07-20 12:34

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import factors.models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0024_auto_20190618_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='factoritem',
            name='fees',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=factors.models.get_empty_dict),
        ),
    ]
