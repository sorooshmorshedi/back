# Generated by Django 2.2 on 2020-03-15 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0058_auto_20200314_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(blank=True, choices=[(0, 'فایفو'), (1, 'میانگین موزون')], null=True),
        ),
    ]
