# Generated by Django 2.2 on 2021-07-18 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imprests', '0024_auto_20210519_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imprestsettlement',
            name='explanation',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='imprestsettlementitem',
            name='explanation',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
