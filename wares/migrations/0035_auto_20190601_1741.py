# Generated by Django 2.2 on 2019-06-01 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0034_auto_20190523_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(choices=[(0, 'فایفو'), (1, 'میانگین موزون')]),
        ),
    ]
