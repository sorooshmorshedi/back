# Generated by Django 2.2 on 2020-11-07 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0054_oilcompanylading_net_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='lading',
            name='local_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oilcompanylading',
            name='local_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='otherdriverpayment',
            name='local_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='remittance',
            name='local_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]