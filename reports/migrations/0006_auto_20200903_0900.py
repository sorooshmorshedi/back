# Generated by Django 2.2 on 2020-09-03 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20200726_0940'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'default_permissions': (), 'managed': False, 'ordering': ['pk'], 'permissions': (('get.accountBalanceReport', 'مشاهده تراز'), ('get.floatAccountBalanceByGroupReport', 'مشاهده تراز شناور بر اساس گروه'), ('get.floatAccountBalanceReport', 'مشاهده تراز شناور'), ('get.balanceSheetReport', 'مشاهده ترازنامه'), ('get.buyReport', 'مشاهده گزارش خرید'), ('get.saleReport', 'مشاهده گزارش فروش'), ('get.incomeStatementReport', 'مشاهده گزارش سود و زیان تفصیلی'), ('get.wareInventoryReport', 'مشاهده کاردکس کالا'), ('get.allWaresInventoryReport', 'مشاهده کاردکس همه کالا ها'), ('get.warehouseInventoryReport', 'مشاهده کاردکس انبار'), ('get.allWarehousesInventoryReport', 'مشاهده کاردکس همه انبار ها'), ('get.sanadItemsReport', 'مشاهده گزارشات ردیف اسناد (دفتر روزنامه، صورت حساب تفصیلی و دفاتر حساب ها)'))},
        ),
    ]
