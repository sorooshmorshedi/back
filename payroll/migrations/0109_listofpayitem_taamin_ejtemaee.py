# Generated by Django 2.2 on 2023-01-29 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0108_auto_20230126_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='listofpayitem',
            name='taamin_ejtemaee',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
    ]
