# Generated by Django 2.0.5 on 2019-04-06 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0013_auto_20190405_1013'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='warehouseinventory',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='warehouseinventory',
            name='financial_year',
        ),
        migrations.RemoveField(
            model_name='warehouseinventory',
            name='ware',
        ),
        migrations.RemoveField(
            model_name='warehouseinventory',
            name='warehouse',
        ),
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(choices=[(0, 'فایفو'), (1, 'میانگین موزون')]),
        ),
        migrations.DeleteModel(
            name='WarehouseInventory',
        ),
    ]