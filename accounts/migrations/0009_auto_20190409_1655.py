# Generated by Django 2.0.5 on 2019-04-09 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190409_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='financial_year',
        ),
        migrations.RemoveField(
            model_name='costcenter',
            name='financial_year',
        ),
        migrations.RemoveField(
            model_name='costcentergroup',
            name='financial_year',
        ),
        migrations.RemoveField(
            model_name='floataccount',
            name='financial_year',
        ),
        migrations.RemoveField(
            model_name='independentaccount',
            name='financial_year',
        ),
        migrations.RemoveField(
            model_name='person',
            name='financial_year',
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='floataccountgroup',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='account',
            name='financial_year',
        ),
        migrations.RemoveField(
            model_name='floataccountgroup',
            name='financial_year',
        ),
    ]