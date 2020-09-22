# Generated by Django 2.2 on 2020-09-19 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0010_auto_20200816_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='superuser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='companies', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]