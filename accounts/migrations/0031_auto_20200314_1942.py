# Generated by Django 2.2 on 2020-03-14 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0014_auto_20200314_1942'),
        ('accounts', '0030_auto_20200312_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountbalance',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='accountsBalance', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accounttype',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='accountTypes', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='floataccount',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='floatAccounts', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='floataccountgroup',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='floatAccountGroups', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='floataccountrelation',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='floatAccountRelations', to='companies.FinancialYear'),
            preserve_default=False,
        ),
    ]