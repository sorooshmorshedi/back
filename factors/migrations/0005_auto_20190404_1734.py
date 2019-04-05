# Generated by Django 2.0.5 on 2019-04-04 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0004_auto_20190404_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='factorExpense', to='accounts.Account'),
        ),
        migrations.AlterField(
            model_name='factorexpense',
            name='factor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='factors.Factor'),
        ),
    ]
