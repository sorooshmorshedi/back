# Generated by Django 2.2 on 2020-03-23 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0066_auto_20200322_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(blank=True, choices=[(1, 'میانگین موزون'), (0, 'فایفو')], null=True),
        ),
    ]