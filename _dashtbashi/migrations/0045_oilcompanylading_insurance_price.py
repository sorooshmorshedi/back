# Generated by Django 2.2 on 2020-09-23 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0044_oilcompanylading_gross_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='oilcompanylading',
            name='insurance_price',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
    ]
