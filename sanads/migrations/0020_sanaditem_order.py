# Generated by Django 2.2 on 2020-11-18 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0019_auto_20201110_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='sanaditem',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]