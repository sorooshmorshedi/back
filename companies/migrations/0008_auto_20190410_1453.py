# Generated by Django 2.0.5 on 2019-04-10 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0021_auto_20190410_1453'),
        ('companies', '0007_auto_20190410_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialyear',
            name='unit',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='wares.Unit'),
        ),
        migrations.AddField(
            model_name='financialyear',
            name='ware_levels',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='wares.WareLevel'),
        ),
        migrations.AddField(
            model_name='financialyear',
            name='warehouses',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='wares.Warehouse'),
        ),
        migrations.AddField(
            model_name='financialyear',
            name='wares',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='wares.Ware'),
        ),
    ]
