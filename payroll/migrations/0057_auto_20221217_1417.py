# Generated by Django 2.2 on 2022-12-17 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0056_contract_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]