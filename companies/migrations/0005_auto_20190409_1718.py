# Generated by Django 2.0.5 on 2019-04-09 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_defaultaccount_financial_year'),
        ('companies', '0004_auto_20190409_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialyear',
            name='default_accounts',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='accounts.DefaultAccount'),
        ),
        migrations.AlterField(
            model_name='financialyear',
            name='accounts',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='accounts.Account'),
        ),
        migrations.AlterField(
            model_name='financialyear',
            name='cost_center_groups',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='accounts.CostCenterGroup'),
        ),
        migrations.AlterField(
            model_name='financialyear',
            name='cost_centers',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='accounts.CostCenter'),
        ),
        migrations.AlterField(
            model_name='financialyear',
            name='float_account_groups',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='accounts.FloatAccountGroup'),
        ),
        migrations.AlterField(
            model_name='financialyear',
            name='float_accounts',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='accounts.FloatAccount'),
        ),
        migrations.AlterField(
            model_name='financialyear',
            name='independent_account',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='accounts.IndependentAccount'),
        ),
        migrations.AlterField(
            model_name='financialyear',
            name='persons',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='accounts.Person'),
        ),
    ]