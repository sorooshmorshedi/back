# Generated by Django 2.2 on 2020-11-18 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0014_auto_20201107_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wareinventory',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
