# Generated by Django 2.2 on 2020-08-09 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200727_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultaccount',
            name='codename',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
