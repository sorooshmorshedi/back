# Generated by Django 2.0.5 on 2018-08-21 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0009_auto_20180821_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='factoritem',
            name='factor',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='factors.Factor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='factoritem',
            name='wareHouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='factorItems', to='wares.WareHouse'),
        ),
    ]
