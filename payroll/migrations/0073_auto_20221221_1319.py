# Generated by Django 2.2 on 2022-12-21 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0072_auto_20221221_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionaldeduction',
            name='is_template',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
