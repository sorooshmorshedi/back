# Generated by Django 2.2 on 2020-04-24 08:26

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sanads', '0001_initial'),
        ('cheques', '0001_initial'),
        ('accounts', '0001_initial'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('date', django_jalali.db.models.jDateField()),
                ('explanation', models.CharField(blank=True, max_length=255)),
                ('created_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('type', models.CharField(choices=[('receive', 'دریافت'), ('payment', 'پرداخت')], max_length=20)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='accounts.Account')),
                ('costCenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactionsAsCostCenter', to='accounts.FloatAccount')),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='companies.FinancialYear')),
                ('floatAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='accounts.FloatAccount')),
                ('sanad', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='sanads.Sanad')),
            ],
            options={
                'ordering': ['code'],
                'permissions': (('get.receiveTransaction', 'مشاهده دریافت'), ('create.receiveTransaction', 'تعریف دریافت'), ('update.receiveTransaction', 'ویرایش دریافت'), ('delete.receiveTransaction', 'حذف دریافت'), ('get.paymentTransaction', 'مشاهده پرداخت'), ('create.paymentTransaction', 'تعریف پرداخت'), ('update.paymentTransaction', 'ویرایش پرداخت'), ('delete.paymentTransaction', 'حذف پرداخت')),
                'abstract': False,
                'default_permissions': (),
                'unique_together': {('code', 'type')},
            },
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=0, max_digits=24)),
                ('date', django_jalali.db.models.jDateField()),
                ('due', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('documentNumber', models.CharField(blank=True, max_length=50, null=True)),
                ('bankName', models.CharField(blank=True, max_length=255, null=True)),
                ('explanation', models.CharField(blank=True, default='', max_length=255)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactionItems', to='accounts.Account')),
                ('cheque', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactionItem', to='cheques.Cheque')),
                ('costCenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactionItemsAsCostCenter', to='accounts.FloatAccount')),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionItems', to='companies.FinancialYear')),
                ('floatAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactionItems', to='accounts.FloatAccount')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='transactions.Transaction')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.DefaultAccount')),
            ],
            options={
                'ordering': ['pk'],
                'permissions': (),
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]