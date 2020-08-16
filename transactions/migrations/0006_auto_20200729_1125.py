# Generated by Django 2.2 on 2020-07-29 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20200726_0940'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'default_permissions': (), 'ordering': ['code'], 'permissions': (('get.receiveTransaction', 'مشاهده دریافت'), ('create.receiveTransaction', 'تعریف دریافت'), ('update.receiveTransaction', 'ویرایش دریافت'), ('delete.receiveTransaction', 'حذف دریافت'), ('get.paymentTransaction', 'مشاهده پرداخت'), ('create.paymentTransaction', 'تعریف پرداخت'), ('update.paymentTransaction', 'ویرایش پرداخت'), ('delete.paymentTransaction', 'حذف پرداخت'), ('get.imprestTransaction', 'مشاهده پرداخت تنخواه'), ('create.imprestTransaction', 'تعریف پرداخت تنخواه'), ('update.imprestTransaction', 'ویرایش پرداخت تنخواه'), ('delete.imprestTransaction', 'حذف پرداخت تنخواه'), ('firstConfirm.receiveTransaction', 'تایید اول دریافت '), ('secondConfirm.receiveTransaction', 'تایید دوم دریافت '), ('firstConfirmOwn.receiveTransaction', 'تایید اول دریافت های خود'), ('secondConfirmOwn.receiveTransaction', 'تایید دوم دریافت های خود'), ('firstConfirm.paymentTransaction', 'تایید اول پرداخت '), ('secondConfirm.paymentTransaction', 'تایید دوم پرداخت '), ('firstConfirmOwn.paymentTransaction', 'تایید اول پرداخت های خود'), ('secondConfirmOwn.paymentTransaction', 'تایید دوم پرداخت های خود'), ('firstConfirm.imprestTransaction', 'تایید اول تنخواه '), ('secondConfirm.imprestTransaction', 'تایید دوم تنخواه '), ('firstConfirmOwn.imprestTransaction', 'تایید اول تنخواه های خود'), ('secondConfirmOwn.imprestTransaction', 'تایید دوم تنخواه های خود'))},
        ),
    ]