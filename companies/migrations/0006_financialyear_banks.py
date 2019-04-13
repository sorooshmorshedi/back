# Generated by Django 2.0.5 on 2019-04-10 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_defaultaccount_financial_year'),
        ('companies', '0005_auto_20190409_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialyear',
            name='banks',
            field=models.ManyToManyField(blank=True, related_name='financial_year', to='accounts.Bank'),
        ),
    ]