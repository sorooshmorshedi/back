# Generated by Django 2.2 on 2022-12-19 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0060_workshoppersonnel_sanavat_btn'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshoppersonnel',
            name='sanavat_button',
            field=models.BooleanField(default=False),
        ),
    ]
