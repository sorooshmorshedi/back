# Generated by Django 2.2 on 2023-02-14 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0118_auto_20230214_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='listofpay',
            name='bank_pay_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
