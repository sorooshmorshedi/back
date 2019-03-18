# Generated by Django 2.0.5 on 2019-03-16 11:57

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
                ('type', models.CharField(choices=[('p', 'شخصی'), ('op', 'شخصی سایرین'), ('c', 'شرکت'), ('oc', 'شرکت سایرین')], max_length=1)),
                ('created_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('bankName', models.CharField(blank=True, max_length=100, null=True)),
                ('branchName', models.CharField(blank=True, max_length=100, null=True)),
                ('accountNumber', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['serial'],
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
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='StatusChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', django_jalali.db.models.jDateField()),
                ('explanation', models.CharField(blank=True, max_length=255)),
                ('transferNumber', models.IntegerField(null=True)),
                ('fromStatus', models.CharField(choices=[('blank', 'blank'), ('notPassed', 'notPassed'), ('inFlow', 'inFlow'), ('passed', 'passed'), ('bounced', 'bounced'), ('cashed', 'cashed'), ('revoked', 'revoked'), ('transferred', 'transferred'), ('', 'any')], max_length=30)),
                ('toStatus', models.CharField(choices=[('blank', 'blank'), ('notPassed', 'notPassed'), ('inFlow', 'inFlow'), ('passed', 'passed'), ('bounced', 'bounced'), ('cashed', 'cashed'), ('revoked', 'revoked'), ('transferred', 'transferred'), ('', 'any')], max_length=30)),
                ('created_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('bedAccount', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBedAccount', to='accounts.Account')),
                ('bedFloatAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBesAccount', to='accounts.FloatAccount')),
                ('besAccount', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBedFloatAccount', to='accounts.Account')),
                ('besFloatAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chequeStatusChangesAsBesFloatAccount', to='accounts.FloatAccount')),
                ('cheque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statusChanges', to='cheques.Cheque')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
