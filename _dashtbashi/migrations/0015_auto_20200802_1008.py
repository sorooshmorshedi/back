# Generated by Django 2.2 on 2020-08-02 05:38

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0014_auto_20200730_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='remittance',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='remittance',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='remittance',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
    ]
