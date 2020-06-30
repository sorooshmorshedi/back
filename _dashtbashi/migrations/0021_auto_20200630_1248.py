# Generated by Django 2.2 on 2020-06-30 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0020_auto_20200630_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lading',
            name='destination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ladingDestinations', to='users.City'),
        ),
        migrations.AlterField(
            model_name='lading',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ladingOrigins', to='users.City'),
        ),
    ]
