# Generated by Django 2.2 on 2022-12-17 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0054_auto_20221217_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mission',
            name='mission_type',
            field=models.CharField(blank=True, choices=[('h', 'ساعتی'), ('d', 'روزانه')], max_length=2, null=True),
        ),
    ]
