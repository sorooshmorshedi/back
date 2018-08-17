# Generated by Django 2.0.5 on 2018-08-16 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0008_auto_20180815_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cheque',
            name='transferNumber',
        ),
        migrations.AddField(
            model_name='statuschange',
            name='transferNumber',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='statuschange',
            name='bedFloatAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBesAccount', to='accounts.FloatAccount'),
        ),
        migrations.AlterField(
            model_name='statuschange',
            name='besFloatAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBesFloatAccount', to='accounts.FloatAccount'),
        ),
    ]
