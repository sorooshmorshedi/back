# Generated by Django 2.2 on 2020-12-24 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0062_auto_20201224_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='oilcompanyladingitem',
            name='net_price',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
    ]
