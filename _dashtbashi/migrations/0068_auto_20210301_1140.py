# Generated by Django 2.2 on 2021-03-01 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0067_merge_20210301_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='car',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='driver',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='driving',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lading',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ladingbillnumber',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ladingbillseries',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='oilcompanylading',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='oilcompanyladingitem',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='otherdriverpayment',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='remittance',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
