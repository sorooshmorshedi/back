# Generated by Django 2.2 on 2020-12-21 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0059_auto_20201110_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lading',
            name='sanad',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lading', to='sanads.Sanad'),
        ),
        migrations.AlterField(
            model_name='oilcompanylading',
            name='sanad',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='oilCompanyLading', to='sanads.Sanad'),
        ),
    ]