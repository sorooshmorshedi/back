# Generated by Django 2.2 on 2021-08-15 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0022_auto_20210719_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['code'], 'permissions': (('get.receiveTransaction', 'مشاهده دریافت'), ('create.receiveTransaction', 'تعریف دریافت'), ('update.receiveTransaction', 'ویرایش دریافت'), ('delete.receiveTransaction', 'حذف دریافت'), ('define.receiveTransaction', 'قطعی کردن دریافت'), ('lock.receiveTransaction', 'قفل کردن دریافت'), ('get.paymentTransaction', 'مشاهده پرداخت'), ('create.paymentTransaction', 'تعریف پرداخت'), ('update.paymentTransaction', 'ویرایش پرداخت'), ('delete.paymentTransaction', 'حذف پرداخت'), ('define.paymentTransaction', 'قطعی کردن پرداخت'), ('lock.paymentTransaction', 'قفل کردن پرداخت'), ('get.bankTransferTransaction', 'مشاهده پرداخت بین بانک ها'), ('create.bankTransferTransaction', 'تعریف پرداخت بین بانک ها'), ('update.bankTransferTransaction', 'ویرایش پرداخت بین بانک ها'), ('delete.bankTransferTransaction', 'حذف پرداخت بین بانک ها'), ('define.bankTransferTransaction', 'قطعی کردن پرداخت بین بانک ها'), ('lock.bankTransferTransaction', 'قفل کردن پرداخت بین بانک ها'), ('get.imprestTransaction', 'مشاهده پرداخت تنخواه'), ('create.imprestTransaction', 'تعریف پرداخت تنخواه'), ('update.imprestTransaction', 'ویرایش پرداخت تنخواه'), ('delete.imprestTransaction', 'حذف پرداخت تنخواه'), ('define.imprestTransaction', 'قطعی کردن پرداخت تنخواه'), ('lock.imprestTransaction', 'قفل کردن پرداخت تنخواه'), ('getOwn.receiveTransaction', 'مشاهده دریافت های خود'), ('updateOwn.receiveTransaction', 'ویرایش دریافت های خود'), ('deleteOwn.receiveTransaction', 'حذف دریافت های خود'), ('defineOwn.receiveTransaction', 'قطعی کردن دریافت های خود'), ('lockOwn.receiveTransaction', 'قفل کردن دریافت های خود'), ('getOwn.paymentTransaction', 'مشاهده پرداخت های خود'), ('updateOwn:.paymentTransaction', 'ویرایش پرداخت های خود'), ('deleteOwn.paymentTransaction', 'حذف پرداخت های خود'), ('defineOwn.paymentTransaction', 'قطعی کردن پرداخت های خود'), ('lockOwn.paymentTransaction', 'قفل کردن پرداخت های خود'), ('getOwn.bankTransferTransaction', 'مشاهده پرداخت های بین بانک های خود'), ('updateOwn:.bankTransferTransaction', 'ویرایش پرداخت های بین بانک های خود'), ('deleteOwn.bankTransferTransaction', 'حذف پرداخت های بین بانک های خود'), ('defineOwn.bankTransferTransaction', 'قطعی کردن پرداخت های بین بانک های خود'), ('lockOwn.bankTransferTransaction', 'قفل کردن پرداخت های بین بانک های خود'), ('getOwn.imprestTransaction', 'مشاهده پرداخت تنخواه های خود'), ('updateOwn.imprestTransaction', 'ویرایش پرداخت تنخواه های خود'), ('deleteOwn.imprestTransaction', 'حذف پرداخت تنخواه های خود'), ('defineOwn.imprestTransaction', 'قطعی کردن پرداخت تنخواه های خود'), ('lockOwn.imprestTransaction', 'قفل کردن پرداخت تنخواه های خود'))},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('receive', 'دریافت'), ('payment', 'پرداخت'), ('imprest', 'پرداخت تنخواه'), ('bankTransfer', 'انتقال بین بانکی')], max_length=20),
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.DefaultAccount'),
        ),
    ]