# Generated by Django 2.2 on 2020-11-08 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0056_auto_20201107_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lading',
            name='local_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='oilcompanylading',
            name='local_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='otherdriverpayment',
            name='local_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='remittance',
            name='local_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]