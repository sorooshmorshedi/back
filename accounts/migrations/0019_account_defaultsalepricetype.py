# Generated by Django 2.2 on 2021-01-26 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0023_auto_20210126_1036'),
        ('accounts', '0018_auto_20210111_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='defaultSalePriceType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='wares.SalePriceType'),
        ),
    ]