# Generated by Django 2.2 on 2021-10-17 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0032_auto_20210719_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanad',
            name='explanation',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
