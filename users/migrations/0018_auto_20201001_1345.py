# Generated by Django 2.2 on 2020-10-01 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20200929_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='max_companies',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='max_users',
            field=models.IntegerField(default=0),
        ),
    ]
