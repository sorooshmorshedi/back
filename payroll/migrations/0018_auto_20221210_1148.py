# Generated by Django 2.2 on 2022-12-10 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0017_auto_20221210_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='job_location_status',
            field=models.IntegerField(blank=True, choices=[(1, 'عادی'), (2, 'مناطق کمتر توسعه یافته'), (3, 'مناطق آزاد تجاری')], null=True),
        ),
    ]
