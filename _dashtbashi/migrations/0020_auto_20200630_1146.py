# Generated by Django 2.2 on 2020-06-30 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0019_auto_20200629_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='LadingBillSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=100)),
                ('from_bill_number', models.IntegerField()),
                ('to_bill_number', models.IntegerField()),
            ],
            options={
                'ordering': ['pk'],
                'permissions': (('get.ladingBillSeries', 'مشاهده سری بارنامه'), ('create.ladingBillSeries', 'تعریف سری بارنامه'), ('update.ladingBillSeries', 'ویرایش سری بارنامه'), ('delete.ladingBillSeries', 'حذف سری بارنامه')),
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.RemoveField(
            model_name='lading',
            name='bill_number',
        ),
        migrations.AddField(
            model_name='lading',
            name='association_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=24),
        ),
        migrations.CreateModel(
            name='LadingBillNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('is_invalid', models.BooleanField(default=False)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numbers', to='_dashtbashi.LadingBillSeries')),
            ],
            options={
                'ordering': ['pk'],
                'permissions': (),
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='lading',
            name='billNumber',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='ladings', to='_dashtbashi.LadingBillNumber'),
            preserve_default=False,
        ),
    ]
