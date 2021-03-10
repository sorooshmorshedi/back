from _pydecimal import Decimal

from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.db.models.aggregates import Sum, Max
from django.db.models.functions.comparison import Coalesce
from django.db.models.query_utils import Q
from django_jalali.db import models as jmodels
from rest_framework.exceptions import ValidationError

from accounts.accounts.models import Account, FloatAccount, AccountBalance
from companies.models import FinancialYear
from distributions.models import Visitor
from distributions.models.car_model import Car
from distributions.models.distribution_model import Distribution
from distributions.models.path_model import Path
from factors.models.expense import Expense
from helpers.db import get_empty_array
from helpers.models import BaseModel, ConfirmationMixin, DECIMAL
from helpers.views.MassRelatedCUD import MassRelatedCUD
from sanads.models import Sanad
from transactions.models import Transaction
from wares.models import Ware, Unit, Warehouse


class Factor(BaseModel, ConfirmationMixin):
    BUY = 'buy'
    SALE = 'sale'
    BACK_FROM_BUY = 'backFromBuy'
    BACK_FROM_SALE = 'backFromSale'
    FIRST_PERIOD_INVENTORY = 'fpi'

    CONSUMPTION_WARE = 'cw'

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
        (CONSUMPTION_WARE, 'حواله کالای مصرفی'),
        *ADJUSTMENT_TYPES
    )

    BUY_GROUP = (BUY, BACK_FROM_SALE, FIRST_PERIOD_INVENTORY)
    SALE_GROUP = (SALE, BACK_FROM_BUY)

    INPUT_GROUP = (*BUY_GROUP, INPUT_TRANSFER, INPUT_ADJUSTMENT)
    OUTPUT_GROUP = (*SALE_GROUP, OUTPUT_TRANSFER, OUTPUT_ADJUSTMENT, CONSUMPTION_WARE)

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factors')
    temporary_code = models.IntegerField()
    code = models.IntegerField(blank=True, null=True)
    sanad = models.OneToOneField(Sanad, on_delete=models.PROTECT, related_name='factor', blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factors', blank=True, null=True)
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factors', blank=True,
                                     null=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorsAsCostCenter',
                                   blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=15, choices=FACTOR_TYPES)
    bijak = models.IntegerField(null=True, blank=True)

    date = jmodels.jDateField()
    time = models.TimeField()

    discountValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    discountPercent = models.IntegerField(default=0, null=True, blank=True)

    has_tax = models.BooleanField(default=False)
    taxValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    taxPercent = models.IntegerField(default=0, null=True, blank=True)

    is_definite = models.BooleanField(default=False)
    defined_by = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, related_name='definedFactors')
    definition_date = models.DateTimeField(blank=True, null=True)

    is_loaded = models.BooleanField(default=False)
    loaded_by = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, related_name='loadedFactors')
    distribution = models.ForeignKey(Distribution, on_delete=models.PROTECT, null=True, related_name='factors')
    loading_date = models.DateTimeField(blank=True, null=True)

    is_delivered = models.BooleanField(default=False)
    delivered_by = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, related_name='deliveredFactors')
    delivery_date = models.DateTimeField(blank=True, null=True)

    is_settled = models.BooleanField(default=False)

    paidValue = DECIMAL()
    total_sum = DECIMAL()

    visitor = models.ForeignKey(Visitor, on_delete=models.PROTECT, related_name='factors', blank=True, null=True)

    path = models.ForeignKey(Path, on_delete=models.PROTECT, related_name='factors', blank=True, null=True)

    backFrom = models.OneToOneField('self', on_delete=models.PROTECT, related_name='backFactor', blank=True, null=True)

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

            ('get.consumptionWareFactor', 'مشاهده حواله کالای مصرفی'),
            ('create.consumptionWareFactor', 'تعریف حواله کالای مصرفی'),
            ('update.consumptionWareFactor', 'ویرایش حواله کالای مصرفی'),
            ('delete.consumptionWareFactor', 'حذف حواله کالای مصرفی'),
            ('definite.consumptionWareFactor', 'قطعی کردن حواله کالای مصرفی'),

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

            ('getOwn.consumptionWareFactor', 'مشاهده حواله کالای مصرفی خود'),
            ('updateOwn.consumptionWareFactor', 'ویرایش حواله کالای مصرفی خود'),
            ('deleteOwn.consumptionWareFactor', 'حذف حواله کالای مصرفی خود'),
            ('definiteOwn.consumptionWareFactor', 'قطعی کردن حواله کالای مصرفی خود'),

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

            ('firstConfirm.consumptionWareFactor', 'تایید اولحواله کالای مصرفی'),
            ('secondConfirm.consumptionWareFactor', 'تایید دومحواله کالای مصرفی'),
            ('firstConfirmOwn.consumptionWareFactor', 'تایید اول حواله کالای مصرفی خود'),
            ('secondConfirmOwn.consumptionWareFactor', 'تایید دوم حواله کالای مصرفی خود'),

        )

    def __str__(self):
        return "ID: {}, code: {}, type: {}, is_definite: {}".format(self.pk, self.code, self.type, self.is_definite)

    @property
    def sum(self):
        sum = 0
        for i in self.items.all():
            sum += i.fee * i.count
        return sum

    @property
    def calculated_sum(self):
        sum = 0
        for item in self.items.all():
            sum += item.calculated_value
        return sum

    @property
    def discountSum(self):
        if self.discountPercent:
            discountSum = self.discountPercent * self.sum / 100
        else:
            discountSum = self.discountValue
        for i in self.items.all():
            discountSum += i.discount
        return discountSum

    @property
    def taxSum(self):
        if self.taxPercent:
            taxSum = self.taxPercent * (self.sum - self.discountSum) / 100
        else:
            taxSum = self.taxValue
        return taxSum

    @property
    def sumAfterDiscount(self):
        return Decimal(self.sum - self.discountSum)

    @property
    def expensesSum(self):
        return Decimal(FactorExpense.objects.filter(factor=self).aggregate(Sum('value'))['value__sum'])

    @property
    def label(self):
        return "فاکتور های {}".format(self.type_label)

    @staticmethod
    def get_type_label(factor_type):
        return [t[1] for t in Factor.FACTOR_TYPES if t[0] == factor_type][0]

    @property
    def type_label(self):
        return self.get_type_label(self.type)

    @property
    def remain(self):
        bed, bes = AccountBalance.get_bed_bes(self.account, self.floatAccount, self.costCenter)
        remain_value = abs(bed - bes)
        remain_type = "bed" if bed > bes else "bes"
        if self.type in ('buy', 'backFromSale'):
            after_factor_title = 'مبلغ قابل پرداخت'
            if remain_type == 'bes':
                before_factor = self.total_sum + remain_value
                sign = '+'
                before_factor_title = 'مانده بستانکار'
            else:
                before_factor = self.total_sum - remain_value
                sign = '-'
                before_factor_title = 'مانده بدهکار'
        else:
            after_factor_title = 'مبلغ قابل دریافت'
            if remain_type == 'bes':
                before_factor = self.total_sum - remain_value
                sign = '-'
                before_factor_title = 'مانده بستانکار'
            else:
                before_factor = self.total_sum + remain_value
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

    def verify_items(self, items_data, ids_to_delete=()):
        """
        Sample input:
        :param items_data: [{"ware": 1, "warehouse": 2, "count": 3, "fee": 4}, ...]
        :param ids_to_delete: [1, 2, 3]
        :return: None
        """

        if not self.financial_year.is_advari and self.is_definite:

            # Verify item deletions
            for item in FactorItem.objects.filter(id__in=ids_to_delete):
                if not item.is_editable:
                    raise ValidationError("ردیف غیر قابل حذف می باشد")

            rows_to_verify = items_data.copy()

            for row in rows_to_verify.copy():

                # skip not changed items
                is_not_changed = False
                for item in self.items.all():
                    if (
                            row['ware'] == item.ware_id
                            and row['warehouse'] == item.warehouse_id
                            and Decimal(row['count']) == item.count
                            and Decimal(row.get('fee', 0)) == item.fee
                    ):
                        is_not_changed = True
                        break

                if is_not_changed:
                    continue

                # Verify new or changed items
                count = FactorItem.objects.filter(
                    ~Q(factor=self),
                    ware_id=row['ware'],
                    warehouse_id=row['warehouse'],
                    financial_year=self.financial_year,
                    factor__is_definite=True,
                    factor__definition_date__gt=self.definition_date,
                )
                count = count.count()

                if count == 0:
                    continue

                raise ValidationError("ردیف {} غیر قابل ثبت می باشد".format(items_data.index(row) + 1))

        # Check items for back factors
        if self.backFrom:
            for item_data in items_data:
                item_exists = False
                for item in self.items.all():
                    if item_data['ware'] == item.ware_id:
                        item_exists = True
                        if item_data['count'] > item.count:
                            raise ValidationError("تعداد ردیف {} بیشتر از تعداد فاکتور اصلی می باشد.".format(
                                items_data.index(item_data) + 1
                            ))
                        break
                if not item_exists:
                    ware = Ware.objects.get(pk=item_data['ware'])
                    raise ValidationError("کالای {} در فاکتور اصلی وجود ندارد".format(ware.name))

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

    @staticmethod
    def get_first_period_inventory(financial_year=None):
        try:
            return Factor.objects.inFinancialYear(financial_year).get(code=0)
        except Factor.DoesNotExist:
            return None

    @staticmethod
    def get_new_code(factor_type):
        data = Factor.objects.inFinancialYear().filter(type=factor_type).aggregate(
            code=Coalesce(Max('code'), 0),
        )
        return data['code'] + 1

    @staticmethod
    def get_new_temporary_code(factor_type):
        data = Factor.objects.inFinancialYear().filter(type=factor_type).aggregate(
            temporary_code=Coalesce(Max('temporary_code'), 0),
        )
        return data['temporary_code'] + 1

    @property
    def is_deletable(self):

        if self.financial_year.is_advari:
            return True

        if self.is_definite:
            for item in self.items.all():
                if not item.is_editable:
                    return False
            return True
        else:
            return True

    def save(self, *args, **kwargs) -> None:
        self.total_sum = self.sum - self.discountSum + self.taxSum
        self.is_settled = self.total_sum == self.paidValue
        super(Factor, self).save(*args, **kwargs)


class FactorExpense(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factor_expenses')
    expense = models.ForeignKey(Expense, on_delete=models.PROTECT, related_name='factorExpenses')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='expenses')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factorExpenses')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorExpenses', blank=True,
                                     null=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorExpensesAsCostCenter',
                                   blank=True, null=True)
    value = DECIMAL()
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
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='factorPayments')
    value = DECIMAL()

    class Meta(BaseModel.Meta):
        unique_together = ('factor', 'transaction')


class FactorItem(BaseModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_ware = self.ware
        self.initial_warehouse = self.warehouse
        self.initial_count = self.count
        self.initial_fee = self.fee

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='factor_items')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='items')
    ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='factorItems')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='factorItems', null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='factorItems', null=True,
                                  blank=True)

    unit_count = models.DecimalField(max_digits=24, decimal_places=6)
    count = models.DecimalField(max_digits=24, decimal_places=6)
    fee = models.DecimalField(max_digits=24, decimal_places=6)

    # Used for undo definition for output factors to increase inventory
    fees = JSONField(default=get_empty_array)

    remain_fees = JSONField(default=get_empty_array)
    discountValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    discountPercent = models.IntegerField(default=0, null=True, blank=True)
    explanation = models.CharField(max_length=255, blank=True)

    # this is used for inventory reports and sanads.
    # it's equals to fee's count * fee's fee
    calculated_value = models.DecimalField(default=0, max_digits=24, decimal_places=0, blank=True)

    order = models.IntegerField(default=0)

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
        return round(count, 2)

    @property
    def remain_value(self):
        value = 0
        for fee in self.remain_fees:
            value += fee['count'] * fee['fee']
        return round(value, 2)

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
    def tax(self):
        if self.factor.taxPercent:
            return self.value * self.factor.taxPercent / 100
        else:
            return 0

    @property
    def totalValue(self):
        return self.value - self.discount + self.tax

    @property
    def is_ware_last_definite_factor_item(self):
        count = FactorItem.objects.filter(
            ware=self.ware,
            warehouse=self.warehouse,
            financial_year=self.financial_year,
            factor__is_definite=True,
            factor__definition_date__gt=self.factor.definition_date
        ).count()
        return count == 0

    @property
    def is_editable(self):
        if self.factor.is_definite:
            return self.is_ware_last_definite_factor_item
        return True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.discountValue = self.discount
        self.calculated_value = 0
        if self.financial_year.is_advari and self.financial_year.are_factors_sorted:
            self.financial_year.are_factors_sorted = False
            self.financial_year.save()
        for fee in self.fees:
            self.calculated_value += fee['count'] * fee['fee']
        return super(FactorItem, self).save(force_insert, force_update, using, update_fields)


def get_factor_permission_basename(factor_type):
    base_codename = ''
    if factor_type == Factor.BUY:
        base_codename = 'buy'
    elif factor_type == Factor.SALE:
        base_codename = 'sale'
    elif factor_type == Factor.BACK_FROM_BUY:
        base_codename = 'backFromBuy'
    elif factor_type == Factor.BACK_FROM_SALE:
        base_codename = 'backFromSale'
    elif factor_type == Factor.CONSUMPTION_WARE:
        base_codename = 'consumptionWare'
    elif factor_type == Factor.FIRST_PERIOD_INVENTORY:
        return 'update.firstPeriodInventory'
    return "{}Factor".format(base_codename)
