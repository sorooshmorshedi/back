# Generated by Django 2.0.5 on 2019-02-18 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0005_auto_20181017_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='bijak',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
