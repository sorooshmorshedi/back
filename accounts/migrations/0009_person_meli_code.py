# Generated by Django 2.0.5 on 2019-02-18 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_person_persontype'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='meli_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]