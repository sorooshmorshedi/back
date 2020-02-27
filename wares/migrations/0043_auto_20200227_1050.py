# Generated by Django 2.2 on 2020-02-27 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0042_ware_isservice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='warehouse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='wares', to='wares.Warehouse'),
        ),
    ]
