# Generated by Django 2.2 on 2019-04-29 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0015_auto_20190429_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='definition_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
