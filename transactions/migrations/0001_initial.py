# Generated by Django 2.2 on 2020-07-19 12:42

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('cheques', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('date', django_jalali.db.models.jDateField()),
                ('explanation', models.CharField(blank=True, max_length=255)),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False)),
                ('type', models.CharField(choices=[('receive', 'دریافت'), ('payment', 'پرداخت'), ('imprest', 'پرداخت تنخواه')], max_length=20)),
            ],
            options={
                'ordering': ['code'],
                'permissions': (('get.receiveTransaction', 'مشاهده دریافت'), ('create.receiveTransaction', 'تعریف دریافت'), ('update.receiveTransaction', 'ویرایش دریافت'), ('delete.receiveTransaction', 'حذف دریافت'), ('get.paymentTransaction', 'مشاهده پرداخت'), ('create.paymentTransaction', 'تعریف پرداخت'), ('update.paymentTransaction', 'ویرایش پرداخت'), ('delete.paymentTransaction', 'حذف پرداخت'), ('get.imprestTransaction', 'مشاهده پرداخت تنخواه'), ('create.imprestTransaction', 'تعریف پرداخت تنخواه'), ('update.imprestTransaction', 'ویرایش پرداخت تنخواه'), ('delete.imprestTransaction', 'حذف پرداخت تنخواه')),
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False)),
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
            ],
            options={
                'ordering': ['pk'],
                'permissions': (),
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
