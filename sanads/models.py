from django.db import models
from accounts.accounts.models import Account, FloatAccount
from django_jalali.db import models as jmodels

from companies.models import FinancialYear
from helpers.exceptions.ConfirmationError import ConfirmationError
from helpers.models import BaseModel, ConfirmationMixin
from server.settings import TESTING


class Sanad(BaseModel, ConfirmationMixin):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='sanads')
    code = models.IntegerField(verbose_name="شماره سند")
    explanation = models.CharField(max_length=255, blank=True, verbose_name="توضیحات")
    date = jmodels.jDateField(verbose_name="تاریخ")
    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    bed = models.DecimalField(max_digits=24, decimal_places=0, default=0, verbose_name="بدهکار")
    bes = models.DecimalField(max_digits=24, decimal_places=0, default=0, verbose_name="بستانکار")

    is_auto_created = models.BooleanField(default=True)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        ordering = ['-code', ]
        permission_basename = 'sanad'
        permissions = (
            ('get.sanad', 'مشاهده سند'),
            ('create.sanad', 'تعریف سند'),
            ('update.sanad', 'ویرایش سند'),

            ('getOwn.sanad', 'مشاهده سند های خود'),
            ('updateOwn.sanad', 'ویرایش سند های خود'),

            ('firstConfirm.sanad', 'تایید اول سند'),
            ('secondConfirm.sanad', 'تایید دوم سند'),
            ('firstConfirmOwn.sanad', 'تایید اول سند های خود'),
            ('secondConfirmOwn.sanad', 'تایید دوم سند های خود'),

            ('reorder.sanad', 'مرتب کردن کد اسناد بر اساس تاریخ'),
        )

    @property
    def isEmpty(self):
        return self.items.count() == 0

    def update_values(self):
        bed = bes = 0
        for item in self.items.all():
            bed += item.bed
            bes += item.bes
        self.bed = bed
        self.bes = bes
        self.save()

    def check_account_balance_confirmations(self):

        for item in self.items.all():
            account = item.account

            balance = account.get_balance()
            bed = balance['bed']
            bes = balance['bes']

            balance = bed - bes

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

    def delete(self, *args, **kwargs):
        for item in self.items.all():
            item.delete()
        return super(Sanad, self).delete(*args, **kwargs)


class SanadItem(BaseModel):
    BED = 'bed'
    BES = 'bes'
    VALUE_TYPES = (
        (BED, 'bed'),
        (BES, 'bes')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='sanad_items')
    sanad = models.ForeignKey(Sanad, on_delete=models.PROTECT, related_name='items', verbose_name='سند')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='sanadItems', verbose_name='حساب')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='sanadItems', blank=True,
                                     null=True, verbose_name='حساب شناور')
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, blank=True, null=True,
                                   verbose_name='مرکز هزینه و درآمد', related_name="sanadItemsAsCostCenter")

    bed = models.DecimalField(max_digits=24, decimal_places=0, default=0)
    bes = models.DecimalField(max_digits=24, decimal_places=0, default=0)

    explanation = models.CharField(max_length=255, blank=True, verbose_name='توضیحات')

    def __str__(self):
        return "{0} - {1}".format(self.sanad.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        pass

    def save(self, *args, **kwargs) -> None:
        self.financial_year = self.sanad.financial_year
        super(SanadItem, self).save(*args, **kwargs)


def clearSanad(sanad: Sanad):
    if not sanad:
        return
    sanad.explanation = ''
    sanad.is_auto_created = False
    sanad.save()
    for item in sanad.items.all():
        item.delete()

    sanad.update_values()


def newSanadCode(financial_year=None):
    try:
        return Sanad.objects.inFinancialYear(financial_year).latest('code').code + 1
    except:
        return 1
