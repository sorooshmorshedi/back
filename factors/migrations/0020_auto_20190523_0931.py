# Generated by Django 2.2 on 2019-05-23 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0012_financialyear_float_account_relations'),
        ('factors', '0019_transfer'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='factor',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='factors', to='accounts.Account'),
        ),
    ]