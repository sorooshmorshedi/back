# Generated by Django 2.2 on 2020-03-09 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0049_auto_20200309_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(blank=True, choices=[(1, 'میانگین موزون'), (0, 'فایفو')], null=True),
        ),
    ]