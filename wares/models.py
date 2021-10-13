import decimal
import logging

from django.db import models
from django.db.models.aggregates import Sum, Max, Min
from django.db.models.functions.comparison import Coalesce
from django_jalali.db import models as jmodels
from rest_framework.exceptions import ValidationError

from companies.models import FinancialYear
from helpers.bale import Bale
from helpers.functions import get_current_user, get_new_child_code
from helpers.models import BaseModel, DECIMAL


class Unit(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        ordering = ('pk',)
        permission_basename = 'unit'
        permissions = (
            ('get.unit', 'مشاهده واحد'),
            ('create.unit', 'تعریف واحد'),
            ('update.unit', 'ویرایش واحد'),
            ('delete.unit', 'حذف واحد'),

            ('getOwn.unit', 'مشاهده واحد های خود'),
            ('updateOwn.unit', 'ویرایش واحد های خود'),
            ('deleteOwn.unit', 'حذف واحد های خود'),
        )

    def __str__(self):
        return self.name


class Warehouse(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='warehouses')
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'warehouse'
        permissions = (
            ('get.warehouse', 'مشاهده انبار'),
            ('create.warehouse', 'تعریف انبار'),
            ('update.warehouse', 'ویرایش انبار'),
            ('delete.warehouse', 'حذف انبار'),

            ('getOwn.warehouse', 'مشاهده انبار های خود'),
            ('updateOwn.warehouse', 'ویرایش انبار های خود'),
            ('deleteOwn.warehouse', 'حذف انبار های خود'),
        )

    def __str__(self):
        return str(self.pk) + ' - ' + self.name


class Ware(BaseModel):
    CODE_LENGTHS = [2, 2, 2, 3]

    NATURE = 0
    GROUP = 1
    CATEGORY = 2
    WARE = 3
    WARE_LEVELS = (
        (NATURE, 'nature'),
        (GROUP, 'group'),
        (CATEGORY, 'category'),
        (WARE, 'ware'),
    )

    FIFO = 'f'
    WEIGHTED_MEAN = 'wm'
    PRICING_TYPES = (
        (FIFO, 'فایفو'),
        (WEIGHTED_MEAN, 'میانگین موزون'),
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='wares')

    # if True allows ware inventory become negative
    check_inventory = models.BooleanField(default=True)

    level = models.IntegerField(choices=WARE_LEVELS)
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)

    barcode = models.CharField(max_length=50, blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    isDisabled = models.BooleanField(default=False)
    pricingType = models.CharField(max_length=2, choices=PRICING_TYPES, null=True, blank=True)
    minSale = models.IntegerField(blank=True, null=True)
    maxSale = models.IntegerField(blank=True, null=True)
    minInventory = models.IntegerField(blank=True, null=True)
    maxInventory = models.IntegerField(blank=True, null=True)

    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='wares', null=True, blank=True)

    is_service = models.BooleanField(default=False)

    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)

    commission_percent = models.IntegerField(blank=True, default=0)

    @property
    def main_unit(self) -> Unit:
        salePrice = self.salePrices.filter(conversion_factor=1).first()
        if salePrice:
            return salePrice.unit
        return None

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        ordering = ['code', ]
        backward_financial_year = True
        permission_basename = 'ware'
        permissions = (
            ('get.ware', 'مشاهده کالا'),
            ('create.ware', 'تعریف کالا'),
            ('update.ware', 'ویرایش کالا'),
            ('delete.ware', 'حذف کالا'),

            ('getOwn.ware', 'مشاهده کالا های خود'),
            ('updateOwn.ware', 'ویرایش کالا های خود'),
            ('deleteOwn.ware', 'حذف کالا های خود'),

            ('sort.inventory', 'مرتب سازی کاردکس کالا'),
        )

    def get_new_child_code(self):
        last_child_code = None

        last_child = self.children.order_by('-code').first()
        if last_child:
            last_child_code = last_child.code

        return get_new_child_code(
            self.code,
            self.CODE_LENGTHS[self.level + 1],
            last_child_code
        )

    @staticmethod
    def get_new_nature_code():
        code = Ware.objects.inFinancialYear().filter(level=Ware.NATURE).aggregate(
            last_code=Max('code')
        )['last_code']

        if code:
            code = int(code) + 1
        else:
            code = 0

        if code < 9:
            code += 10

        if code >= 99:
            from rest_framework import serializers
            raise serializers.ValidationError("تعداد عضو های این سطح پر شده است")

        return str(code)

    def has_factorItem(self):
        return self.factorItems.count() != 0

    def has_inventory(self):
        pass

    def last_factor_item(self, user, exclude_factors=None, other_filters=None):
        try:
            from factors.models.factor import FactorItem
            from factors.models import Factor
            from django.db.models import Q
            last_factor_item = FactorItem.objects.inFinancialYear().filter(ware=self) \
                .filter(factor__is_defined=True, factor__type__in=(*Factor.SALE_GROUP, *Factor.BUY_GROUP)) \
                .order_by('-factor__definition_date', '-id')

            if exclude_factors:
                last_factor_item = last_factor_item.filter(~Q(factor__in=exclude_factors))

            if other_filters:
                last_factor_item = last_factor_item.filter(**other_filters)

            return last_factor_item[0]
        except IndexError:
            return None

    def get_inventory_count(self, warehouse: Warehouse):
        return WareInventory.get_inventory_count(self, warehouse)

    def remain(self, user, last_factor_item=None):
        res = {
            'count': 0,
            'value': 0,
            'last_factor_item': None,
        }
        if not last_factor_item:
            last_factor_item = self.last_factor_item(user)
        factor_item = last_factor_item
        if factor_item:
            res['count'] = factor_item.remain_count
            res['value'] = factor_item.remain_value
            res['last_factor_item'] = factor_item
        return res


class SalePriceType(BaseModel):
    name = models.CharField(max_length=100)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    class Meta(BaseModel.Meta):
        permission_basename = 'salePriceType'
        ordering = ('id',)
        permissions = (
            ('get.salePriceType', 'مشاهده نوع های نرخ فروش '),
            ('create.salePriceType', 'تعریف نوع های نرخ فروش '),
            ('update.salePriceType', 'ویرایش نوع های نرخ فروش '),
            ('delete.salePriceType', 'حذف نوع های نرخ فروش '),

            ('getOwn.salePriceType', 'مشاهده نوع های نرخ فروش خود'),
            ('updateOwn.salePriceType', 'ویرایش نوع های نرخ فروش خود'),
            ('deleteOwn.salePriceType', 'حذف نوع های نرخ فروش خود'),
        )
        backward_financial_year = True


class SalePrice(BaseModel):
    type = models.ForeignKey(SalePriceType, on_delete=models.PROTECT, null=True)

    ware = models.ForeignKey(Ware, on_delete=models.CASCADE, related_name='salePrices')

    mainUnit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='salePricesAsMainUnit', null=True)
    conversion_factor = DECIMAL(default=1)

    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='salePrices')
    price = DECIMAL(null=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        unique_together = ('ware', 'unit', 'type')
        ordering = ('pk',)
        permission_basename = 'salePrice'
        permissions = (
            ('get.salePrice', 'مشاهده قیمت فروش'),
            ('create.salePrice', 'تعریف قیمت فروش'),
            ('update.salePrice', 'ویرایش قیمت فروش'),
            ('delete.salePrice', 'حذف قیمت فروش'),

            ('getOwn.salePrice', 'مشاهده قیمت های فروش خود'),
            ('updateOwn.salePrice', 'ویرایش قیمت های فروش خود'),
            ('deleteOwn.salePrice', 'حذف قیمت های فروش خود'),
        )


class SalePriceChange(BaseModel):
    is_increase = models.BooleanField()
    is_percent = models.BooleanField()
    rate = DECIMAL()

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        ordering = ('-pk',)
        permission_basename = 'salePriceChange'
        permissions = (
            ('get.salePriceChange', 'مشاهده تغییرات قیمت فروش'),
            ('getOwn.salePriceChange', 'مشاهده تغییرات قیمت های فروش خود'),
        )


class WareSalePriceChange(BaseModel):
    salePriceChange = models.ForeignKey(SalePriceChange, on_delete=models.CASCADE)
    salePrice = models.ForeignKey(SalePrice, on_delete=models.CASCADE)

    previous_price = DECIMAL()
    new_price = DECIMAL()

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        ordering = ('pk',)
        permission_basename = ''
        permissions = ()


class WareInventory(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='waresInventories')
    ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='inventory')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='inventory')
    count = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    fee = models.DecimalField(max_digits=24, decimal_places=6, default=0)

    order = models.IntegerField(default=0)

    logger = logging.getLogger('inventory')

    class Meta(BaseModel.Meta):
        ordering = ['order']

    def __str__(self):
        return "{} - {} - {} - {} {} ({})".format(
            self.financial_year.id,
            self.ware.id,
            self.warehouse.id,
            self.count,
            self.fee,
            self.id
        )

    @staticmethod
    def _get_order(ware: Ware, warehouse: Warehouse, revert=False):
        qs = WareInventory.objects.filter(ware=ware, warehouse=warehouse)

        if revert:
            return qs.aggregate(min_order=Coalesce(Min('order'), 0))['min_order'] - 1
        else:
            return qs.aggregate(max_order=Coalesce(Max('order'), 0))['max_order'] + 1

    @staticmethod
    def increase_inventory(ware: Ware, warehouse: Warehouse, count, fee, financial_year=None, revert=False):
        if not financial_year:
            user = get_current_user()
            financial_year = user.active_financial_year

        log = "Financial Year #{}: inc {} #{} from #{}, revert:{}".format(
            financial_year.id, count, ware.id, warehouse.id, revert
        )
        print(log)
        WareInventory.logger.info(log)

        negative_inventory = WareInventory.objects.filter(
            financial_year=financial_year,
            ware=ware,
            warehouse=warehouse,
            count__lt=0,
        ).first()

        if negative_inventory:
            negative_inventory.count += decimal.Decimal(count)
            negative_inventory.fee = fee
            negative_inventory.save()
        else:
            WareInventory.objects.create(
                ware=ware,
                warehouse=warehouse,
                count=count,
                fee=fee,
                financial_year=financial_year,
                order=WareInventory._get_order(ware, warehouse, revert=revert)
            )

    @staticmethod
    def decrease_inventory(ware: Ware, warehouse: Warehouse, count, financial_year=None, revert=False):
        if not financial_year:
            user = get_current_user()
            financial_year = user.active_financial_year

        log = "Financial Year #{}: dec {} #{} from #{}, revert:{}".format(
            financial_year.id, count, ware.id, warehouse.id, revert
        )
        print(log)
        Bale.to_me(log)
        WareInventory.logger.info(log)

        ware_balances = WareInventory.objects.filter(
            ware=ware,
            warehouse=warehouse,
            financial_year=financial_year
        )

        if revert:
            ware_balances = ware_balances.order_by('-order')
        else:
            ware_balances = ware_balances.order_by('order')

        check_inventory = ware.check_inventory
        current_inventory_count = ware_balances.aggregate(count=Coalesce(Sum('count'), 0))['count']
        Bale.to_me(current_inventory_count, count)
        if check_inventory:
            if not revert and current_inventory_count < count:
                raise ValidationError("موجودی {} کافی نیست، موجودی فعلی: {} {}".format(
                    ware,
                    "{0:g}".format(float(current_inventory_count)),
                    ware.main_unit.name
                ))
        elif ware_balances.count() == 0:
            fee = 0
            WareInventory.increase_inventory(ware, warehouse, -count, fee)
            return [{
                'fee': fee,
                'count': float(count)
            }]
        elif ware_balances.count() == 1:
            ware_balance = ware_balances.first()
            fees = [{
                'fee': float(ware_balance.fee),
                'count': float(count)
            }]
            ware_balance.count -= count
            ware_balance.save()
            return fees

        fees = []

        for ware_balance in ware_balances:

            fee = {
                'fee': float(ware_balance.fee),
            }

            if ware_balance.count == count:
                fee['count'] = float(ware_balance.count)
                fees.append(fee)
                ware_balance.delete()
                break

            elif ware_balance.count < count:
                count -= ware_balance.count
                fee['count'] = float(ware_balance.count)
                fees.append(fee)
                ware_balance.delete()

            elif ware_balance.count > count:
                ware_balance.count -= count
                fee['count'] = float(count)
                fees.append(fee)
                ware_balance.save()
                break

        negative_inventory = current_inventory_count - count
        if not check_inventory and negative_inventory <= 0:
            WareInventory.increase_inventory(ware, warehouse, negative_inventory, fees[0]['fee'])
            fees[0]['count'] += -float(negative_inventory)

        return fees

    @staticmethod
    def get_inventory_count(ware: Ware, warehouse: Warehouse, financial_year=None):
        if not financial_year:
            user = get_current_user()
            financial_year = user.active_financial_year

        ware_balance = WareInventory.objects.filter(
            ware=ware,
            warehouse=warehouse,
            financial_year=financial_year
        ).aggregate(count=Coalesce(Sum('count'), 0))
        return ware_balance['count']

    @staticmethod
    def get_remain_fees(ware: Ware, warehouse: Warehouse = None, financial_year=None):
        if not financial_year:
            user = get_current_user()
            financial_year = user.active_financial_year

        ware_inventories = WareInventory.objects.filter(
            ware=ware,
            financial_year=financial_year
        )

        if warehouse:
            ware_inventories = ware_inventories.filter(
                warehouse=warehouse,
            )

        fees = []
        for ware_inventory in ware_inventories:
            fees.append({
                'count': float(ware_inventory.count),
                'fee': float(ware_inventory.fee),
            })
        return fees
