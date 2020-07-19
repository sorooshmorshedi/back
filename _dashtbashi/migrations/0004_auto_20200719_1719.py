# Generated by Django 2.2 on 2020-07-19 12:49

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0003_auto_20200719_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='association',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='driving',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='driving',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='ladingbillnumber',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='ladingbillnumber',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='ladingbillseries',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='ladingbillseries',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='oilcompanyladingitem',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='oilcompanyladingitem',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True),
        ),
    ]
