# Generated by Django 2.2 on 2021-07-27 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0062_auto_20210727_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='factorsaggregatedsanad',
            name='explanation',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
