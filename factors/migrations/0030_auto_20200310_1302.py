# Generated by Django 2.2 on 2020-03-10 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_account_person_type'),
        ('factors', '0029_factor_costcenter'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='costCenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='factorExpenseAsCostCenter', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='factorexpense',
            name='costCenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='factorExpensesAsCostCenter', to='accounts.FloatAccount'),
        ),
    ]