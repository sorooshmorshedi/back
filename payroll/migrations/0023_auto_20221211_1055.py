# Generated by Django 2.2 on 2022-12-11 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0022_auto_20221211_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjustment',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
    ]