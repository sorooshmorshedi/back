# Generated by Django 2.2 on 2020-09-24 06:16

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0047_auto_20200923_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lading',
            name='bill_date',
            field=django_jalali.db.models.jDateField(null=True),
        ),
        migrations.AlterField(
            model_name='lading',
            name='lading_date',
            field=django_jalali.db.models.jDateField(null=True),
        ),
    ]
