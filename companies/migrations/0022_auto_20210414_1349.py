# Generated by Django 2.2 on 2021-04-14 09:19

from django.db import migrations, models
import helpers.models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0021_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.FileField(blank=True, default=None, null=True, upload_to=helpers.models.upload_to),
        ),
    ]