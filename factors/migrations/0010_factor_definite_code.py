# Generated by Django 2.2 on 2019-04-25 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0009_factor_definition_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='definite_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
