# Generated by Django 2.2 on 2022-12-15 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0043_auto_20221215_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshoppersonnel',
            name='sanavat_day',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
