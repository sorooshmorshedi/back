# Generated by Django 2.2 on 2020-09-06 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0006_auto_20200726_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='ware',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wares', to='wares.Warehouse'),
        ),
    ]
