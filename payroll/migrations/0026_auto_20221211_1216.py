# Generated by Django 2.2 on 2022-12-11 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0025_contractrow_initial_to_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjustment',
            name='status',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
