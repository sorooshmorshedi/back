# Generated by Django 2.2 on 2023-02-09 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0116_auto_20230208_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='listofpayitem',
            name='dept_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
    ]
