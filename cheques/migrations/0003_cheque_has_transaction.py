# Generated by Django 2.0.5 on 2019-03-30 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0002_auto_20190318_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='cheque',
            name='has_transaction',
            field=models.BooleanField(default=False),
        ),
    ]