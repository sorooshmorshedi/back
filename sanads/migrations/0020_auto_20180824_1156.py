# Generated by Django 2.0.5 on 2018-08-24 07:26

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0019_transactionitem_cheque'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionitem',
            name='due',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='Cheque',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactionItem', to='cheques.Cheque'),
        ),
    ]
