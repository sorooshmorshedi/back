# Generated by Django 2.0.5 on 2019-03-10 09:19

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
            name='Unit',
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
            name='Ware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('barcode', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('isDisabled', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=0, max_digits=24)),
                ('pricingType', models.IntegerField(choices=[(1, 'میانگین موزون'), (0, 'فایفو')])),
                ('minSale', models.IntegerField(blank=True, null=True)),
                ('maxSale', models.IntegerField(blank=True, null=True)),
                ('minInventory', models.IntegerField(blank=True, null=True)),
                ('maxInventory', models.IntegerField(blank=True, null=True)),
                ('created_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
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
            name='WarehouseInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('ware', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory', to='wares.Ware')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory', to='wares.Warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='WareLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('level', models.IntegerField(choices=[(0, 'nature'), (1, 'group'), (2, 'category')])),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='wares.WareLevel')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='ware',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wares', to='wares.WareLevel'),
        ),
        migrations.AddField(
            model_name='ware',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='ware',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wares', to='wares.Unit'),
        ),
        migrations.AddField(
            model_name='ware',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wares', to='wares.Warehouse'),
        ),
        migrations.AlterUniqueTogether(
            name='warelevel',
            unique_together={('name', 'level')},
        ),
        migrations.AlterUniqueTogether(
            name='warehouseinventory',
            unique_together={('warehouse', 'ware')},
        ),
    ]
