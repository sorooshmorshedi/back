from decimal import Decimal
from django.db import models
from django.db.models import signals, Sum, Max
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account, FloatAccount
from companies.models import FinancialYear
from factors.signals import clearFactorSanad
from helpers.models import BaseModel
from sanads.sanads.models import Sanad
from sanads.transactions.models import Transaction
from wares.models import Ware, Warehouse

EXPENSE_TYPES = (
    ('buy', 'خرید'),
    ('sale', 'فروش')
)


class Expense(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='expenses')
    name = models.CharField(max_length=100, unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factorExpense')
    type = models.CharField(max_length=10, choices=EXPENSE_TYPES)
    explanation = models.CharField(max_length=255, blank=True)


class Factor(BaseModel):

    BUY = 'buy'
    SALE = 'sale'
    BACK_FROM_BUY = 'backFromBuy'
    BACK_FROM_SALE = 'backFromSale'
    FIRST_PERIOD_INVENTORY = 'fpi'
    INPUT_TRANSFER = 'it'
    OUTPUT_TRANSFER = 'ot'

    FACTOR_TYPES = (
        (BUY, 'خرید'),
        (SALE, 'فروش'),
        (BACK_FROM_BUY, 'بازگشت از خرید'),
        (BACK_FROM_SALE, 'بازگشت از فروش'),
        (FIRST_PERIOD_INVENTORY, 'موجودی اول دوره'),
        (INPUT_TRANSFER, 'وارده از انتقال'),
        (OUTPUT_TRANSFER, 'صادره با انتقال'),
    )

    BUY_GROUP = (BUY, BACK_FROM_SALE, FIRST_PERIOD_INVENTORY)
    SALE_GROUP = (SALE, BACK_FROM_BUY)

    INPUT_GROUP = (*BUY_GROUP, INPUT_TRANSFER)
    OUTPUT_GROUP = (*SALE_GROUP, OUTPUT_TRANSFER)

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factors')
    code = models.IntegerField(blank=True, null=True)
    sanad = models.OneToOneField(Sanad, on_delete=models.PROTECT, related_name='factor', blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factors', blank=True, null=True)
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factors', blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=15, choices=FACTOR_TYPES)
    paidValue = models.DecimalField(default=0, max_digits=24, decimal_places=0)
    bijak = models.IntegerField(null=True, blank=True)

    date = jmodels.jDateField()
    time = models.TimeField(auto_now=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    discountValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    discountPercent = models.IntegerField(default=0, null=True, blank=True)
    taxValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    taxPercent = models.IntegerField(default=0, null=True, blank=True)

    is_definite = models.BooleanField(default=0)
    definition_date = models.DateTimeField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        unique_together = ('code', 'type')

    def __str__(self):
        return "ID: {}, code: {}, type: {}, is_definite: {}".format(self.pk, self.code, self.type, self.is_definite)

    @property
    def sum(self):
        sum = 0
        for i in self.items.all():
            sum += i.fee * i.count
        return Decimal(sum)

    @property
    def discountSum(self):
        if self.discountPercent:
            discountSum = self.discountPercent * self.sum / 100
        else:
            discountSum = self.discountValue
        for i in self.items.all():
            discountSum += i.discount
        return Decimal(discountSum)

    @property
    def taxSum(self):
        if self.taxPercent:
            taxSum = self.taxPercent * (self.sum - self.discountSum) / 100
        else:
            taxSum = self.taxValue
        return Decimal(taxSum)

    @property
    def sumAfterDiscount(self):
        return Decimal(self.sum - self.discountSum)

    @property
    def totalSum(self):
        return Decimal(self.sum - self.discountSum + self.taxSum)

    @property
    def expensesSum(self):
        return Decimal(FactorExpense.objects.filter(factor=self).aggregate(Sum('value'))['value__sum'])

    @property
    def label(self):
        return "فاکتور {}".format(self.get_type_label)

    @property
    def type_label(self):
        return [t[1] for t in Factor.FACTOR_TYPES if t[0] == self.type][0]

    @property
    def remain(self):
        account_remain = self.account.get_remain()
        if self.type in ('buy', 'backFromSale'):
            after_factor_title = 'مبلغ قابل پرداخت'
            if account_remain['remain_type'] == 'bes':
                before_factor = self.totalSum + account_remain['value']
                sign = '+'
                before_factor_title = 'مانده بستانکار'
            else:
                before_factor = self.totalSum - account_remain['value']
                sign = '-'
                before_factor_title = 'مانده بدهکار'
        else:
            after_factor_title = 'مبلغ قابل دریافت'
            if account_remain['remain_type'] == 'bes':
                before_factor = self.totalSum - account_remain['value']
                sign = '-'
                before_factor_title = 'مانده بستانکار'
            else:
                before_factor = self.totalSum + account_remain['value']
                sign = '+'
                before_factor_title = 'مانده بدهکار'

        res = {
            'before_factor_title': before_factor_title,
            'before_factor': abs(before_factor),
            'after_factor_title': after_factor_title,
            'after_factor': account_remain['value'],
            'sign': sign
        }
        return res

    @staticmethod
    def getFirstPeriodInventory(user):
        try:
            return Factor.objects.inFinancialYear(user).get(code=0)
        except Factor.DoesNotExist:
            return None

    @staticmethod
    def newCodes(user, factor_type=None):
        codes = {}
        for type in Factor.FACTOR_TYPES:
            type = type[0]
            if factor_type:
                if type != factor_type:
                    continue

            codes[type] = {}
            try:
                last_factor = Factor.objects.inFinancialYear(user) \
                    .filter(type=type, is_definite=1).latest('code')
                codes[type]['code'] = last_factor.code + 1
                codes[type]['last_id'] = last_factor.pk
            except:
                codes[type]['code'] = 1
                codes[type]['last_id'] = 0

        if factor_type:
            return codes[factor_type]['code']
        else:
            return codes

    @property
    def has_uneditable_item(self):
        for item in self.items.all():
            if not item.get_is_editable():
                return True
        return False

    @property
    def has_editable_item(self):
        for item in self.items.all():
            if item.get_is_editable():
                return True
        return False

    @property
    def is_last_definite_factor(self):
        count = Factor.objects\
            .filter(financial_year=self.financial_year,
                    is_definite=self.is_definite,
                    definition_date__gt=self.definition_date
                    )\
            .count()
        if count == 0:
            return True
        else:
            return False

    @property
    def is_output_after_this(self):
        count = Factor.objects \
            .filter(financial_year=self.financial_year,
                    type__in=Factor.OUTPUT_GROUP,
                    created_at__gte=self.definition_date
                    ) \
            .count()
        return count

    @property
    def is_deletable(self):
        if self.is_definite:
            return self.is_last_definite_factor
            # if self.type in Factor.BUY_GROUP:
            #     return self.is_last_definite_factor and not self.is_output_after_this
            # else:
            #     return self.is_last_definite_factor
        else:
            return True

    @property
    def is_editable(self):
        if self.is_definite:
            return self.is_last_definite_factor
            # if self.type in Factor.BUY_GROUP:
            #     res = not self.is_output_after_this
            # else:
            #     res = self.is_last_definite_factor
        else:
            return True


class FactorExpense(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factor_expenses')
    expense = models.ForeignKey(Expense, on_delete=models.PROTECT, related_name='factorExpenses')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='expenses')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factorExpenses')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorExpenses', blank=True, null=True)
    value = models.DecimalField(max_digits=24, decimal_places=0)
    explanation = models.CharField(max_length=255, blank=True)


class FactorPayment(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factor_payments')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='payments')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='payments')
    value = models.DecimalField(max_digits=24, decimal_places=0)

    class Meta(BaseModel.Meta):
        unique_together = ('factor', 'transaction')


class FactorItem(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factor_items')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='items')
    ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='factorItems')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='factorItems')

    count = models.IntegerField()
    fee = models.DecimalField(max_digits=24, decimal_places=0)
    discountValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    discountPercent = models.IntegerField(default=0, null=True, blank=True)
    explanation = models.CharField(max_length=255, blank=True)

    calculated_output_value = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    remain_count = models.IntegerField(null=True, blank=True, default=0)
    remain_value = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)

    is_editable = models.BooleanField(default=1)

    @property
    def value(self):
        return self.fee * self.count

    @property
    def discount(self):
        if self.discountPercent:
            return self.value * self.discountPercent / 100
        else:
            return self.discountValue

    @property
    def totalValue(self):
        return self.value - self.discount

    def get_is_editable(self):
        ware = self.ware
        if ware.pricingType == Ware.FIFO:
            return self.is_editable
        else:
            qs = FactorItem.objects.filter(
                financial_year=self.financial_year,
                ware=ware,
                factor__type__in=Factor.SALE_GROUP,
                factor__is_definite=True,
                factor__definition_date__gt=str(self.factor.created_at)
            ).count()
            if qs:
                return False
            return True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.discountValue = self.discount
        return super(FactorItem, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class Transfer(BaseModel):
    code = models.IntegerField()
    date = jmodels.jDateField()
    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    input_factor = models.ForeignKey(Factor, on_delete=models.PROTECT, related_name='input_transfer')
    output_factor = models.ForeignKey(Factor, on_delete=models.PROTECT, related_name='output_transfer')
    explanation = models.CharField(max_length=255, blank=True)

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='transfers')


signals.post_delete.connect(receiver=clearFactorSanad, sender=Factor)

