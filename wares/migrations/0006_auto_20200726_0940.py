# Generated by Django 2.2 on 2020-07-26 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0005_auto_20200726_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ware',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wareinventory',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='warelevel',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
    ]
