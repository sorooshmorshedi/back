# Generated by Django 2.0.5 on 2018-09-13 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0003_auto_20180912_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricing_type',
            field=models.IntegerField(choices=[(2, 'avg'), (3, 'special_value'), (0, 'fifo'), (1, 'lifo')]),
        ),
        migrations.AlterField(
            model_name='warelevel',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='warelevel',
            unique_together={('name', 'level')},
        ),
    ]
