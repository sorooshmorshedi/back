from decimal import Decimal

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
from distributions.models.distribution_model import Distribution
from distributions.models.path_model import Path
from factors.models.expense import Expense
from helpers.db import get_empty_array
from helpers.models import BaseModel, DECIMAL, DefinableMixin, LockableMixin
from helpers.views.MassRelatedCUD import MassRelatedCUD
from sanads.models import Sanad
from transactions.models import Transaction
from wares.models import Ware, Unit, Warehouse


class Factor(BaseModel, DefinableMixin, LockableMixin):
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

    RECEIPT = 'rc'
    REMITTANCE = 'rm'

    PRODUCTION = 'p'

    FACTOR_TYPES = (
        (BUY, 'خرید'),
        (SALE, 'فروش'),
        (BACK_FROM_BUY, 'بازگشت از خرید'),
        (BACK_FROM_SALE, 'بازگشت از فروش'),
        (FIRST_PERIOD_INVENTORY, 'موجودی اول دوره'),
        (INPUT_TRANSFER, 'وارده از انتقال'),
        (OUTPUT_TRANSFER, 'صادره با انتقال'),
        (CONSUMPTION_WARE, 'حواله کالای مصرفی'),
        *ADJUSTMENT_TYPES,
        (RECEIPT, 'رسید'),
        (REMITTANCE, 'حواله'),
        (PRODUCTION, 'تولید'),
    )

    BUY_GROUP = (BUY, BACK_FROM_SALE, FIRST_PERIOD_INVENTORY, PRODUCTION)
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

    after_rows_explanation = models.TextField(blank=True, null=True)
    bottom_explanation = models.TextField(blank=True, null=True)

    is_pre_factor = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        permissions = (
            ('get.buyFactor', 'مشاهده فاکتور خرید'),
            ('create.buyFactor', 'تعریف فاکتور خرید'),
            ('update.buyFactor', 'ویرایش فاکتور خرید'),
            ('delete.buyFactor', 'حذف فاکتور خرید'),
            ('define.buyFactor', 'قطعی کردن فاکتور خرید'),
            ('lock.buyFactor', 'قفل کردن فاکتور خرید'),

            ('get.saleFactor', 'مشاهده فاکتور فروش'),
            ('create.saleFactor', 'تعریف فاکتور فروش'),
            ('update.saleFactor', 'ویرایش فاکتور فروش'),
            ('delete.saleFactor', 'حذف فاکتور فروش'),
            ('define.saleFactor', 'قطعی کردن فاکتور فروش'),
            ('lock.saleFactor', 'قفل کردن فاکتور فروش'),

            ('get.backFromSaleFactor', 'مشاهده فاکتور برگشت از فروش'),
            ('create.backFromSaleFactor', 'تعریف فاکتور برگشت از فروش'),
            ('update.backFromSaleFactor', 'ویرایش فاکتور برگشت از فروش'),
            ('delete.backFromSaleFactor', 'حذف فاکتور برگشت از فروش'),
            ('define.backFromSaleFactor', 'قطعی کردن فاکتور برگشت از فروش'),
            ('lock.backFromSaleFactor', 'قفل کردن فاکتور برگشت از فروش'),

            ('get.backFromBuyFactor', 'مشاهده فاکتور برگشت از خرید'),
            ('create.backFromBuyFactor', 'تعریف فاکتور برگشت از خرید'),
            ('update.backFromBuyFactor', 'ویرایش فاکتور برگشت از خرید'),
            ('delete.backFromBuyFactor', 'حذف فاکتور برگشت از خرید'),
            ('define.backFromBuyFactor', 'قطعی کردن فاکتور برگشت از خرید'),
            ('lock.backFromBuyFactor', 'قفل کردن فاکتور برگشت از خرید'),

            ('get.consumptionWareFactor', 'مشاهده حواله کالای مصرفی'),
            ('create.consumptionWareFactor', 'تعریف حواله کالای مصرفی'),
            ('update.consumptionWareFactor', 'ویرایش حواله کالای مصرفی'),
            ('delete.consumptionWareFactor', 'حذف حواله کالای مصرفی'),
            ('define.consumptionWareFactor', 'قطعی کردن حواله کالای مصرفی'),
            ('lock.consumptionWareFactor', 'قفل کردن حواله کالای مصرفی'),

            ('get.notPaidFactor', 'مشاهده فاکتور های پرداخت نشده'),
            ('get.notReceivedFactor', 'مشاهده فاکتور های دریافت نشده'),

            ('getOwn.buyFactor', 'مشاهده فاکتور خرید خود'),
            ('updateOwn.buyFactor', 'ویرایش فاکتور های خرید خود'),
            ('deleteOwn.buyFactor', 'حذف فاکتور های خرید خود'),
            ('defineOwn.buyFactor', 'قطعی کردن فاکتور های خرید خود'),
            ('lockOwn.buyFactor', 'قفل کردن فاکتور های خرید خود'),

            ('getOwn.saleFactor', 'مشاهده فاکتور های فروش خود'),
            ('updateOwn.saleFactor', 'ویرایش فاکتور های فروش خود'),
            ('deleteOwn.saleFactor', 'حذف فاکتور های فروش خود'),
            ('defineOwn.saleFactor', 'قطعی کردن فاکتور های فروش خود'),
            ('lockOwn.saleFactor', 'قفل کردن فاکتور های فروش خود'),

            ('getOwn.backFromSaleFactor', 'مشاهده فاکتور های برگشت از فروش خود'),
            ('updateOwn.backFromSaleFactor', 'ویرایش فاکتور های برگشت از فروش خود'),
            ('deleteOwn.backFromSaleFactor', 'حذف فاکتور های برگشت از فروش خود'),
            ('defineOwn.backFromSaleFactor', 'قطعی کردن فاکتور های برگشت از فروش خود'),
            ('lockOwn.backFromSaleFactor', 'قفل کردن فاکتور های برگشت از فروش خود'),

            ('getOwn.backFromBuyFactor', 'مشاهده فاکتور های برگشت از خرید خود'),
            ('updateOwn.backFromBuyFactor', 'ویرایش فاکتور های برگشت از خرید خود'),
            ('deleteOwn.backFromBuyFactor', 'حذف فاکتور های برگشت از خرید خود'),
            ('defineOwn.backFromBuyFactor', 'قطعی کردن فاکتور های برگشت از خرید خود'),
            ('lockOwn.backFromBuyFactor', 'قفل کردن فاکتور های برگشت از خرید خود'),

            ('getOwn.consumptionWareFactor', 'مشاهده حواله کالای مصرفی خود'),
            ('updateOwn.consumptionWareFactor', 'ویرایش حواله کالای مصرفی خود'),
            ('deleteOwn.consumptionWareFactor', 'حذف حواله کالای مصرفی خود'),
            ('defineOwn.consumptionWareFactor', 'قطعی کردن حواله کالای مصرفی خود'),
            ('lockOwn.consumptionWareFactor', 'قفل کردن حواله کالای مصرفی خود'),

            ('getOwn.notPaidFactor', 'مشاهده فاکتور های پرداخت نشده خود'),
            ('getOwn.notReceivedFactor', 'مشاهده فاکتور های دریافت نشده خود'),

            ('get.firstPeriodInventory', 'مشاهده موجودی اول دوره'),
            ('update.firstPeriodInventory', 'ثبت موجودی اول دوره'),

            ('create.buyPreFactor', 'تعریف پیش فاکتور خرید'),

            ('get.buyPreFactor', 'مشاهده پیش فاکتور خرید'),
            ('update.buyPreFactor', 'ویرایش پیش فاکتور خرید'),
            ('delete.buyPreFactor', 'حذف پیش فاکتور خرید'),
            ('convert.buyPreFactor', 'تبدیل پیش فاکتور خرید به فاکتور'),

            ('getOwn.buyPreFactor', 'مشاهده پیش فاکتور خرید خود'),
            ('updateOwn.buyPreFactor', 'ویرایش پیش فاکتور خرید خود'),
            ('deleteOwn.buyPreFactor', 'حذف پیش فاکتور خرید خود'),
            ('convertOwn.buyPreFactor', 'تبدیل پیش فاکتور خرید خود به فاکتور'),

            ('create.salePreFactor', 'تعریف پیش فاکتور فروش'),

            ('get.salePreFactor', 'مشاهده پیش فاکتور فروش'),
            ('update.salePreFactor', 'ویرایش پیش فاکتور فروش'),
            ('delete.salePreFactor', 'حذف پیش فاکتور فروش'),
            ('convert.salePreFactor', 'تبدیل پیش فاکتور فروش به فاکتور'),

            ('getOwn.salePreFactor', 'مشاهده پیش فاکتور فروش خود'),
            ('updateOwn.salePreFactor', 'ویرایش پیش فاکتور فروش خود'),
            ('deleteOwn.salePreFactor', 'حذف پیش فاکتور فروش خود'),
            ('convertOwn.salePreFactor', 'تبدیل پیش فاکتور فروش خود به فاکتور'),

            ('create.receipt', 'تعریف رسید'),

            ('get.receipt', 'مشاهده رسید'),
            ('update.receipt', 'ویرایش رسید'),
            ('delete.receipt', 'حذف رسید'),

            ('getOwn.receipt', 'مشاهده رسید های خود'),
            ('updateOwn.receipt', 'ویرایش رسید های خود'),
            ('deleteOwn.receipt', 'حذف رسید های خود'),

            ('create.remittance', 'تعریف حواله'),

            ('get.remittance', 'مشاهده حواله'),
            ('update.remittance', 'ویرایش حواله'),
            ('delete.remittance', 'حذف حواله'),

            ('getOwn.remittance', 'مشاهده حواله های خود'),
            ('updateOwn.remittance', 'ویرایش حواله های خود'),
            ('deleteOwn.remittance', 'حذف حواله های خود'),

            ('create.production', 'تعریف تولید'),

            ('get.production', 'مشاهده تولید'),
            ('update.production', 'ویرایش تولید'),
            ('delete.production', 'حذف تولید'),

            ('getOwn.production', 'مشاهده تولید های خود'),
            ('updateOwn.production', 'ویرایش تولید های خود'),
            ('deleteOwn.production', 'حذف تولید های خود'),

        )

    def __str__(self):
        return "ID: {}, code: {}, type: {}, is_defined: {}".format(self.pk, self.code, self.type, self.is_defined)

    @property
    def sum(self):
        sum = 0
        for i in self.items.all():
            sum += i.fee * i.unit_count
        return sum

    @property
    def rows_sum_after_tax(self):
        sum = 0
        for item in self.items.all():
            sum += item.totalValue
        return sum

    @property
    def calculated_sum(self):
        sum = 0
        for item in self.items.all():
            sum += item.calculated_value
        return sum

    @property
    def factor_discount(self):
        if self.discountPercent:
            discount = self.discountPercent * self.rows_sum_after_tax / 100
        else:
            discount = self.discountValue
        return discount

    @property
    def discountSum(self):
        discountSum = self.factor_discount
        for i in self.items.all():
            discountSum += i.discount
        return discountSum

    @property
    def taxSum(self):
        tax_sum = self.taxValue
        for item in self.items.all():
            tax_sum += item.tax
        return tax_sum

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

    def verify_items(self, items_data, ids_to_delete=()):
        """
        Sample input:
        :param items_data: [{"ware": 1, "warehouse": 2, "count": 3, "fee": 4}, ...]
        :param ids_to_delete: [1, 2, 3]
        :return: None
        """

        if not self.financial_year.is_advari and self.is_defined:

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
                            and float(row['count']) == float(item.count)
                            and float(row.get('fee', 0)) == float(item.fee)
                    ):
                        is_not_changed = True
                        break

                if is_not_changed:
                    continue

                # Verify new or changed items
                qs = FactorItem.objects.filter(
                    ~Q(factor=self),
                    ware_id=row['ware'],
                    warehouse_id=row['warehouse'],
                    financial_year=self.financial_year,
                    factor__is_defined=True,
                    factor__definition_date__gt=self.definition_date,
                )
                count = qs.count()

                if count == 0:
                    continue

                ware = Ware.objects.get(pk=row['ware'])

                raise ValidationError({
                    "non_field_errors": [
                        "ردیف {} ({}) غیر قابل ثبت می باشد".format(items_data.index(row) + 1, ware.name),
                    ],
                    "why": {
                        'is_not_changed': is_not_changed,
                        'newer_factors': qs.values_list('factor_id', flat=True)
                    },
                })

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
        data = Factor.objects.inFinancialYear().filter(
            type=factor_type,
        ).aggregate(
            code=Coalesce(Max('code'), 0),
        )
        return data['code'] + 1

    @staticmethod
    def get_new_temporary_code(factor_type, is_pre_factor=False):
        data = Factor.objects.inFinancialYear().filter(
            type=factor_type,
            is_pre_factor=is_pre_factor
        ).aggregate(
            temporary_code=Coalesce(Max('temporary_code'), 0),
        )
        return data['temporary_code'] + 1

    @property
    def is_deletable(self):

        if self.financial_year.is_advari:
            return True

        if self.is_defined:
            for item in self.items.all():
                if not item.is_editable:
                    return False
            return True
        else:
            return True

    @property
    def export_data(self):
        sums = {
            'unit_count': 0,
            'sum': 0,
            'discount': 0,
            'tax': 0,
            'sum_after_tax': 0
        }
        for item in self.items.all():
            sums['unit_count'] += item.unit_count
            sums['sum'] += item.value
            sums['discount'] += item.discount
            sums['tax'] += item.tax
            sums['sum_after_tax'] += item.totalValue

        totals = {
            'sum_after_discount': sums['sum_after_tax'] - self.factor_discount
        }

        bed, bes = AccountBalance.get_bed_bes(self.account, self.floatAccount, self.costCenter)
        remain_value = abs(bed - bes)
        remain_type = "bed" if bed > bes else "bes"

        if self.type in ('buy', 'backFromSale'):
            after_factor_title = 'مبلغ قابل پرداخت'
            if remain_type == 'bes':
                value = self.total_sum
                is_negative = False
            else:
                value = -self.total_sum
                is_negative = True
        else:
            after_factor_title = 'مبلغ قابل دریافت'
            if remain_type == 'bes':
                value = -self.total_sum
                is_negative = True
            else:
                value = +self.total_sum
                is_negative = False

        if self.is_defined:
            before_factor = remain_value - value
            after_factor = remain_value
        else:
            before_factor = remain_value
            after_factor = remain_value + value

        remains = {
            'before_factor': abs(before_factor),
            'after_factor_title': after_factor_title,
            'after_factor': after_factor,
            'is_negative': is_negative
        }

        return {
            'sums': sums,
            'totals': totals,
            'remains': remains
        }

    def save(self, *args, **kwargs) -> None:
        self.financial_year.check_date(self.date)

        self.total_sum = Decimal(self.rows_sum_after_tax) - Decimal(self.factor_discount) + self.taxValue
        self.is_settled = self.total_sum == self.paidValue
        self.discountValue = self.factor_discount
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

    tax_value = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    tax_percent = models.IntegerField(default=0, null=True, blank=True)

    explanation = models.CharField(max_length=255, blank=True)

    # this is used for inventory reports and sanads.
    # it's equals to fee's count * fee's fee
    calculated_value = models.DecimalField(default=0, max_digits=24, decimal_places=0, blank=True)

    order = models.IntegerField(default=0)

    preFactorItem = models.OneToOneField('self', on_delete=models.PROTECT, related_name='factorItem', blank=True,
                                         null=True)

    meta = JSONField(default=dict)

    def __str__(self):
        return "factor id: {}, factor type: {}, is_defined: {}, ware: {}, count: {}".format(
            self.factor.id,
            self.factor.type,
            self.factor.is_defined,
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
        return self.fee * self.unit_count

    @property
    def discount(self):
        if self.discountPercent:
            return self.value * self.discountPercent / 100
        else:
            return self.discountValue

    @property
    def tax(self):
        if self.tax_percent:
            return (self.value - self.discount) * self.tax_percent / 100
        else:
            return self.tax_value

    @property
    def totalValue(self):
        return self.value - self.discount + self.tax

    @property
    def is_ware_last_definite_factor_item(self):
        qs = FactorItem.objects.filter(
            ware=self.ware,
            warehouse=self.warehouse,
            financial_year=self.financial_year,
            factor__is_defined=True,
            factor__definition_date__gt=self.factor.definition_date
        )
        is_last = qs.count() == 0
        return is_last

    @property
    def is_editable(self):
        if self.factor.is_defined:
            return self.is_ware_last_definite_factor_item
        return True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.discountValue = self.discount
        self.tax_value = self.tax
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
