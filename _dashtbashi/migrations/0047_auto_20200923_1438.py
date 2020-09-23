# Generated by Django 2.2 on 2020-09-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0046_oilcompanylading_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='oilcompanyladingitem',
            name='complication_price',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AddField(
            model_name='oilcompanyladingitem',
            name='total_value',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
    ]
