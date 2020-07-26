# Generated by Django 2.2 on 2020-07-19 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='floataccountrelation',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='floataccountrelation',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='floatAccountRelations', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='floataccountrelation',
            name='floatAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='floataccountrelation',
            name='floatAccountGroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation', to='accounts.FloatAccountGroup'),
        ),
        migrations.AddField(
            model_name='floataccountgroup',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='floataccountgroup',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='floatAccountGroups', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='floataccount',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='floataccount',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='floatAccounts', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='floataccount',
            name='floatAccountGroups',
            field=models.ManyToManyField(related_name='floatAccounts', through='accounts.FloatAccountRelation', to='accounts.FloatAccountGroup'),
        ),
        migrations.AddField(
            model_name='defaultaccount',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='defaultAccounts', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='defaultaccount',
            name='costCenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='defaultAccountsAsCostCenter', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='defaultaccount',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='defaultaccount',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financialYear', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='defaultaccount',
            name='floatAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='defaultAccounts', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='accounttype',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accounttype',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountTypes', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='accountbalance',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='balance', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='accountbalance',
            name='costCenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='balanceAsCostCenter', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='accountbalance',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accountbalance',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountsBalance', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='accountbalance',
            name='floatAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='balance', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='account',
            name='costCenterGroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='accountsAsCostCenter', to='accounts.FloatAccountGroup'),
        ),
        migrations.AddField(
            model_name='account',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='account',
            name='floatAccountGroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='accounts', to='accounts.FloatAccountGroup'),
        ),
        migrations.AddField(
            model_name='account',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts', to='accounts.AccountType'),
        ),
    ]