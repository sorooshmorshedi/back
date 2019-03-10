# Generated by Django 2.0.5 on 2019-03-10 09:19

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
                ('postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('eghtesadi_code', models.CharField(blank=True, max_length=20, null=True)),
                ('shenase', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('start', django_jalali.db.models.jDateField()),
                ('end', django_jalali.db.models.jDateField()),
                ('is_active', models.BooleanField(default=0)),
                ('explanation', models.CharField(blank=True, max_length=255, verbose_name='توضیحات')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='financial_years', to='companies.Company')),
            ],
        ),
    ]
