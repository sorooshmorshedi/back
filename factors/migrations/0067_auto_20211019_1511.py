# Generated by Django 2.2 on 2021-10-19 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0066_auto_20210907_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='explanation',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
