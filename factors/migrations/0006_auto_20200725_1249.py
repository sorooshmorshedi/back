# Generated by Django 2.2 on 2020-07-25 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0005_auto_20200725_1010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'default_permissions': (), 'ordering': ['pk'], 'permissions': (('get.expense', 'مشاهده هزینه فاکتور'), ('create.expense', 'تعریف هزینه  فاکتور'), ('update.expense', 'ویرایش هزینه فاکتور'), ('delete.expense', 'حذف هزینه فاکتور'), ('getOwn.expense', 'مشاهده هزینه های فاکتور خود'), ('updateOwn.expense', 'ویرایش هزینه های فاکتور خود'), ('deleteOwn.expense', 'حذف هزینه های فاکتور خود'))},
        ),
        migrations.AlterModelOptions(
            name='factor',
            options={'default_permissions': (), 'ordering': ['pk'], 'permissions': (('get.buyFactor', 'مشاهده فاکتور خرید'), ('create.buyFactor', 'تعریف فاکتور خرید'), ('update.buyFactor', 'ویرایش فاکتور خرید'), ('delete.buyFactor', 'حذف فاکتور خرید'), ('definite.buyFactor', 'قطعی کردن خرید'), ('get.saleFactor', 'مشاهده فاکتور فروش'), ('create.saleFactor', 'تعریف فاکتور فروش'), ('update.saleFactor', 'ویرایش فاکتور فروش'), ('delete.saleFactor', 'حذف فاکتور فروش'), ('definite.saleFactor', 'قطعی کردن فروش'), ('get.backFromSaleFactor', 'مشاهده فاکتور برگشت از فروش'), ('create.backFromSaleFactor', 'تعریف فاکتور برگشت از فروش'), ('update.backFromSaleFactor', 'ویرایش فاکتور برگشت از فروش'), ('delete.backFromSaleFactor', 'حذف فاکتور برگشت از فروش'), ('definite.backFromSaleFactor', 'قطعی کردن برگشت از فروش'), ('get.backFromBuyFactor', 'مشاهده فاکتور برگشت از خرید'), ('create.backFromBuyFactor', 'تعریف فاکتور برگشت از خرید'), ('update.backFromBuyFactor', 'ویرایش فاکتور برگشت از خرید'), ('delete.backFromBuyFactor', 'حذف فاکتور برگشت از خرید'), ('definite.backFromBuyFactor', 'قطعی کردن برگشت از خرید'), ('get.notPaidFactor', 'مشاهده فاکتور های پرداخت نشده'), ('get.notReceivedFactor', 'مشاهده فاکتور های دریافت نشده'), ('getOwn.buyFactor', 'مشاهده فاکتور خرید خود'), ('updateOwn.buyFactor', 'ویرایش فاکتور های خرید خود'), ('deleteOwn.buyFactor', 'حذف فاکتور های خرید خود'), ('definiteOwn.buyFactor', 'قطعی کردن فاکتور های خرید خود'), ('getOwn.saleFactor', 'مشاهده فاکتور های فروش خود'), ('updateOwn.saleFactor', 'ویرایش فاکتور های فروش خود'), ('deleteOwn.saleFactor', 'حذف فاکتور های فروش خود'), ('definiteOwn.saleFactor', 'قطعی کردن فاکتور های فروش خود'), ('getOwn.backFromSaleFactor', 'مشاهده فاکتور های برگشت از فروش خود'), ('updateOwn.backFromSaleFactor', 'ویرایش فاکتور های برگشت از فروش خود'), ('deleteOwn.backFromSaleFactor', 'حذف فاکتور های برگشت از فروش خود'), ('definiteOwn.backFromSaleFactor', 'قطعی کردن فاکتور های برگشت از فروش خود'), ('getOwn.backFromBuyFactor', 'مشاهده فاکتور های برگشت از خرید خود'), ('updateOwn.backFromBuyFactor', 'ویرایش فاکتور های برگشت از خرید خود'), ('deleteOwn.backFromBuyFactor', 'حذف فاکتور های برگشت از خرید خود'), ('definiteOwn.backFromBuyFactor', 'قطعی کردن فاکتور های برگشت از خرید خود'), ('getOwn.notPaidFactor', 'مشاهده فاکتور های پرداخت نشده خود'), ('getOwn.notReceivedFactor', 'مشاهده فاکتور های دریافت نشده خود'), ('get.firstPeriodInventory', 'مشاهده موجودی اول دوره'), ('update.firstPeriodInventory', 'ثبت موجودی اول دوره'))},
        ),
        migrations.AlterModelOptions(
            name='transfer',
            options={'default_permissions': (), 'ordering': ['pk'], 'permissions': (('get.transfer', 'مشاهده انتقال'), ('create.transfer', 'تعریف انتقال'), ('update.transfer', 'ویرایش انتقال'), ('delete.transfer', 'حذف انتقال'), ('getOwn.transfer', 'مشاهده انتقال های خود'), ('updateOwn.transfer', 'ویرایش انتقال های خود'), ('deleteOwn.transfer', 'حذف انتقال های خود'))},
        ),
    ]
