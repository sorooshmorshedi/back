# Generated by Django 2.2 on 2020-07-26 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0007_auto_20200725_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='cheque',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='chequebook',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='statuschange',
            name='is_auto_created',
            field=models.BooleanField(default=True),
        ),
    ]
