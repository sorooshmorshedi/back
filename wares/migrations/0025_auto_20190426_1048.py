# Generated by Django 2.2 on 2019-04-26 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0024_auto_20190422_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(choices=[(1, 'میانگین موزون'), (0, 'فایفو')]),
        ),
    ]
