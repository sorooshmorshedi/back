# Generated by Django 2.2 on 2022-12-10 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0014_auto_20221210_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshoppersonnel',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]