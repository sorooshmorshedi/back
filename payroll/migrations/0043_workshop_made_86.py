# Generated by Django 2.2 on 2022-09-18 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0042_auto_20220918_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='made_86',
            field=models.BooleanField(default=False),
        ),
    ]
