# Generated by Django 2.0.5 on 2018-06-15 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180615_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='level',
            field=models.IntegerField(choices=[('0', 'group'), ('1', 'kol'), ('2', 'moein'), ('3', 'tafzili')]),
        ),
    ]
