# Generated by Django 2.0.5 on 2018-07-17 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0005_auto_20180716_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricing_type',
            field=models.IntegerField(choices=[(1, 'lifo'), (0, 'fifo'), (2, 'avg'), (3, 'special_value')]),
        ),
    ]
