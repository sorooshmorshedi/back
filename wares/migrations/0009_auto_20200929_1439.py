# Generated by Django 2.2 on 2020-09-29 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0008_auto_20200929_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ware',
            name='barcode',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ware',
            name='code',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='warelevel',
            name='code',
            field=models.CharField(max_length=50),
        ),
    ]
