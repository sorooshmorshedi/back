# Generated by Django 2.2 on 2020-07-29 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('_dashtbashi', '0011_lading_is_paid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lading',
            options={'default_permissions': (), 'ordering': ['pk'], 'permissions': (('get.lading', 'مشاهده بارگیری'), ('create.lading', 'تعریف بارگیری'), ('update.lading', 'ویرایش بارگیری'), ('delete.lading', 'حذف بارگیری'), ('getOwn.lading', 'مشاهده بارگیری های خود'), ('updateOwn.lading', 'ویرایش بارگیری های خود'), ('deleteOwn.lading', 'حذف بارگیری های خود'), ('firstConfirm.lading', 'تایید اول بارگیری '), ('secondConfirm.lading', 'تایید دوم بارگیری '), ('firstConfirmOwn.lading', 'تایید اول بارگیری های خود'), ('secondConfirmOwn.lading', 'تایید دوم بارگیری های خود'))},
        ),
        migrations.AlterModelOptions(
            name='oilcompanylading',
            options={'default_permissions': (), 'ordering': ['pk'], 'permissions': (('get.oilCompanyLading', 'مشاهده بارگیری شرکت نفت'), ('create.oilCompanyLading', 'تعریف بارگیری شرکت نفت'), ('update.oilCompanyLading', 'ویرایش بارگیری شرکت نفت'), ('delete.oilCompanyLading', 'حذف بارگیری شرکت نفت'), ('getOwn.oilCompanyLading', 'مشاهده بارگیری شرکت نفت خود'), ('updateOwn.oilCompanyLading', 'ویرایش بارگیری شرکت نفت خود'), ('deleteOwn.oilCompanyLading', 'حذف بارگیری شرکت نفت خود'), ('firstConfirm.oilCompanyLading', 'تایید اول بارگیری شرکت نفت '), ('secondConfirm.oilCompanyLading', 'تایید دوم بارگیری شرکت نفت '), ('firstConfirmOwn.oilCompanyLading', 'تایید اول بارگیری شرکت نفت خود'), ('secondConfirmOwn.oilCompanyLading', 'تایید دوم بارگیری شرکت نفت خود'))},
        ),
        migrations.AlterModelOptions(
            name='otherdriverpayment',
            options={'default_permissions': (), 'ordering': ['pk'], 'permissions': (('get.otherDriverPayment', 'مشاهده پرداخت رانندگان متفرقه '), ('create.otherDriverPayment', 'تعریف پرداخت رانندگان متفرقه'), ('update.otherDriverPayment', 'ویرایش پرداخت رانندگان متفرقه'), ('delete.otherDriverPayment', 'حذف پرداخت رانندگان متفرقه'), ('getOwn.otherDriverPayment', 'مشاهده پرداخت رانندگان متفرقه خود'), ('updateOwn.otherDriverPayment', 'ویرایش پرداخت رانندگان متفرقه خود'), ('deleteOwn.otherDriverPayment', 'حذف پرداخت رانندگان متفرقه خود'), ('firstConfirm.otherDriverPayment', 'تایید اول پرداخت رانندگان متفرقه '), ('secondConfirm.otherDriverPayment', 'تایید دوم پرداخت رانندگان متفرقه '), ('firstConfirmOwn.otherDriverPayment', 'تایید اول پرداخت رانندگان متفرقه خود'), ('secondConfirmOwn.otherDriverPayment', 'تایید دوم پرداخت رانندگان متفرقه خود'))},
        ),
        migrations.AlterModelOptions(
            name='remittance',
            options={'default_permissions': (), 'ordering': ['-code'], 'permissions': (('get.remittance', 'مشاهده حواله'), ('create.remittance', 'تعریف حواله'), ('update.remittance', 'ویرایش حواله'), ('delete.remittance', 'حذف حواله'), ('getOwn.remittance', 'مشاهده حواله های خود'), ('updateOwn.remittance', 'ویرایش حواله های خود'), ('deleteOwn.remittance', 'حذف حواله های خود'), ('firstConfirm.remittance', 'تایید اول حواله '), ('secondConfirm.remittance', 'تایید دوم حواله '), ('firstConfirmOwn.remittance', 'تایید اول حواله های خود'), ('secondConfirmOwn.remittance', 'تایید دوم حواله های خود'))},
        ),
        migrations.AddField(
            model_name='remittance',
            name='first_confirmed_at',
            field=django_jalali.db.models.jDateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='remittance',
            name='first_confirmed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='first_remittanceConfirmer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='remittance',
            name='second_confirmed_at',
            field=django_jalali.db.models.jDateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='remittance',
            name='second_confirmed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='second_remittanceConfirmer', to=settings.AUTH_USER_MODEL),
        ),
    ]
