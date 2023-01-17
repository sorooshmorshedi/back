# Generated by Django 2.2 on 2023-01-05 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0093_workshoppersonnel_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hrletter',
            name='daily_pay_base',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='day_hourly_pay_base',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='insurance_benefit',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='insurance_not_included',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='insurance_pay_day',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='month_hourly_pay_base',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='monthly_pay_base',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='listofpayitem',
            name='pay_base',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
    ]