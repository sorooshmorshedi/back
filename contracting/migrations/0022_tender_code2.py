# Generated by Django 2.2 on 2022-07-16 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracting', '0021_auto_20220427_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='tender',
            name='code2',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
