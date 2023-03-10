# Generated by Django 2.2 on 2021-07-18 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sanads', '0031_auto_20210707_1444'),
        ('factors', '0059_auto_20210706_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='has_aggregated_sanad',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='factor',
            name='has_auto_sanad',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='adjustment',
            name='explanation',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='warehousehandling',
            name='explanation',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='warehousehandlingitem',
            name='explanation',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.CreateModel(
            name='FactorsAggregatedSanad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True)),
                ('is_auto_created', models.BooleanField(default=False)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('date', django_jalali.db.models.jDateField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('sanad', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='factorsAggregatedSanad', to='sanads.Sanad')),
            ],
            options={
                'ordering': ['-pk'],
                'permissions': (),
                'get_latest_by': 'pk',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='factor',
            name='aggregatedSanad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factors', to='factors.FactorsAggregatedSanad'),
        ),
    ]
