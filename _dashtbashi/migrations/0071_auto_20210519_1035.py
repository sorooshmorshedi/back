# Generated by Django 2.2 on 2021-05-19 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0070_auto_20210516_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lading',
            name='first_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='lading',
            name='first_confirmed_by',
        ),
        migrations.RemoveField(
            model_name='lading',
            name='second_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='lading',
            name='second_confirmed_by',
        ),
        migrations.RemoveField(
            model_name='oilcompanylading',
            name='first_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='oilcompanylading',
            name='first_confirmed_by',
        ),
        migrations.RemoveField(
            model_name='oilcompanylading',
            name='second_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='oilcompanylading',
            name='second_confirmed_by',
        ),
        migrations.RemoveField(
            model_name='otherdriverpayment',
            name='first_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='otherdriverpayment',
            name='first_confirmed_by',
        ),
        migrations.RemoveField(
            model_name='otherdriverpayment',
            name='second_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='otherdriverpayment',
            name='second_confirmed_by',
        ),
        migrations.RemoveField(
            model_name='remittance',
            name='first_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='remittance',
            name='first_confirmed_by',
        ),
        migrations.RemoveField(
            model_name='remittance',
            name='second_confirmed_at',
        ),
        migrations.RemoveField(
            model_name='remittance',
            name='second_confirmed_by',
        ),
    ]
