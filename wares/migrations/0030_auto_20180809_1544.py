# Generated by Django 2.0.5 on 2018-08-09 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0029_auto_20180805_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricing_type',
            field=models.IntegerField(choices=[(0, 'fifo'), (3, 'special_value'), (1, 'lifo'), (2, 'avg')]),
        ),
    ]
