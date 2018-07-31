# Generated by Django 2.0.5 on 2018-07-29 10:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_bank'),
        ('sanads', '0004_auto_20180729_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True)),
                ('date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('type', models.CharField(choices=[('receive', 'receive'), ('payment', 'payment')], max_length=20)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='accounts.Account')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=0, max_digits=24)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactionItems', to='accounts.Account')),
                ('floatAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactionItems', to='accounts.FloatAccount')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sanads.Transaction')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sanads.RPType')),
            ],
        ),
        migrations.AlterField(
            model_name='sanad',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='sanaditem',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sanadItems', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sanad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='sanads.Sanad'),
        ),
    ]
