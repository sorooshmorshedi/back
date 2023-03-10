# Generated by Django 2.2 on 2020-07-26 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0007_auto_20200726_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='factor',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='factorexpense',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='factoritem',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='factorpayment',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
    ]
