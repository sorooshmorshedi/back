# Generated by Django 2.2 on 2021-04-04 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20210301_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='max_bed',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='max_bes',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='floataccount',
            name='max_bed',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='floataccount',
            name='max_bed_with_sanad',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='floataccount',
            name='max_bes',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='floataccount',
            name='max_bes_with_sanad',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
    ]