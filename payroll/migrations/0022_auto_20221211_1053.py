# Generated by Django 2.2 on 2022-12-11 07:23

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0021_auto_20221211_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjustment',
            name='change_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
    ]
