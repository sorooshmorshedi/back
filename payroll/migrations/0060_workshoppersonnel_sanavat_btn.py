# Generated by Django 2.2 on 2022-12-19 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0059_auto_20221218_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshoppersonnel',
            name='sanavat_btn',
            field=models.BooleanField(default=False),
        ),
    ]
