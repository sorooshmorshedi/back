# Generated by Django 2.2 on 2020-09-29 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0007_auto_20200906_1023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ware',
            old_name='isService',
            new_name='is_service',
        ),
    ]
