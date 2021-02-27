# Generated by Django 2.2 on 2021-02-27 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0041_factor_path'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adjustment',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.adjustment', 'مشاهده تعدیل '), ('create.adjustment', 'تعریف تعدیل '), ('update.adjustment', 'ویرایش تعدیل '), ('delete.adjustment', 'حذف تعدیل '), ('getOwn.adjustment', 'مشاهده تعدیل های خود'), ('updateOwn.adjustment', 'ویرایش تعدیل های خود'), ('deleteOwn.adjustment', 'حذف تعدیل های خود'))},
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.expense', 'مشاهده هزینه فاکتور'), ('create.expense', 'تعریف هزینه  فاکتور'), ('update.expense', 'ویرایش هزینه فاکتور'), ('delete.expense', 'حذف هزینه فاکتور'), ('getOwn.expense', 'مشاهده هزینه های فاکتور خود'), ('updateOwn.expense', 'ویرایش هزینه های فاکتور خود'), ('deleteOwn.expense', 'حذف هزینه های فاکتور خود'))},
        ),
        migrations.AlterModelOptions(
            name='factor',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.buyFactor', 'مشاهده فاکتور خرید'), ('create.buyFactor', 'تعریف فاکتور خرید'), ('update.buyFactor', 'ویرایش فاکتور خرید'), ('delete.buyFactor', 'حذف فاکتور خرید'), ('definite.buyFactor', 'قطعی کردن خرید'), ('get.saleFactor', 'مشاهده فاکتور فروش'), ('create.saleFactor', 'تعریف فاکتور فروش'), ('update.saleFactor', 'ویرایش فاکتور فروش'), ('delete.saleFactor', 'حذف فاکتور فروش'), ('definite.saleFactor', 'قطعی کردن فروش'), ('get.backFromSaleFactor', 'مشاهده فاکتور برگشت از فروش'), ('create.backFromSaleFactor', 'تعریف فاکتور برگشت از فروش'), ('update.backFromSaleFactor', 'ویرایش فاکتور برگشت از فروش'), ('delete.backFromSaleFactor', 'حذف فاکتور برگشت از فروش'), ('definite.backFromSaleFactor', 'قطعی کردن برگشت از فروش'), ('get.backFromBuyFactor', 'مشاهده فاکتور برگشت از خرید'), ('create.backFromBuyFactor', 'تعریف فاکتور برگشت از خرید'), ('update.backFromBuyFactor', 'ویرایش فاکتور برگشت از خرید'), ('delete.backFromBuyFactor', 'حذف فاکتور برگشت از خرید'), ('definite.backFromBuyFactor', 'قطعی کردن برگشت از خرید'), ('get.consumptionWareFactor', 'مشاهده حواله کالای مصرفی'), ('create.consumptionWareFactor', 'تعریف حواله کالای مصرفی'), ('update.consumptionWareFactor', 'ویرایش حواله کالای مصرفی'), ('delete.consumptionWareFactor', 'حذف حواله کالای مصرفی'), ('definite.consumptionWareFactor', 'قطعی کردن حواله کالای مصرفی'), ('get.notPaidFactor', 'مشاهده فاکتور های پرداخت نشده'), ('get.notReceivedFactor', 'مشاهده فاکتور های دریافت نشده'), ('getOwn.buyFactor', 'مشاهده فاکتور خرید خود'), ('updateOwn.buyFactor', 'ویرایش فاکتور های خرید خود'), ('deleteOwn.buyFactor', 'حذف فاکتور های خرید خود'), ('definiteOwn.buyFactor', 'قطعی کردن فاکتور های خرید خود'), ('getOwn.saleFactor', 'مشاهده فاکتور های فروش خود'), ('updateOwn.saleFactor', 'ویرایش فاکتور های فروش خود'), ('deleteOwn.saleFactor', 'حذف فاکتور های فروش خود'), ('definiteOwn.saleFactor', 'قطعی کردن فاکتور های فروش خود'), ('getOwn.backFromSaleFactor', 'مشاهده فاکتور های برگشت از فروش خود'), ('updateOwn.backFromSaleFactor', 'ویرایش فاکتور های برگشت از فروش خود'), ('deleteOwn.backFromSaleFactor', 'حذف فاکتور های برگشت از فروش خود'), ('definiteOwn.backFromSaleFactor', 'قطعی کردن فاکتور های برگشت از فروش خود'), ('getOwn.backFromBuyFactor', 'مشاهده فاکتور های برگشت از خرید خود'), ('updateOwn.backFromBuyFactor', 'ویرایش فاکتور های برگشت از خرید خود'), ('deleteOwn.backFromBuyFactor', 'حذف فاکتور های برگشت از خرید خود'), ('definiteOwn.backFromBuyFactor', 'قطعی کردن فاکتور های برگشت از خرید خود'), ('getOwn.consumptionWareFactor', 'مشاهده حواله کالای مصرفی خود'), ('updateOwn.consumptionWareFactor', 'ویرایش حواله کالای مصرفی خود'), ('deleteOwn.consumptionWareFactor', 'حذف حواله کالای مصرفی خود'), ('definiteOwn.consumptionWareFactor', 'قطعی کردن حواله کالای مصرفی خود'), ('getOwn.notPaidFactor', 'مشاهده فاکتور های پرداخت نشده خود'), ('getOwn.notReceivedFactor', 'مشاهده فاکتور های دریافت نشده خود'), ('get.firstPeriodInventory', 'مشاهده موجودی اول دوره'), ('update.firstPeriodInventory', 'ثبت موجودی اول دوره'), ('firstConfirm.buyFactor', 'تایید اول فاکتور خرید '), ('secondConfirm.buyFactor', 'تایید دوم فاکتور خرید '), ('firstConfirmOwn.buyFactor', 'تایید اول فاکتور های خرید خود'), ('secondConfirmOwn.buyFactor', 'تایید دوم فاکتور های خرید خود'), ('firstConfirm.saleFactor', 'تایید اول فاکتور فروش '), ('secondConfirm.saleFactor', 'تایید دوم فاکتور فروش '), ('firstConfirmOwn.saleFactor', 'تایید اول فاکتور های فروش خود'), ('secondConfirmOwn.saleFactor', 'تایید دوم فاکتور های فروش خود'), ('firstConfirm.backFromBuyFactor', 'تایید اول فاکتور برگشت از خرید'), ('secondConfirm.backFromBuyFactor', 'تایید دوم فاکتور برگشت از خرید'), ('firstConfirmOwn.backFromBuyFactor', 'تایید اول فاکتور های برگشت از خرید خود'), ('secondConfirmOwn.backFromBuyFactor', 'تایید دوم فاکتور های برگشت از خرید خود'), ('firstConfirm.backFromSaleFromSaleFactor', 'تایید اول فاکتور برگشت از فروش '), ('secondConfirm.backFromSaleFromSaleFactor', 'تایید دوم فاکتور برگشت از فروش '), ('firstConfirmOwn.backFromSaleFromSaleFactor', 'تایید اول فاکتور های برگشت از فروش خود'), ('secondConfirmOwn.backFromSaleFromSaleFactor', 'تایید دوم فاکتور های برگشت از فروش خود'), ('firstConfirm.consumptionWareFactor', 'تایید اولحواله کالای مصرفی'), ('secondConfirm.consumptionWareFactor', 'تایید دومحواله کالای مصرفی'), ('firstConfirmOwn.consumptionWareFactor', 'تایید اول حواله کالای مصرفی خود'), ('secondConfirmOwn.consumptionWareFactor', 'تایید دوم حواله کالای مصرفی خود'))},
        ),
        migrations.AlterModelOptions(
            name='factorexpense',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.factorExpenses', 'مشاهده هزینه های فاکتور'), ('create.factorExpenses', 'تعریف هزینه های فاکتور'), ('update.factorExpenses', 'ویرایش هزینه های فاکتور'), ('delete.factorExpenses', 'حذف هزینه های فاکتور'), ('getOwn.factorExpenses', 'مشاهده هزینه های فاکتور خود'), ('updateOwn.factorExpenses', 'ویرایش هزینه های فاکتور خود'), ('deleteOwn.factorExpenses', 'حذف هزینه های فاکتور خود'))},
        ),
        migrations.AlterModelOptions(
            name='factoritem',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='factorpayment',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='transfer',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.transfer', 'مشاهده انتقال'), ('create.transfer', 'تعریف انتقال'), ('update.transfer', 'ویرایش انتقال'), ('delete.transfer', 'حذف انتقال'), ('getOwn.transfer', 'مشاهده انتقال های خود'), ('updateOwn.transfer', 'ویرایش انتقال های خود'), ('deleteOwn.transfer', 'حذف انتقال های خود'))},
        ),
        migrations.AlterModelOptions(
            name='warehousehandling',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.warehouseHandling', 'مشاهده انبار گردانی'), ('create.warehouseHandling', 'تعریف انبار گردانی'), ('update.warehouseHandling', 'ویرایش انبار گردانی'), ('delete.warehouseHandling', 'حذف انبار گردانی'))},
        ),
        migrations.AlterModelOptions(
            name='warehousehandlingitem',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': ()},
        ),
    ]
