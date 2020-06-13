# Generated by Django 2.2 on 2020-06-09 07:54

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0006_auto_20200609_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.CharField(choices=[('wm', 'میانگین موزون'), ('f', 'فایفو')], max_length=2),
        ),
        migrations.AlterField(
            model_name='ware',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, editable=False),
        ),
    ]