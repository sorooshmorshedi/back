# Generated by Django 2.2 on 2020-03-09 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20200309_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='person_type',
            field=models.CharField(blank='true', choices=[('r', 'حقیقی'), ('l', 'حقوقی')], default='', max_length=10),
        ),
    ]
