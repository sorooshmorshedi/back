from django.db.models import signals
from django.db import models
from accounts.accounts.models import Account, FloatAccount
from django_jalali.db import models as jmodels

from companies.models import FinancialYear
from helpers.exceptions.ConfirmationError import ConfirmationError
from helpers.models import BaseModel, ConfirmationMixin
from server.settings import TESTING


class Sanad(BaseModel, ConfirmationMixin):
    TEMPORARY = 'temporary'
    DEFINITE = 'definite'
    SANAD_TYPES = (
        (TEMPORARY, 'موقت'),
        (DEFINITE, 'قطعی'),
    )

    AUTO = 'auto'
    MANUAL = 'manual'
    SANAD_CREATE_TYPES = (
        (AUTO, 'خودکار'),
        (MANUAL, 'دستی')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='sanads')
    code = models.IntegerField(verbose_name="شماره سند")
    explanation = models.CharField(max_length=255, blank=True, verbose_name="توضیحات")
    date = jmodels.jDateField(verbose_name="تاریخ")
    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=SANAD_TYPES)
    createType = models.CharField(max_length=20, choices=SANAD_CREATE_TYPES, default=MANUAL, verbose_name="نوع ثبت")

    bed = models.DecimalField(max_digits=24, decimal_places=0, default=0, verbose_name="بدهکار")
    bes = models.DecimalField(max_digits=24, decimal_places=0, default=0, verbose_name="بستانکار")

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        ordering = ['-code', ]
        permission_basename = 'sanad'
        permissions = (
            ('get.sanad', 'مشاهده سند'),
            ('create.sanad', 'تعریف سند'),
            ('update.sanad', 'ویرایش سند'),
            ('delete.sanad', 'حذف سند'),

            ('getOwn.sanad', 'مشاهده سند های خود'),
            ('updateOwn.sanad', 'ویرایش سند های خود'),
            ('deleteOwn.sanad', 'حذف سند های خود'),

            ('firstConfirm.sanad', 'تایید اول سند'),
            ('secondConfirm.sanad', 'تایید دوم سند'),
            ('firstConfirmOwn.sanad', 'تایید اول سند های خود'),
            ('secondConfirmOwn.sanad', 'تایید دوم سند های خود'),

            ('reorder.sanad', 'مرتب کردن کد اسناد بر اساس تاریخ'),
        )

    @property
    def isEmpty(self):
        return self.items.count() == 0

    def check_account_balance_confirmations(self):

        for item in self.items.all():
            account = item.account

            balance = account.bed - account.bes

            if balance > 0:
                if account.max_bed and account.max_bed < balance:
                    if not TESTING:
                        raise ConfirmationError("بدهکاری حساب {} بیشتر از سقف مشخص شده می باشد. سقف: {}".format(
                            account.title,
                            account.max_bed
                        ))
            else:
                balance = -balance
                if account.max_bes and account.max_bes < balance:
                    if not TESTING:
                        raise ConfirmationError("بستانکاری حساب {} بیشتر از سقف مشخص شده می باشد. سقف: {}".format(
                            account.title,
                            account.max_bes
                        ))


class SanadItem(BaseModel):
    BED = 'bed'
    BES = 'bes'
    VALUE_TYPES = (
        (BED, 'bed'),
        (BES, 'bes')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='sanad_items')
    sanad = models.ForeignKey(Sanad, on_delete=models.CASCADE, related_name='items', verbose_name='سند')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='sanadItems', verbose_name='حساب')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='sanadItems', blank=True,
                                     null=True, verbose_name='حساب شناور')
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, blank=True, null=True,
                                   verbose_name='مرکز هزینه', related_name="sanadItemsAsCostCenter")

    bed = models.DecimalField(max_digits=24, decimal_places=0, default=0)
    bes = models.DecimalField(max_digits=24, decimal_places=0, default=0)

    explanation = models.CharField(max_length=255, blank=True, verbose_name='توضیحات')

    def __str__(self):
        return "{0} - {1}".format(self.sanad.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        pass


def updateSanadValues(sender, instance, raw, using, update_fields, **kwargs):
    sanad = instance.sanad

    if instance.id:
        sanadItem = SanadItem.objects.get(pk=instance.id)
        sanad.bed -= sanadItem.bed
        sanad.bes -= sanadItem.bes

    sanad.bed += instance.bed
    sanad.bes += instance.bes

    sanad.save()


def updateSanadValuesOnDelete(sender, instance, using, **kwargs):
    sanad = instance.sanad
    sanad.bed -= instance.bed
    sanad.bes -= instance.bes
    sanad.save()


signals.pre_save.connect(receiver=updateSanadValues, sender=SanadItem)
signals.pre_delete.connect(receiver=updateSanadValuesOnDelete, sender=SanadItem)


def clearSanad(sanad):
    if not sanad:
        return
    sanad.explanation = ''
    sanad.type = 'manual'
    sanad.save()
    for item in sanad.items.all():
        item.delete()


def newSanadCode(financial_year=None):
    try:
        return Sanad.objects.inFinancialYear(financial_year).latest('code').code + 1
    except:
        return 1
