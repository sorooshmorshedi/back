# Generated by Django 2.2 on 2022-12-10 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0011_workshop_workshop_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='is_active',
            field=models.BooleanField(),
        ),
    ]
