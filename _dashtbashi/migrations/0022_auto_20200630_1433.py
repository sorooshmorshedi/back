# Generated by Django 2.2 on 2020-06-30 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0021_auto_20200630_1248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ladingbillnumber',
            old_name='is_invalid',
            new_name='is_revoked',
        ),
    ]
