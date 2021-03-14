# Generated by Django 2.2 on 2021-02-27 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0013_auto_20201110_1413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cheque',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['serial'], 'permissions': (('get.receivedCheque', 'مشاهده چک دریافتی'), ('update.receivedCheque', 'ویرایش چک دریافتی'), ('delete.receivedCheque', 'حذف چک دریافتی'), ('submit.receivedCheque', 'ثبت چک دریافتی'), ('changeStatus.receivedCheque', 'تغییر وضعیت دریافتی'), ('get.paidCheque', 'مشاهده چک پرداختی'), ('update.paidCheque', 'ویرایش چک پرداختی'), ('delete.paidCheque', 'حذف چک پرداختی'), ('submit.paidCheque', 'ثبت چک پرداختی'), ('changeStatus.paidCheque', 'تغییر وضعیت پرداختی'), ('getOwn.receivedCheque', 'مشاهده چک های دریافتی خود'), ('updateOwn.receivedCheque', 'ویرایش چک های دریافتی خود'), ('deleteOwn.receivedCheque', 'حذف چک های دریافتی خود'), ('changeStatusOwn.receivedCheque', 'تغییر وضعیت های دریافتی خود'), ('getOwn.paidCheque', 'مشاهده چک های پرداختی خود'), ('updateOwn.paidCheque', 'ویرایش چک های پرداختی خود'), ('deleteOwn.paidCheque', 'حذف چک های پرداختی خود'), ('changeStatusOwn.paidCheque', 'تغییر وضعیت های پرداختی خود'), ('firstConfirm.receivedCheque', 'تایید اول چک دریافتی'), ('secondConfirm.receivedCheque', 'تایید دوم چک دریافتی'), ('firstConfirmOwn.receivedCheque', 'تایید اول چک های دریافتی خود'), ('secondConfirmOwn.receivedCheque', 'تایید دوم چک های دریافتی خود'), ('firstConfirm.paidCheque', 'تایید اول چک پرداختی '), ('secondConfirm.paidCheque', 'تایید دوم چک پرداختی '), ('firstConfirmOwn.paidCheque', 'تایید اول چک های پرداختی خود'), ('secondConfirmOwn.paidCheque', 'تایید دوم چک های پرداختی خود')), 'verbose_name': 'چک'},
        ),
        migrations.AlterModelOptions(
            name='chequebook',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.chequebook', 'مشاهده دفتر چک'), ('create.chequebook', 'تعریف دفتر چک'), ('update.chequebook', 'ویرایش دفتر چک'), ('delete.chequebook', 'حذف دفتر چک'), ('getOwn.chequebook', 'مشاهده دفتر چک های خود'), ('updateOwn.chequebook', 'ویرایش دفتر چک های خود'), ('deleteOwn.chequebook', 'حذف دفتر چک های خود')), 'verbose_name': 'دفتر چک'},
        ),
        migrations.AlterModelOptions(
            name='statuschange',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['id'], 'permissions': (('delete.receivedChequeStatusChange', 'حذف تغییر وضعیت های چک دریافتی'), ('delete.paidChequeStatusChange', 'حذف تغییر وضعیت های چک پرداختی'), ('deleteOwn.receivedChequeStatusChange', 'حذف تغییر وضعیت های چک دریافتی خود'), ('deleteOwn.paidChequeStatusChange', 'حذف تغییر وضعیت های چک پرداختی خود')), 'verbose_name': 'تغییر وضعیت'},
        ),
    ]