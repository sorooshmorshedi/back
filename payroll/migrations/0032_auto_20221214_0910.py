# Generated by Django 2.2 on 2022-12-14 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0031_auto_20221213_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='location_of_birth_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='location_of_birth',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
