# Generated by Django 2.0.5 on 2018-08-24 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0013_auto_20180817_1554'),
        ('sanads', '0018_auto_20180817_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionitem',
            name='Cheque',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactionItems', to='cheques.Cheque'),
        ),
    ]
