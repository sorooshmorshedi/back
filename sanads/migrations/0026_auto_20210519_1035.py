# Generated by Django 2.2 on 2021-05-19 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0025_auto_20210301_1140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sanad',
            name='first_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='sanad',
            name='first_confirmed_by',
        ),
        migrations.RemoveField(
            model_name='sanad',
            name='second_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='sanad',
            name='second_confirmed_by',
        ),
    ]