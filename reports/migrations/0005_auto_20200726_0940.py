# Generated by Django 2.2 on 2020-07-26 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_exportverifier_is_auto_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exportverifier',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
    ]
