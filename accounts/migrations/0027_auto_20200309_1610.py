# Generated by Django 2.2 on 2020-03-09 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20200309_1006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'default_permissions': (), 'ordering': ['code']},
        ),
        migrations.RemoveField(
            model_name='account',
            name='person_type',
        ),
    ]
