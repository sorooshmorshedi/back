# Generated by Django 2.2 on 2023-01-08 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0096_auto_20230108_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='listofpay',
            name='use_in_bime',
            field=models.BooleanField(default=False),
        ),
    ]
