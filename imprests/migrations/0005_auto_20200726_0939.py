# Generated by Django 2.2 on 2020-07-26 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imprests', '0004_auto_20200725_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='imprestsettlement',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='imprestsettlementitem',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
    ]
