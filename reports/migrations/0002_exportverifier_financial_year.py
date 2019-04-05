# Generated by Django 2.0.5 on 2019-04-05 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_remove_financialyear_is_active'),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exportverifier',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='export_verifiers', to='companies.FinancialYear'),
            preserve_default=False,
        ),
    ]
