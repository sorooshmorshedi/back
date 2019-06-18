# Generated by Django 2.2 on 2019-06-18 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0036_auto_20190603_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ware',
            name='metadata',
        ),
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(choices=[(0, 'فایفو'), (1, 'میانگین موزون')]),
        ),
        migrations.DeleteModel(
            name='WareMetaData',
        ),
    ]
