# Generated by Django 2.2 on 2020-03-14 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0013_auto_20200309_0739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialyear',
            name='accounts',
        ),
        migrations.RemoveField(
            model_name='financialyear',
            name='defaultAccounts',
        ),
        migrations.RemoveField(
            model_name='financialyear',
            name='floatAccountGroups',
        ),
        migrations.RemoveField(
            model_name='financialyear',
            name='floatAccountRelations',
        ),
        migrations.RemoveField(
            model_name='financialyear',
            name='floatAccounts',
        ),
        migrations.RemoveField(
            model_name='financialyear',
            name='units',
        ),
        migrations.RemoveField(
            model_name='financialyear',
            name='wareLevels',
        ),
        migrations.RemoveField(
            model_name='financialyear',
            name='warehouses',
        ),
        migrations.RemoveField(
            model_name='financialyear',
            name='wares',
        ),
    ]
