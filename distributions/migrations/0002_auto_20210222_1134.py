# Generated by Django 2.2 on 2021-02-22 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0018_auto_20210104_1053'),
        ('distributions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commissionrange',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commissionrangeitem',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='companies.FinancialYear'),
            preserve_default=False,
        ),
    ]
