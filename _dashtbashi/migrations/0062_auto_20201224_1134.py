# Generated by Django 2.2 on 2020-12-24 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0061_oilcompanyladingitem_bill_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oilcompanylading',
            name='month',
            field=models.CharField(choices=[('1', 'فروردین'), ('2', 'اردیبهشت'), ('3', 'خرداد'), ('4', 'تیر'), ('5', 'مرداد'), ('6', 'شهریور'), ('7', 'مهر'), ('8', 'آبان'), ('9', 'آذر'), ('10', 'دی'), ('11', 'بهمن'), ('12', 'اسفند')], max_length=1),
        ),
    ]