# Generated by Django 2.2 on 2021-02-07 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20201217_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultaccount',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='defaultAccounts', to='accounts.Account'),
        ),
    ]
