# Generated by Django 2.2 on 2022-08-31 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payroll', '0032_auto_20220831_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True)),
                ('is_auto_created', models.BooleanField(default=False)),
                ('is_defined', models.BooleanField(default=False)),
                ('definition_date', models.DateTimeField(blank=True, null=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('lock_date', models.DateTimeField(blank=True, null=True)),
                ('mission_type', models.CharField(choices=[('h', 'ساعتی'), ('d', 'روزانه')], default='d', max_length=2)),
                ('from_date', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('to_date', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('date', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('from_hour', models.TimeField(blank=True, null=True)),
                ('to_hour', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('explanation', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('is_in_payment', models.BooleanField(default=False)),
                ('time_period', models.DecimalField(blank=True, decimal_places=2, max_digits=24, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('defined_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('locked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('workshop_personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mission', to='payroll.WorkshopPersonnel')),
            ],
            options={
                'verbose_name': 'Mission',
                'ordering': ['-pk'],
                'permissions': (('get.mission', 'مشاهده ماموریت'), ('create.mission', 'تعریف ماموریت'), ('update.mission', 'ویرایش ماموریت'), ('delete.mission', 'حذف ماموریت'), ('getOwn.mission', 'مشاهده ماموریت خود'), ('updateOwn.mission', 'ویرایش ماموریت خود'), ('deleteOwn.mission', 'حذف ماموریت خود')),
                'get_latest_by': 'pk',
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
