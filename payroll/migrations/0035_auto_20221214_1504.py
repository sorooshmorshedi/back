# Generated by Django 2.2 on 2022-12-14 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0034_workshop_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='employer_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='is_active',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]