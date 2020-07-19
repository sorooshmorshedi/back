# Generated by Django 2.2 on 2020-07-19 12:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('address1', models.CharField(blank=True, max_length=255, null=True)),
                ('address2', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('sabt_number', models.CharField(blank=True, max_length=20, null=True)),
                ('phone1', models.CharField(blank=True, max_length=20, null=True)),
                ('phone2', models.CharField(blank=True, max_length=20, null=True)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='طول کد پستی باید 10 رقم باشد', regex='^.{10}$')])),
                ('eghtesadi_code', models.CharField(blank=True, max_length=20, null=True)),
                ('shenase', models.CharField(blank=True, max_length=20, null=True)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['pk'],
                'permissions': (('get.company', 'مشاهده شرکت'), ('create.company', 'تعریف شرکت'), ('update.company', 'ویرایش شرکت'), ('delete.company', 'حذف شرکت')),
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('start', django_jalali.db.models.jDateField()),
                ('end', django_jalali.db.models.jDateField()),
                ('explanation', models.CharField(blank=True, max_length=255, verbose_name='توضیحات')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='financial_years', to='companies.Company')),
            ],
            options={
                'ordering': ['pk'],
                'permissions': (('get.financialYear', 'مشاهده سال مالی'), ('create.financialYear', 'تعریف سال مالی'), ('update.financialYear', 'ویرایش سال مالی'), ('delete.financialYear', 'حذف سال مالی'), ('move.financialYear', 'انتقال سال مالی'), ('close.financialYear', 'بستن سال مالی'), ('cancelClosing.financialYear', 'لغو بستن سال مالی')),
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
