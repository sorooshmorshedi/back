# Generated by Django 2.2 on 2022-01-02 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracting', '0006_auto_20220102_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
