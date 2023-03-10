# Generated by Django 2.2 on 2020-07-28 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0007_auto_20200728_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanad',
            name='first_confirmed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='first_sanadConfirmer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sanad',
            name='second_confirmed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='second_sanadConfirmer', to=settings.AUTH_USER_MODEL),
        ),
    ]
