# Generated by Django 2.2 on 2020-10-17 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0012_auto_20201015_0838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ware',
            name='category',
        ),
        migrations.DeleteModel(
            name='WareLevel',
        ),
    ]
