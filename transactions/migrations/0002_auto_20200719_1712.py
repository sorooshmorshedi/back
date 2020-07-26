# Generated by Django 2.2 on 2020-07-19 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0002_auto_20200719_1712'),
        ('accounts', '0002_auto_20200719_1712'),
        ('transactions', '0001_initial'),
        ('sanads', '0002_auto_20200719_1712'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionitem',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionItems', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='floatAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactionItems', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='transactions.Transaction'),
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.DefaultAccount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='costCenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactionsAsCostCenter', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='floatAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sanad',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='sanads.Sanad'),
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together={('code', 'type')},
        ),
    ]