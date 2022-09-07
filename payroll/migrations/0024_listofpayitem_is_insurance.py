# Generated by Django 2.2 on 2022-09-07 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0023_listofpayitem_calculate_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='listofpayitem',
            name='is_insurance',
            field=models.CharField(choices=[('y', 'بله'), ('n', 'خیر')], default='n', max_length=2),
        ),
    ]
