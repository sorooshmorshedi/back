# Generated by Django 2.2 on 2022-12-20 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0064_workshop_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hrletter',
            name='is_calculated',
            field=models.BooleanField(default=True),
        ),
    ]