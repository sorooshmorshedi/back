# Generated by Django 2.2 on 2020-07-19 12:49

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_option_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='option',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
    ]
