# Generated by Django 2.2 on 2022-12-11 08:22

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0024_contractrow_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractrow',
            name='initial_to_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
    ]
