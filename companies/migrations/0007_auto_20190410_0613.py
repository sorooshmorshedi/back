# Generated by Django 2.0.5 on 2019-04-10 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_financialyear_banks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='financialyear',
            old_name='independent_account',
            new_name='independent_accounts',
        ),
    ]