# Generated by Django 2.2 on 2020-10-04 09:51

from django.db import migrations, models
from django.db.models.expressions import F


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0016_auto_20201001_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='temporary_code',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]