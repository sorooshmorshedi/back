# Generated by Django 2.2 on 2021-02-23 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributions', '0004_auto_20210222_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='commission_percent',
            field=models.FloatField(default=0),
        ),
    ]