# Generated by Django 2.2 on 2019-04-29 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0030_auto_20190429_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='metadata',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wares.WareMetaData'),
        ),
    ]