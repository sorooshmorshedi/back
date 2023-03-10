# Generated by Django 2.2 on 2020-07-30 04:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('_dashtbashi', '0013_auto_20200730_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='lading',
            name='first_confirmed_at',
            field=django_jalali.db.models.jDateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='lading',
            name='first_confirmed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='first_ladingConfirmer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lading',
            name='second_confirmed_at',
            field=django_jalali.db.models.jDateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='lading',
            name='second_confirmed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='second_ladingConfirmer', to=settings.AUTH_USER_MODEL),
        ),
    ]
