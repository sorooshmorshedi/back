# Generated by Django 2.2 on 2022-08-13 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0005_auto_20220813_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='hrletter',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
