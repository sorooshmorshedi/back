# Generated by Django 2.0.5 on 2018-10-07 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0014_auto_20181007_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricing_type',
            field=models.IntegerField(choices=[(1, 'lifo'), (2, 'avg'), (3, 'special_value'), (0, 'fifo')]),
        ),
    ]
