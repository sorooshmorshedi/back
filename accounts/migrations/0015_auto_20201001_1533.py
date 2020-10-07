# Generated by Django 2.2 on 2020-10-01 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_remove_accounttype_financial_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_account', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accountbalance',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_accountbalance', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_accounttype', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='defaultaccount',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_defaultaccount', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='floataccount',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_floataccount', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='floataccountgroup',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_floataccountgroup', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='floataccountrelation',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_floataccountrelation', to=settings.AUTH_USER_MODEL),
        ),
    ]