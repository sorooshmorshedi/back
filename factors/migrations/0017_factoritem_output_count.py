# Generated by Django 2.2 on 2019-05-19 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0016_auto_20190429_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='factoritem',
            name='output_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]