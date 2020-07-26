# Generated by Django 2.2 on 2020-07-19 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sanads', '0001_initial'),
        ('accounts', '0002_auto_20200719_1712'),
        ('cheques', '0001_initial'),
        ('companies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='statuschange',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='statuschange',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statusChanges', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='statuschange',
            name='sanad',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statusChange', to='sanads.Sanad'),
        ),
        migrations.AddField(
            model_name='chequebook',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chequebook', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='chequebook',
            name='costCenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequebooksAsCostCenter', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='chequebook',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chequebook',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chequebooks', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='chequebook',
            name='floatAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequebook', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='receivedCheques', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='chequebook',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cheques', to='cheques.Chequebook'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='costCenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='receivedChequesAsCostCenter', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cheque',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cheques', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='floatAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='receivedCheques', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='lastAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lastCheques', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='lastCostCenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lastChequesAsCostCenter', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='lastFloatAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lastCheques', to='accounts.FloatAccount'),
        ),
    ]