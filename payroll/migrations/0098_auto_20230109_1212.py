# Generated by Django 2.2 on 2023-01-09 08:42

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0097_listofpay_use_in_bime'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='tax',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract',
            name='tax_add_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
    ]