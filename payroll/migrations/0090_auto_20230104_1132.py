# Generated by Django 2.2 on 2023-01-04 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0089_auto_20230104_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshoptax',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='workshoptax',
            name='un_editable',
            field=models.BooleanField(default=False),
        ),
    ]