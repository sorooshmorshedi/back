# Generated by Django 2.2 on 2019-07-20 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20190411_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='level',
            field=models.IntegerField(choices=[(0, 'group'), (1, 'kol'), (2, 'moein'), (3, 'tafsili')]),
        ),
    ]