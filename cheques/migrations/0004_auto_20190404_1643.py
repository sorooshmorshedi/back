# Generated by Django 2.0.5 on 2019-04-04 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_remove_financialyear_is_active'),
        ('cheques', '0003_cheque_has_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='cheque',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cheques', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chequebook',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='chequebooks', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='statuschange',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='status_changes', to='companies.FinancialYear'),
            preserve_default=False,
        ),
    ]
