# Generated by Django 2.2 on 2021-01-30 06:54

from django.db import migrations


def save_all_factors(apps, schema_editor):
    Factor = apps.get_model('factors', 'Factor')
    for item in Factor.objects.all():
        item.save()


class Migration(migrations.Migration):
    dependencies = [
        ('factors', '0037_auto_20210130_1024'),
    ]

    operations = [
        migrations.RunPython(save_all_factors, migrations.RunPython.noop)
    ]
