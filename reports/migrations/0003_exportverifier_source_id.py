# Generated by Django 2.0.5 on 2019-04-09 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_exportverifier_financial_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='exportverifier',
            name='source_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]