# Generated by Django 2.2 on 2020-07-26 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0006_auto_20200725_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='factorexpense',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='factoritem',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='factorpayment',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='transfer',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
    ]
