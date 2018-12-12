# Generated by Django 2.0.5 on 2018-10-23 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0004_auto_20181017_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ware',
            old_name='is_disabled',
            new_name='isDisabled',
        ),
        migrations.RenameField(
            model_name='ware',
            old_name='max_inventory',
            new_name='maxInventory',
        ),
        migrations.RenameField(
            model_name='ware',
            old_name='max_sale',
            new_name='maxSale',
        ),
        migrations.RenameField(
            model_name='ware',
            old_name='min_inventory',
            new_name='minInventory',
        ),
        migrations.RenameField(
            model_name='ware',
            old_name='min_sale',
            new_name='minSale',
        ),
        migrations.RemoveField(
            model_name='ware',
            name='pricing_type',
        ),
        migrations.AddField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(choices=[(2, 'avg'), (0, 'fifo')], default=0),
            preserve_default=False,
        ),
    ]