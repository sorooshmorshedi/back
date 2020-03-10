# Generated by Django 2.2 on 2020-03-10 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_defaultaccount_costcenter'),
        ('cheques', '0009_auto_20200310_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuschange',
            name='bedCostCenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBesAccountAsCostCenter', to='accounts.FloatAccount'),
        ),
        migrations.AddField(
            model_name='statuschange',
            name='besCostCenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBesFloatAccountAsCostCenter', to='accounts.FloatAccount'),
        ),
    ]
