# Generated by Django 2.2 on 2023-01-26 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0107_listofpayitem_loan_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='listofpayitem',
            name='insurance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listofpayitem',
            name='insurance_day',
            field=models.IntegerField(default=0),
        ),
    ]