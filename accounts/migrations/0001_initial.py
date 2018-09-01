# Generated by Django 2.0.5 on 2018-09-01 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('max_bed', models.IntegerField(blank=True, null=True)),
                ('max_bes', models.IntegerField(blank=True, null=True)),
                ('max_bed_with_sanad', models.IntegerField(blank=True, null=True)),
                ('max_bes_with_sanad', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now=True, null=True)),
                ('updated_at', models.DateField(auto_now_add=True, null=True)),
                ('level', models.IntegerField(choices=[(0, 'group'), (1, 'kol'), (2, 'moein'), (3, 'tafzili')])),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(choices=[('BED', 'bedehkar'), ('BES', 'bestankar')], max_length=3)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CostCenterGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='DefaultAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('explanation', models.TextField(blank=True, null=True)),
                ('usage', models.CharField(choices=[('receive', 'دریافت'), ('payment', 'پرداخت'), ('receiveAndPayment', 'دریافت و پرداخت'), ('factor', 'فاکتور')], max_length=20)),
                ('programingName', models.CharField(blank=True, max_length=50, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FloatAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('max_bed', models.CharField(blank=True, max_length=20, null=True)),
                ('max_bes', models.CharField(blank=True, max_length=20, null=True)),
                ('max_bed_with_sanad', models.CharField(blank=True, max_length=20, null=True)),
                ('max_bes_with_sanad', models.CharField(blank=True, max_length=20, null=True)),
                ('is_disabled', models.BooleanField(default=False)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='FloatAccountGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='IndependentAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='bank', serialize=False, to='accounts.Account')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('branch', models.CharField(blank=True, max_length=100, null=True)),
                ('branchCode', models.CharField(blank=True, max_length=20, null=True)),
                ('accountNumber', models.CharField(blank=True, max_length=50, null=True)),
                ('sheba', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='person', serialize=False, to='accounts.Account')),
                ('phone1', models.CharField(blank=True, max_length=20, null=True)),
                ('phone2', models.CharField(blank=True, max_length=20, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address1', models.CharField(blank=True, max_length=255, null=True)),
                ('address2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('province', models.CharField(blank=True, max_length=255, null=True)),
                ('postalCode', models.CharField(blank=True, max_length=20, null=True)),
                ('accountNumber1', models.CharField(blank=True, max_length=50, null=True)),
                ('accountNumber2', models.CharField(blank=True, max_length=50, null=True)),
                ('eghtesadiCode', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(choices=[('buyer', 'buyer'), ('seller', 'seller')], max_length=10)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='floataccount',
            name='floatAccountGroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='floatAccounts', to='accounts.FloatAccountGroup'),
        ),
        migrations.AddField(
            model_name='defaultaccount',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='defaultAccount', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='costcenter',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='costCenters', to='accounts.CostCenterGroup'),
        ),
        migrations.AddField(
            model_name='account',
            name='costCenterGroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='accounts', to='accounts.CostCenterGroup'),
        ),
        migrations.AddField(
            model_name='account',
            name='floatAccountGroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='accounts', to='accounts.FloatAccountGroup'),
        ),
        migrations.AddField(
            model_name='account',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts', to='accounts.AccountType'),
        ),
    ]
