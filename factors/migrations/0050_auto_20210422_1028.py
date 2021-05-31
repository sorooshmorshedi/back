# Generated by Django 2.2 on 2021-04-22 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0049_auto_20210415_0846'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='factor',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.buyFactor', 'مشاهده فاکتور خرید'), ('create.buyFactor', 'تعریف فاکتور خرید'), ('update.buyFactor', 'ویرایش فاکتور خرید'), ('delete.buyFactor', 'حذف فاکتور خرید'), ('definite.buyFactor', 'قطعی کردن خرید'), ('get.saleFactor', 'مشاهده فاکتور فروش'), ('create.saleFactor', 'تعریف فاکتور فروش'), ('update.saleFactor', 'ویرایش فاکتور فروش'), ('delete.saleFactor', 'حذف فاکتور فروش'), ('definite.saleFactor', 'قطعی کردن فروش'), ('get.backFromSaleFactor', 'مشاهده فاکتور برگشت از فروش'), ('create.backFromSaleFactor', 'تعریف فاکتور برگشت از فروش'), ('update.backFromSaleFactor', 'ویرایش فاکتور برگشت از فروش'), ('delete.backFromSaleFactor', 'حذف فاکتور برگشت از فروش'), ('definite.backFromSaleFactor', 'قطعی کردن برگشت از فروش'), ('get.backFromBuyFactor', 'مشاهده فاکتور برگشت از خرید'), ('create.backFromBuyFactor', 'تعریف فاکتور برگشت از خرید'), ('update.backFromBuyFactor', 'ویرایش فاکتور برگشت از خرید'), ('delete.backFromBuyFactor', 'حذف فاکتور برگشت از خرید'), ('definite.backFromBuyFactor', 'قطعی کردن برگشت از خرید'), ('get.consumptionWareFactor', 'مشاهده حواله کالای مصرفی'), ('create.consumptionWareFactor', 'تعریف حواله کالای مصرفی'), ('update.consumptionWareFactor', 'ویرایش حواله کالای مصرفی'), ('delete.consumptionWareFactor', 'حذف حواله کالای مصرفی'), ('definite.consumptionWareFactor', 'قطعی کردن حواله کالای مصرفی'), ('get.notPaidFactor', 'مشاهده فاکتور های پرداخت نشده'), ('get.notReceivedFactor', 'مشاهده فاکتور های دریافت نشده'), ('getOwn.buyFactor', 'مشاهده فاکتور خرید خود'), ('updateOwn.buyFactor', 'ویرایش فاکتور های خرید خود'), ('deleteOwn.buyFactor', 'حذف فاکتور های خرید خود'), ('definiteOwn.buyFactor', 'قطعی کردن فاکتور های خرید خود'), ('getOwn.saleFactor', 'مشاهده فاکتور های فروش خود'), ('updateOwn.saleFactor', 'ویرایش فاکتور های فروش خود'), ('deleteOwn.saleFactor', 'حذف فاکتور های فروش خود'), ('definiteOwn.saleFactor', 'قطعی کردن فاکتور های فروش خود'), ('getOwn.backFromSaleFactor', 'مشاهده فاکتور های برگشت از فروش خود'), ('updateOwn.backFromSaleFactor', 'ویرایش فاکتور های برگشت از فروش خود'), ('deleteOwn.backFromSaleFactor', 'حذف فاکتور های برگشت از فروش خود'), ('definiteOwn.backFromSaleFactor', 'قطعی کردن فاکتور های برگشت از فروش خود'), ('getOwn.backFromBuyFactor', 'مشاهده فاکتور های برگشت از خرید خود'), ('updateOwn.backFromBuyFactor', 'ویرایش فاکتور های برگشت از خرید خود'), ('deleteOwn.backFromBuyFactor', 'حذف فاکتور های برگشت از خرید خود'), ('definiteOwn.backFromBuyFactor', 'قطعی کردن فاکتور های برگشت از خرید خود'), ('getOwn.consumptionWareFactor', 'مشاهده حواله کالای مصرفی خود'), ('updateOwn.consumptionWareFactor', 'ویرایش حواله کالای مصرفی خود'), ('deleteOwn.consumptionWareFactor', 'حذف حواله کالای مصرفی خود'), ('definiteOwn.consumptionWareFactor', 'قطعی کردن حواله کالای مصرفی خود'), ('getOwn.notPaidFactor', 'مشاهده فاکتور های پرداخت نشده خود'), ('getOwn.notReceivedFactor', 'مشاهده فاکتور های دریافت نشده خود'), ('get.firstPeriodInventory', 'مشاهده موجودی اول دوره'), ('update.firstPeriodInventory', 'ثبت موجودی اول دوره'), ('firstConfirm.buyFactor', 'تایید اول فاکتور خرید '), ('secondConfirm.buyFactor', 'تایید دوم فاکتور خرید '), ('firstConfirmOwn.buyFactor', 'تایید اول فاکتور های خرید خود'), ('secondConfirmOwn.buyFactor', 'تایید دوم فاکتور های خرید خود'), ('firstConfirm.saleFactor', 'تایید اول فاکتور فروش '), ('secondConfirm.saleFactor', 'تایید دوم فاکتور فروش '), ('firstConfirmOwn.saleFactor', 'تایید اول فاکتور های فروش خود'), ('secondConfirmOwn.saleFactor', 'تایید دوم فاکتور های فروش خود'), ('firstConfirm.backFromBuyFactor', 'تایید اول فاکتور برگشت از خرید'), ('secondConfirm.backFromBuyFactor', 'تایید دوم فاکتور برگشت از خرید'), ('firstConfirmOwn.backFromBuyFactor', 'تایید اول فاکتور های برگشت از خرید خود'), ('secondConfirmOwn.backFromBuyFactor', 'تایید دوم فاکتور های برگشت از خرید خود'), ('firstConfirm.backFromSaleFromSaleFactor', 'تایید اول فاکتور برگشت از فروش '), ('secondConfirm.backFromSaleFromSaleFactor', 'تایید دوم فاکتور برگشت از فروش '), ('firstConfirmOwn.backFromSaleFromSaleFactor', 'تایید اول فاکتور های برگشت از فروش خود'), ('secondConfirmOwn.backFromSaleFromSaleFactor', 'تایید دوم فاکتور های برگشت از فروش خود'), ('firstConfirm.consumptionWareFactor', 'تایید اولحواله کالای مصرفی'), ('secondConfirm.consumptionWareFactor', 'تایید دومحواله کالای مصرفی'), ('firstConfirmOwn.consumptionWareFactor', 'تایید اول حواله کالای مصرفی خود'), ('secondConfirmOwn.consumptionWareFactor', 'تایید دوم حواله کالای مصرفی خود'), ('create.buyPreFactor', 'تعریف پیش فاکتور خرید'), ('get.buyPreFactor', 'مشاهده پیش فاکتور خرید'), ('update.buyPreFactor', 'ویرایش پیش فاکتور خرید'), ('delete.buyPreFactor', 'حذف پیش فاکتور خرید'), ('convert.buyPreFactor', 'تبدیل پیش فاکتور خرید به فاکتور'), ('getOwn.buyPreFactor', 'مشاهده پیش فاکتور خرید خود'), ('updateOwn.buyPreFactor', 'ویرایش پیش فاکتور خرید خود'), ('deleteOwn.buyPreFactor', 'حذف پیش فاکتور خرید خود'), ('convertOwn.buyPreFactor', 'تبدیل پیش فاکتور خرید خود به فاکتور'), ('create.salePreFactor', 'تعریف پیش فاکتور فروش'), ('get.salePreFactor', 'مشاهده پیش فاکتور فروش'), ('update.salePreFactor', 'ویرایش پیش فاکتور فروش'), ('delete.salePreFactor', 'حذف پیش فاکتور فروش'), ('convert.salePreFactor', 'تبدیل پیش فاکتور فروش به فاکتور'), ('getOwn.salePreFactor', 'مشاهده پیش فاکتور فروش خود'), ('updateOwn.salePreFactor', 'ویرایش پیش فاکتور فروش خود'), ('deleteOwn.salePreFactor', 'حذف پیش فاکتور فروش خود'), ('convertOwn.salePreFactor', 'تبدیل پیش فاکتور فروش خود به فاکتور'), ('create.receipt', 'تعریف رسید'), ('get.receipt', 'مشاهده رسید'), ('update.receipt', 'ویرایش رسید'), ('delete.receipt', 'حذف رسید'), ('getOwn.receipt', 'مشاهده رسید های خود'), ('updateOwn.receipt', 'ویرایش رسید های خود'), ('deleteOwn.receipt', 'حذف رسید های خود'), ('create.remittance', 'تعریف حواله'), ('get.remittance', 'مشاهده حواله'), ('update.remittance', 'ویرایش حواله'), ('delete.remittance', 'حذف حواله'), ('getOwn.remittance', 'مشاهده حواله های خود'), ('updateOwn.remittance', 'ویرایش حواله های خود'), ('deleteOwn.remittance', 'حذف حواله های خود'))},
        ),
    ]