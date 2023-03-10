# Generated by Django 2.2 on 2020-10-01 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0049_auto_20200929_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_association', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='car',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_car', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='driver',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_driver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='driving',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_driving', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lading',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_lading', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ladingbillnumber',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_ladingbillnumber', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ladingbillseries',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_ladingbillseries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='oilcompanylading',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_oilcompanylading', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='oilcompanyladingitem',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_oilcompanyladingitem', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='otherdriverpayment',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_otherdriverpayment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='remittance',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_remittance', to=settings.AUTH_USER_MODEL),
        ),
    ]
