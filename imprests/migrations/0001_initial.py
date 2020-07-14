# Generated by Django 2.2 on 2020-07-12 08:37

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0002_auto_20200609_1224'),
        ('companies', '0005_auto_20200614_1141'),
        ('accounts', '0008_auto_20200708_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImprestCheckout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('date', django_jalali.db.models.jDateField()),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False)),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.FinancialYear')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='imprestCheckouts', to='transactions.Transaction')),
            ],
            options={
                'ordering': ['-code'],
                'permissions': (('get.imprestCheckout', 'مشاهده تسویه تنخواه'), ('create.imprestCheckout', 'تعریف تسویه تنخواه'), ('update.imprestCheckout', 'ویرایش تسویه تنخواه'), ('delete.imprestCheckout', 'حذف تسویه تنخواه')),
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ImprestCheckoutItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', django_jalali.db.models.jDateField()),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='imprestCheckoutItems', to='accounts.Account')),
                ('costCenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='imprestCheckoutItemsAsCostCenter', to='accounts.FloatAccount')),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.FinancialYear')),
                ('floatAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='imprestCheckoutItems', to='accounts.FloatAccount')),
                ('imprestCheckout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='imprests.ImprestCheckout')),
            ],
            options={
                'ordering': ['pk'],
                'permissions': (),
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
