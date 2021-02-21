# Generated by Django 2.2 on 2021-01-21 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('wares', '0017_auto_20210103_1128'),
        ('factors', '0034_warehousehandling_submit_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='factoritem',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='factorItems',
                                    to='wares.Unit'),
        ),
        migrations.AddField(
            model_name='factoritem',
            name='unit_count',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
            preserve_default=False,
        ),
    ]