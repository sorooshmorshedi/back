# Generated by Django 2.2 on 2021-04-01 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0029_auto_20210305_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleprice',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='wares.SalePriceType'),
        ),
    ]
