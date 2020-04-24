# Generated by Django 2.2 on 2020-04-24 08:26

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=255)),
                ('value', models.DecimalField(blank=True, decimal_places=0, max_digits=24, null=True)),
                ('due', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('date', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('explanation', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('blank', 'blank'), ('notPassed', 'notPassed'), ('inFlow', 'inFlow'), ('passed', 'passed'), ('bounced', 'bounced'), ('cashed', 'cashed'), ('revoked', 'revoked'), ('transferred', 'transferred'), ('', 'any')], max_length=30)),
                ('received_or_paid', models.CharField(choices=[('r', 'دریافتنی'), ('p', 'پرداختنی')], max_length=10)),
                ('type', models.CharField(blank=True, choices=[('p', 'شخصی'), ('op', 'شخصی سایرین'), ('c', 'شرکت'), ('oc', 'شرکت سایرین')], max_length=1)),
                ('created_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('bankName', models.CharField(blank=True, max_length=100, null=True)),
                ('branchName', models.CharField(blank=True, max_length=100, null=True)),
                ('accountNumber', models.CharField(blank=True, max_length=50, null=True)),
                ('has_transaction', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'چک',
                'ordering': ['serial'],
                'permissions': (('get.receivedCheque', 'مشاهده چک دریافتی'), ('update.receivedCheque', 'ویرایش چک دریافتی'), ('delete.receivedCheque', 'حذف چک دریافتی'), ('submit.receivedCheque', 'ثبت چک دریافتی'), ('changeStatus.receivedCheque', 'تغییر وضعیت دریافتی'), ('get.paidCheque', 'مشاهده چک پرداختی'), ('update.paidCheque', 'ویرایش چک پرداختی'), ('delete.paidCheque', 'حذف چک پرداختی'), ('submit.paidCheque', 'ثبت چک پرداختی'), ('changeStatus.paidCheque', 'تغییر وضعیت پرداختی')),
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Chequebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True)),
                ('explanation', models.CharField(blank=True, max_length=255)),
                ('serial_from', models.IntegerField()),
                ('serial_to', models.IntegerField()),
            ],
            options={
                'verbose_name': 'دفتر چک',
                'ordering': ['code'],
                'permissions': (('get.chequebook', 'مشاهده دفتر چک'), ('create.chequebook', 'تعریف دفتر چک'), ('update.chequebook', 'ویرایش دفتر چک'), ('delete.chequebook', 'حذف دفتر چک')),
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='StatusChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', django_jalali.db.models.jDateField()),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('transferNumber', models.IntegerField(null=True)),
                ('fromStatus', models.CharField(choices=[('blank', 'blank'), ('notPassed', 'notPassed'), ('inFlow', 'inFlow'), ('passed', 'passed'), ('bounced', 'bounced'), ('cashed', 'cashed'), ('revoked', 'revoked'), ('transferred', 'transferred'), ('', 'any')], max_length=30)),
                ('toStatus', models.CharField(choices=[('blank', 'blank'), ('notPassed', 'notPassed'), ('inFlow', 'inFlow'), ('passed', 'passed'), ('bounced', 'bounced'), ('cashed', 'cashed'), ('revoked', 'revoked'), ('transferred', 'transferred'), ('', 'any')], max_length=30)),
                ('created_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('bedAccount', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBedAccount', to='accounts.Account')),
                ('bedCostCenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBesAccountAsCostCenter', to='accounts.FloatAccount')),
                ('bedFloatAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBesAccount', to='accounts.FloatAccount')),
                ('besAccount', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBedFloatAccount', to='accounts.Account')),
                ('besCostCenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBesFloatAccountAsCostCenter', to='accounts.FloatAccount')),
                ('besFloatAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBesFloatAccount', to='accounts.FloatAccount')),
                ('cheque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statusChanges', to='cheques.Cheque')),
            ],
            options={
                'verbose_name': 'تغییر وضعیت',
                'ordering': ['id'],
                'permissions': (('delete.receivedChequeStatusChange', 'حذف تغییر وضعیت های چک دریافتی'), ('delete.paidChequeStatusChange', 'حذف تغییر وضعیت های چک پرداختی')),
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
