# Generated by Django 2.0.5 on 2018-09-26 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0010_auto_20180924_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricing_type',
            field=models.IntegerField(choices=[(3, 'special_value'), (1, 'lifo'), (2, 'avg'), (0, 'fifo')]),
        ),
    ]
