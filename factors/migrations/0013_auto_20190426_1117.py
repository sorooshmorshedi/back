# Generated by Django 2.2 on 2019-04-26 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0012_auto_20190426_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='code',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
