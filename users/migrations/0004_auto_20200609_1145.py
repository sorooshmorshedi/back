# Generated by Django 2.2 on 2020-06-09 07:15

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_phoneverification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phoneverification',
            options={'get_latest_by': 'id'},
        ),
        migrations.AlterField(
            model_name='phoneverification',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='phoneverification',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False),
        ),
    ]