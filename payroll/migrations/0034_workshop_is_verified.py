# Generated by Django 2.2 on 2022-12-14 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0033_auto_20221214_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='is_verified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
