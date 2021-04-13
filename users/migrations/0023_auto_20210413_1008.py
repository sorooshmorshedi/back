# Generated by Django 2.2 on 2021-04-13 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20210301_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='active_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usersActiveCompany', to='companies.Company'),
        ),
        migrations.AlterField(
            model_name='user',
            name='active_financial_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='companies.FinancialYear'),
        ),
    ]
