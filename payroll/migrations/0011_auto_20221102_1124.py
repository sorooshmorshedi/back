# Generated by Django 2.2 on 2022-11-02 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0010_auto_20221027_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='listofpay',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='listofpay',
            name='use_in_calculate',
            field=models.BooleanField(default=False),
        ),
    ]