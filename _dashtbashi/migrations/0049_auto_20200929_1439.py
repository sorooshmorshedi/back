# Generated by Django 2.2 on 2020-09-29 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0048_auto_20200924_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remittance',
            name='code',
            field=models.IntegerField(),
        ),
    ]
