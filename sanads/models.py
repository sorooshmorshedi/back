from django.contrib.admin.options import get_content_type_for_model
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.db import models
from django.db.models.aggregates import Max
from django.db.models.expressions import F
from django.db.models.functions.comparison import Coalesce

from accounts.accounts.models import Account, FloatAccount, AccountBalance
from django_jalali.db import models as jmodels

from companies.models import FinancialYear
from helpers.exceptions.ConfirmationError import ConfirmationError
from helpers.functions import get_current_user, get_object_accounts
from helpers.models import BaseModel, DefinableMixin, LockableMixin
from server.settings import TESTING


class Sanad(BaseModel, DefinableMixin, LockableMixin):
    OPENING = 'o'
    CLOSING = 'c'
    NORMAL = 'n'

    TYPES = (
        (OPENING, 'افتتاحیه'),
        (CLOSING, 'اختتامیه'),
        (NORMAL, 'عادی'),
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='sanads')
    code = models.IntegerField(verbose_name="شماره سند")
    local_id = models.BigIntegerField()
    explanation = models.CharField(max_length=255, blank=True, verbose_name="توضیحات")
    date = jmodels.jDateField(verbose_name="تاریخ")
    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    bed = models.DecimalField(max_digits=24, decimal_places=0, default=0, verbose_name="بدهکار")
    bes = models.DecimalField(max_digits=24, decimal_places=0, default=0, verbose_name="بستانکار")

    is_auto_created = models.BooleanField(default=True)

    type = models.CharField(choices=TYPES, default=NORMAL, max_length=3)

    origin_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True, blank=True)
    origin_id = models.BigIntegerField(null=True, blank=True)

    def get_origin(self):
        if self.origin_id:
            origin = self.origin_content_type.get_object_for_this_type(pk=self.origin_id)
            return origin
        else:
            return None

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        ordering = ['-code', ]
        unique_together = ('code', 'financial_year')
        permission_basename = 'sanad'
        permissions = (
            ('create.sanad', 'تعریف سند'),

            ('get.sanad', 'مشاهده سند'),
            ('update.sanad', 'ویرایش سند'),
            ('define.sanad', 'قطعی کردن سند'),
            ('lock.sanad', 'قفل کردن سند'),

            ('getOwn.sanad', 'مشاهده سند های خود'),
            ('updateOwn.sanad', 'ویرایش سند های خود'),
            ('defineOwn.sanad', 'قطعی کردن سند های خود'),
            ('lockOwn.sanad', 'قفل کردن سند های خود'),

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

    def delete_items(self, origin: BaseModel = None):
        qs = self.items.all()
        if origin:
            qs.filter(
                origin_content_type=get_content_type_for_model(type(origin)),
                origin_id=origin.id
            )

        for item in qs:
            item.delete()

        self.save()
        self.update_values()

    def save(self, *args, **kwargs) -> None:

        self.financial_year.check_date(self.date)

        if not self.local_id:
            self.local_id = Sanad.objects.inFinancialYear(self.financial_year).aggregate(
                local_id=Coalesce(Max('local_id'), 0)
            )['local_id'] + 1

        if self.is_auto_created:
            i = 1
            for item in self.items.all().order_by(F('bes') - F('bed')):
                item.order = i
                item.save()
                i += 1

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for item in self.items.all():
            item.delete()
        return super(Sanad, self).delete(*args, **kwargs)

    def define(self, date=None):
        if not self.is_defined:
            self.is_defined = True
            self.defined_by = get_current_user()
            self.definition_date = date or now()
            self.save()

            for item in self.items.all():
                AccountBalance.update_balance(
                    financial_year=item.financial_year,
                    **get_object_accounts(item),
                    bed_change=item.bed,
                    bes_change=item.bes
                )


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

    order = models.IntegerField(default=0)

    origin_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True, blank=True)
    origin_id = models.BigIntegerField(null=True, blank=True)

    def get_origin(self):
        if self.origin_id:
            origin = self.origin_content_type.get_object_for_this_type(pk=self.origin_id)
            return origin
        else:
            return None

    def __str__(self):
        return "{0} - {1}".format(self.sanad.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        ordering = ('order', 'pk')

    def save(self, *args, **kwargs) -> None:
        self.financial_year = self.sanad.financial_year
        self.is_auto_created = self.sanad.is_auto_created
        super(SanadItem, self).save(*args, **kwargs)


def clearSanad(sanad: Sanad):
    if not sanad:
        return
    sanad.explanation = ''
    sanad.is_auto_created = False
    sanad.type = Sanad.NORMAL
    sanad.date = sanad.financial_year.start
    sanad.origin_content_type = None
    sanad.origin_id = None

    for item in sanad.items.all():
        item.delete()

    sanad.save()
    sanad.update_values()


def newSanadCode(financial_year=None):
    try:
        return Sanad.objects.inFinancialYear(financial_year).latest('code').code + 1
    except:
        financial_year = financial_year or get_current_user().active_financial_year
        company = financial_year.company
        if company.financial_years.count() == 1:
            return 1
        else:
            return 2
