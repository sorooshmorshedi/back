# Generated by Django 2.2 on 2022-12-06 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0002_auto_20221206_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractrow',
            name='use_in_insurance_list',
            field=models.BooleanField(default=False),
        ),
    ]