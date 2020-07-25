# Generated by Django 2.2 on 2020-07-25 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0006_auto_20200723_1559'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cheque',
            options={'default_permissions': (), 'ordering': ['serial'], 'permissions': (('get.receivedCheque', 'مشاهده چک دریافتی'), ('update.receivedCheque', 'ویرایش چک دریافتی'), ('delete.receivedCheque', 'حذف چک دریافتی'), ('submit.receivedCheque', 'ثبت چک دریافتی'), ('changeStatus.receivedCheque', 'تغییر وضعیت دریافتی'), ('get.paidCheque', 'مشاهده چک پرداختی'), ('update.paidCheque', 'ویرایش چک پرداختی'), ('delete.paidCheque', 'حذف چک پرداختی'), ('submit.paidCheque', 'ثبت چک پرداختی'), ('changeStatus.paidCheque', 'تغییر وضعیت پرداختی'), ('getOwn.receivedCheque', 'مشاهده چک های دریافتی خود'), ('updateOwn.receivedCheque', 'ویرایش چک های دریافتی خود'), ('deleteOwn.receivedCheque', 'حذف چک های دریافتی خود'), ('changeStatusOwn.receivedCheque', 'تغییر وضعیت های دریافتی خود'), ('getOwn.paidCheque', 'مشاهده چک های پرداختی خود'), ('updateOwn.paidCheque', 'ویرایش چک های پرداختی خود'), ('deleteOwn.paidCheque', 'حذف چک های پرداختی خود'), ('changeStatusOwn.paidCheque', 'تغییر وضعیت های پرداختی خود')), 'verbose_name': 'چک'},
        ),
        migrations.AlterModelOptions(
            name='statuschange',
            options={'default_permissions': (), 'ordering': ['id'], 'permissions': (('delete.receivedChequeStatusChange', 'حذف تغییر وضعیت های چک دریافتی'), ('delete.paidChequeStatusChange', 'حذف تغییر وضعیت های چک پرداختی'), ('deleteOwn.receivedChequeStatusChange', 'حذف تغییر وضعیت های چک دریافتی خود'), ('deleteOwn.paidChequeStatusChange', 'حذف تغییر وضعیت های چک پرداختی خود')), 'verbose_name': 'تغییر وضعیت'},
        ),
    ]
