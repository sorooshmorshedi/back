# Generated by Django 2.2 on 2020-09-23 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0043_car_imprestaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='oilcompanylading',
            name='gross_price',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
    ]
