# Generated by Django 2.2 on 2020-09-16 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0026_auto_20200914_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lading',
            name='receive_type',
            field=models.CharField(blank=True, choices=[('cr', 'نسیه'), ('cs', 'نقدی'), ('p', 'کارت خوان')], max_length=2, null=True),
        ),
    ]
