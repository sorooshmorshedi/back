# Generated by Django 2.2 on 2023-02-07 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0114_auto_20230202_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshoptaxrow',
            name='is_last',
            field=models.BooleanField(default=False),
        ),
    ]
