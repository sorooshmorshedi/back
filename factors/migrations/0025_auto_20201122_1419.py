# Generated by Django 2.2 on 2020-11-22 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0024_warehousehandlingitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehousehandlingitem',
            name='first_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='warehousehandlingitem',
            name='first_confirmed_by',
        ),
        migrations.RemoveField(
            model_name='warehousehandlingitem',
            name='second_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='warehousehandlingitem',
            name='second_confirmed_by',
        ),
    ]
