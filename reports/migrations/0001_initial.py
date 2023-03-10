# Generated by Django 2.2 on 2022-09-03 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0031_auto_20210718_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportsPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('get.accountBalanceReport', 'مشاهده تراز'), ('get.floatAccountBalanceByGroupReport', 'مشاهده تراز شناور بر اساس گروه'), ('get.floatAccountBalanceReport', 'مشاهده تراز شناور'), ('get.balanceSheetReport', 'مشاهده ترازنامه'), ('get.incomeStatementReport', 'مشاهده گزارش سود و زیان تفصیلی'), ('get.buyReport', 'مشاهده گزارش خرید'), ('get.saleReport', 'مشاهده گزارش فروش'), ('get.wareInventoryReport', 'مشاهده کاردکس کالا'), ('get.allWaresInventoryReport', 'مشاهده کاردکس همه کالا ها'), ('get.warehouseInventoryReport', 'مشاهده کاردکس انبار'), ('get.allWarehousesInventoryReport', 'مشاهده کاردکس همه انبار ها'), ('get.sanadItemsReport', 'مشاهده گزارشات ردیف اسناد (دفتر روزنامه، صورت حساب تفصیلی و دفاتر حساب ها)'), ('get.accountsCodingReport', 'مشاهده گزارش کدینگ حساب ها')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ExportVerifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True)),
                ('is_auto_created', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('post', models.CharField(max_length=255)),
                ('form', models.CharField(choices=[('s', 'سند'), ('fb', 'فاکتور خرید'), ('fs', 'فاکتور فروش'), ('fbfb', 'فاکتور برگشت از خرید'), ('fbfs', 'فاکتور برگشت از فروش'), ('tr', 'دریافت'), ('tp', 'پرداخت'), ('t', 'انتقال'), ('cwr', 'حواله کالای مصرفی'), ('fpi', 'موجودی اول دوره'), ('ia', 'رسید تعدیل انبار'), ('oa', 'حواله تعدیل انبار'), ('pfb', 'پیش فاکتور خرید'), ('pfs', 'پیش فاکتور فروش'), ('frc', 'رسید'), ('frm', 'حواله')], max_length=4)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='export_verifiers', to='companies.FinancialYear')),
            ],
            options={
                'ordering': ['-pk'],
                'permissions': (('create.exportVerifier', 'تعریف تایید کنندگان خروجی'), ('get.exportVerifier', 'مشاهده تایید کنندگان خروجی'), ('update.exportVerifier', 'ویرایش تایید کنندگان خروجی'), ('delete.exportVerifier', 'حذف تایید کنندگان خروجی'), ('getOwn.exportVerifier', 'مشاهده تایید کنندگان خروجی خود'), ('updateOwn.exportVerifier', 'ویرایش تایید کنندگان خروجی خود'), ('deleteOwn.exportVerifier', 'حذف تایید کنندگان خروجی خود')),
                'get_latest_by': 'pk',
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
