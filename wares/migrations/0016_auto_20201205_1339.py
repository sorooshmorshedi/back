# Generated by Django 2.2 on 2020-12-05 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0015_auto_20201118_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wareinventory',
            name='fee',
            field=models.DecimalField(decimal_places=6, max_digits=24),
        ),
    ]
