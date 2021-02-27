# Generated by Django 2.2 on 2021-02-27 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20210207_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultaccount',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='defaultAccounts', to='accounts.Account'),
        ),
    ]
