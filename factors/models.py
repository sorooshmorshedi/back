from decimal import Decimal

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Sum
from django_jalali.db import models as jmodels
from rest_framework.exceptions import ValidationError

from accounts.accounts.models import Account, FloatAccount, AccountBalance
from companies.models import FinancialYear
from helpers.models import BaseModel, ConfirmationMixin, EXPLANATION
from helpers.views.MassRelatedCUD import MassRelatedCUD
from sanads.models import Sanad
from transactions.models import Transaction
from wares.models import Ware, Warehouse

EXPENSE_TYPES = (
    ('buy', 'خرید'),
    ('sale', 'فروش')
)


class Expense(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='expenses')
    name = models.CharField(max_length=100, unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factorExpense')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorExpense', null=True,
                                     blank=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorExpenseAsCostCenter',
                                   blank=True, null=True)
    type = models.CharField(max_length=10, choices=EXPENSE_TYPES)
    explanation = models.CharField(max_length=255, blank=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'expense'
        permissions = (
            ('get.expense', 'مشاهده هزینه فاکتور'),
            ('create.expense', 'تعریف هزینه  فاکتور'),
            ('update.expense', 'ویرایش هزینه فاکتور'),
            ('delete.expense', 'حذف هزینه فاکتور'),

            ('getOwn.expense', 'مشاهده هزینه های فاکتور خود'),
            ('updateOwn.expense', 'ویرایش هزینه های فاکتور خود'),
            ('deleteOwn.expense', 'حذف هزینه های فاکتور خود'),
        )


class Factor(BaseModel, ConfirmationMixin):
    BUY = 'buy'
    SALE = 'sale'
    BACK_FROM_BUY = 'backFromBuy'
    BACK_FROM_SALE = 'backFromSale'
    FIRST_PERIOD_INVENTORY = 'fpi'

    INPUT_TRANSFER = 'it'
    OUTPUT_TRANSFER = 'ot'

    INPUT_ADJUSTMENT = 'ia'
    OUTPUT_ADJUSTMENT = 'oa'
    ADJUSTMENT_TYPES = (
        (INPUT_ADJUSTMENT, 'رسید تعدیل انبار'),
        (OUTPUT_ADJUSTMENT, 'حواله تعدیل انبار'),
    )

    FACTOR_TYPES = (
        (BUY, 'خرید'),
        (SALE, 'فروش'),
        (BACK_FROM_BUY, 'بازگشت از خرید'),
        (BACK_FROM_SALE, 'بازگشت از فروش'),
        (FIRST_PERIOD_INVENTORY, 'موجودی اول دوره'),
        (INPUT_TRANSFER, 'وارده از انتقال'),
        (OUTPUT_TRANSFER, 'صادره با انتقال'),
        *ADJUSTMENT_TYPES
    )

    BUY_GROUP = (BUY, BACK_FROM_SALE, FIRST_PERIOD_INVENTORY)
    SALE_GROUP = (SALE, BACK_FROM_BUY)

    INPUT_GROUP = (*BUY_GROUP, INPUT_TRANSFER, INPUT_ADJUSTMENT)
    OUTPUT_GROUP = (*SALE_GROUP, OUTPUT_TRANSFER, OUTPUT_ADJUSTMENT)

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factors')
    code = models.IntegerField(blank=True, null=True)
    sanad = models.OneToOneField(Sanad, on_delete=models.PROTECT, related_name='factor', blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factors', blank=True, null=True)
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factors', blank=True,
                                     null=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorsAsCostCenter',
                                   blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=15, choices=FACTOR_TYPES)
    paidValue = models.DecimalField(default=0, max_digits=24, decimal_places=0)
    bijak = models.IntegerField(null=True, blank=True)

    date = jmodels.jDateField()
    time = models.TimeField()

    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    discountValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    discountPercent = models.IntegerField(default=0, null=True, blank=True)

    has_tax = models.BooleanField(default=False)
    taxValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    taxPercent = models.IntegerField(default=0, null=True, blank=True)

    is_definite = models.BooleanField(default=0)
    definition_date = models.DateTimeField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        permissions = (
            ('get.buyFactor', 'مشاهده فاکتور خرید'),
            ('create.buyFactor', 'تعریف فاکتور خرید'),
            ('update.buyFactor', 'ویرایش فاکتور خرید'),
            ('delete.buyFactor', 'حذف فاکتور خرید'),
            ('definite.buyFactor', 'قطعی کردن خرید'),

            ('get.saleFactor', 'مشاهده فاکتور فروش'),
            ('create.saleFactor', 'تعریف فاکتور فروش'),
            ('update.saleFactor', 'ویرایش فاکتور فروش'),
            ('delete.saleFactor', 'حذف فاکتور فروش'),
            ('definite.saleFactor', 'قطعی کردن فروش'),

            ('get.backFromSaleFactor', 'مشاهده فاکتور برگشت از فروش'),
            ('create.backFromSaleFactor', 'تعریف فاکتور برگشت از فروش'),
            ('update.backFromSaleFactor', 'ویرایش فاکتور برگشت از فروش'),
            ('delete.backFromSaleFactor', 'حذف فاکتور برگشت از فروش'),
            ('definite.backFromSaleFactor', 'قطعی کردن برگشت از فروش'),

            ('get.backFromBuyFactor', 'مشاهده فاکتور برگشت از خرید'),
            ('create.backFromBuyFactor', 'تعریف فاکتور برگشت از خرید'),
            ('update.backFromBuyFactor', 'ویرایش فاکتور برگشت از خرید'),
            ('delete.backFromBuyFactor', 'حذف فاکتور برگشت از خرید'),
            ('definite.backFromBuyFactor', 'قطعی کردن برگشت از خرید'),

            ('get.notPaidFactor', 'مشاهده فاکتور های پرداخت نشده'),
            ('get.notReceivedFactor', 'مشاهده فاکتور های دریافت نشده'),

            ('getOwn.buyFactor', 'مشاهده فاکتور خرید خود'),
            ('updateOwn.buyFactor', 'ویرایش فاکتور های خرید خود'),
            ('deleteOwn.buyFactor', 'حذف فاکتور های خرید خود'),
            ('definiteOwn.buyFactor', 'قطعی کردن فاکتور های خرید خود'),

            ('getOwn.saleFactor', 'مشاهده فاکتور های فروش خود'),
            ('updateOwn.saleFactor', 'ویرایش فاکتور های فروش خود'),
            ('deleteOwn.saleFactor', 'حذف فاکتور های فروش خود'),
            ('definiteOwn.saleFactor', 'قطعی کردن فاکتور های فروش خود'),

            ('getOwn.backFromSaleFactor', 'مشاهده فاکتور های برگشت از فروش خود'),
            ('updateOwn.backFromSaleFactor', 'ویرایش فاکتور های برگشت از فروش خود'),
            ('deleteOwn.backFromSaleFactor', 'حذف فاکتور های برگشت از فروش خود'),
            ('definiteOwn.backFromSaleFactor', 'قطعی کردن فاکتور های برگشت از فروش خود'),

            ('getOwn.backFromBuyFactor', 'مشاهده فاکتور های برگشت از خرید خود'),
            ('updateOwn.backFromBuyFactor', 'ویرایش فاکتور های برگشت از خرید خود'),
            ('deleteOwn.backFromBuyFactor', 'حذف فاکتور های برگشت از خرید خود'),
            ('definiteOwn.backFromBuyFactor', 'قطعی کردن فاکتور های برگشت از خرید خود'),

            ('getOwn.notPaidFactor', 'مشاهده فاکتور های پرداخت نشده خود'),
            ('getOwn.notReceivedFactor', 'مشاهده فاکتور های دریافت نشده خود'),

            ('get.firstPeriodInventory', 'مشاهده موجودی اول دوره'),
            ('update.firstPeriodInventory', 'ثبت موجودی اول دوره'),

            ('firstConfirm.buyFactor', 'تایید اول فاکتور خرید '),
            ('secondConfirm.buyFactor', 'تایید دوم فاکتور خرید '),
            ('firstConfirmOwn.buyFactor', 'تایید اول فاکتور های خرید خود'),
            ('secondConfirmOwn.buyFactor', 'تایید دوم فاکتور های خرید خود'),

            ('firstConfirm.saleFactor', 'تایید اول فاکتور فروش '),
            ('secondConfirm.saleFactor', 'تایید دوم فاکتور فروش '),
            ('firstConfirmOwn.saleFactor', 'تایید اول فاکتور های فروش خود'),
            ('secondConfirmOwn.saleFactor', 'تایید دوم فاکتور های فروش خود'),

            ('firstConfirm.backFromBuyFactor', 'تایید اول فاکتور برگشت از خرید'),
            ('secondConfirm.backFromBuyFactor', 'تایید دوم فاکتور برگشت از خرید'),
            ('firstConfirmOwn.backFromBuyFactor', 'تایید اول فاکتور های برگشت از خرید خود'),
            ('secondConfirmOwn.backFromBuyFactor', 'تایید دوم فاکتور های برگشت از خرید خود'),

            ('firstConfirm.backFromSaleFromSaleFactor', 'تایید اول فاکتور برگشت از فروش '),
            ('secondConfirm.backFromSaleFromSaleFactor', 'تایید دوم فاکتور برگشت از فروش '),
            ('firstConfirmOwn.backFromSaleFromSaleFactor', 'تایید اول فاکتور های برگشت از فروش خود'),
            ('secondConfirmOwn.backFromSaleFromSaleFactor', 'تایید دوم فاکتور های برگشت از فروش خود'),

        )

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
        return "فاکتور های {}".format(self.get_type_label)

    @property
    def type_label(self):
        return [t[1] for t in Factor.FACTOR_TYPES if t[0] == self.type][0]

    @property
    def remain(self):
        bed, bes = AccountBalance.get_bed_bes(self.account, self.floatAccount, self.costCenter)
        remain_value = abs(bed - bes)
        remain_type = "bed" if bed > bes else "bes"
        if self.type in ('buy', 'backFromSale'):
            after_factor_title = 'مبلغ قابل پرداخت'
            if remain_type == 'bes':
                before_factor = self.totalSum + remain_value
                sign = '+'
                before_factor_title = 'مانده بستانکار'
            else:
                before_factor = self.totalSum - remain_value
                sign = '-'
                before_factor_title = 'مانده بدهکار'
        else:
            after_factor_title = 'مبلغ قابل دریافت'
            if remain_type == 'bes':
                before_factor = self.totalSum - remain_value
                sign = '-'
                before_factor_title = 'مانده بستانکار'
            else:
                before_factor = self.totalSum + remain_value
                sign = '+'
                before_factor_title = 'مانده بدهکار'

        res = {
            'before_factor_title': before_factor_title,
            'before_factor': abs(before_factor),
            'after_factor_title': after_factor_title,
            'after_factor': remain_value,
            'sign': sign
        }
        return res

    def sync(self, user, data):
        from factors.serializers import FactorItemSerializer
        from factors.serializers import FactorExpenseSerializer

        factor_items_data = data.get('items')
        factor_expenses_data = data.get('expenses')

        MassRelatedCUD(
            user,
            factor_items_data.get('items'),
            factor_items_data.get('ids_to_delete'),
            'factor',
            self.id,
            FactorItemSerializer,
            FactorItemSerializer
        ).sync()

        MassRelatedCUD(
            user,
            factor_expenses_data.get('items'),
            factor_expenses_data.get('ids_to_delete'),
            'factor',
            self.id,
            FactorExpenseSerializer,
            FactorExpenseSerializer

        ).sync()

    def check_inventory(self):
        for item in self.items.all():
            ware = item.ware
            warehouse = item.warehouse

            count = ware.get_inventory_count(warehouse)

            if count < 0:
                raise ValidationError("موجودی انبار برای کالای {} کافی نیست.".format(ware))

    @staticmethod
    def get_first_period_inventory(financial_year=None):
        try:
            return Factor.objects.inFinancialYear(financial_year).get(code=0)
        except Factor.DoesNotExist:
            return None

    @staticmethod
    def newCodes(factor_type=None):
        codes = {}
        for type in Factor.FACTOR_TYPES:
            type = type[0]
            if factor_type:
                if type != factor_type:
                    continue

            codes[type] = {}
            try:
                last_factor = Factor.objects.inFinancialYear() \
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
    def is_last_definite_factor(self):
        count = Factor.objects \
            .filter(financial_year=self.financial_year,
                    is_definite=self.is_definite,
                    definition_date__gt=self.definition_date
                    ) \
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
        else:
            return True

    @property
    def is_editable(self):
        if self.is_definite:
            return self.is_last_definite_factor
        else:
            return True


class FactorExpense(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factor_expenses')
    expense = models.ForeignKey(Expense, on_delete=models.PROTECT, related_name='factorExpenses')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='expenses')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factorExpenses')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorExpenses', blank=True,
                                     null=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorExpensesAsCostCenter',
                                   blank=True, null=True)
    value = models.DecimalField(max_digits=24, decimal_places=0)
    explanation = models.CharField(max_length=255, blank=True)

    class Meta(BaseModel.Meta):
        permission_basename = 'factorExpenses'
        permissions = (
            ('get.factorExpenses', 'مشاهده هزینه های فاکتور'),
            ('create.factorExpenses', 'تعریف هزینه های فاکتور'),
            ('update.factorExpenses', 'ویرایش هزینه های فاکتور'),
            ('delete.factorExpenses', 'حذف هزینه های فاکتور'),

            ('getOwn.factorExpenses', 'مشاهده هزینه های فاکتور خود'),
            ('updateOwn.factorExpenses', 'ویرایش هزینه های فاکتور خود'),
            ('deleteOwn.factorExpenses', 'حذف هزینه های فاکتور خود'),
        )


class FactorPayment(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factor_payments')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='payments')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='payments')
    value = models.DecimalField(max_digits=24, decimal_places=0)

    class Meta(BaseModel.Meta):
        unique_together = ('factor', 'transaction')


def get_empty_array():
    return []


class FactorItem(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factor_items')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='items')
    ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='factorItems')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='factorItems', null=True,
                                  blank=True)

    count = models.DecimalField(max_digits=24, decimal_places=6)
    fee = models.DecimalField(max_digits=24, decimal_places=0)

    # Used for undo definition for output factors to increase inventory
    fees = JSONField(default=get_empty_array)

    remain_fees = JSONField(default=get_empty_array)
    discountValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    discountPercent = models.IntegerField(default=0, null=True, blank=True)
    explanation = models.CharField(max_length=255, blank=True)

    # this is used for inventory reports and sanads.
    # it's equals to fees count * fees fee
    calculated_value = models.DecimalField(default=0, max_digits=24, decimal_places=0, blank=True)

    def __str__(self):
        return "factor id: {}, factor type: {}, is_definite: {}, ware: {}, count: {}".format(
            self.factor.id,
            self.factor.type,
            self.factor.is_definite,
            self.ware, self.count
        )

    class Meta(BaseModel.Meta):
        pass

    @property
    def remain_count(self):
        count = 0
        for fee in self.remain_fees:
            count += fee['count']
        return count

    @property
    def remain_value(self):
        value = 0
        for fee in self.remain_fees:
            value += fee['count'] * fee['fee']
        return value

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.factor.is_editable:
            raise ValidationError('فاکتور غیر قابل ویرایش می باشد')

        self.discountValue = self.discount
        self.calculated_value = 0
        for fee in self.fees:
            self.calculated_value += fee['count'] * fee['fee']
        return super(FactorItem, self).save(force_insert, force_update, using, update_fields)

    def delete(self, *args, **kwargs):
        if not self.factor.is_editable:
            raise ValidationError('فاکتور غیر قابل ویرایش می باشد')
        return super().delete(**args, **kwargs)


class Transfer(BaseModel):
    code = models.IntegerField()
    date = jmodels.jDateField()

    input_factor = models.ForeignKey(Factor, on_delete=models.PROTECT, related_name='input_transfer')
    output_factor = models.ForeignKey(Factor, on_delete=models.PROTECT, related_name='output_transfer')
    explanation = models.CharField(max_length=255, blank=True)

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='transfers')

    class Meta(BaseModel.Meta):
        permission_basename = 'transfer'
        permissions = (
            ('get.transfer', 'مشاهده انتقال'),
            ('create.transfer', 'تعریف انتقال'),
            ('update.transfer', 'ویرایش انتقال'),
            ('delete.transfer', 'حذف انتقال'),

            ('getOwn.transfer', 'مشاهده انتقال های خود'),
            ('updateOwn.transfer', 'ویرایش انتقال های خود'),
            ('deleteOwn.transfer', 'حذف انتقال های خود'),
        )


class Adjustment(BaseModel):
    code = models.IntegerField()
    date = jmodels.jDateField()

    type = models.CharField(max_length=2, choices=Factor.ADJUSTMENT_TYPES)
    factor = models.ForeignKey(Factor, on_delete=models.PROTECT, related_name='adjustment')
    sanad = models.ForeignKey(Sanad, on_delete=models.PROTECT, related_name='adjustment', null=True)
    explanation = EXPLANATION()

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    class Meta(BaseModel.Meta):
        permission_basename = 'adjustment'
        permissions = (
            ('get.adjustment', 'مشاهده تعدیل '),
            ('create.adjustment', 'تعریف تعدیل '),
            ('update.adjustment', 'ویرایش تعدیل '),
            ('delete.adjustment', 'حذف تعدیل '),

            ('getOwn.adjustment', 'مشاهده تعدیل های خود'),
            ('updateOwn.adjustment', 'ویرایش تعدیل های خود'),
            ('deleteOwn.adjustment', 'حذف تعدیل های خود'),
        )
