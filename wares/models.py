from django.db import models
from django_jalali.db import models as jmodels
from accounts.accounts.models import Account
from companies.models import FinancialYear
from helpers.functions import get_current_user
from helpers.models import BaseModel


class Unit(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True

    def __str__(self):
        return self.name


class Warehouse(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='warehouses')
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True

    def __str__(self):
        return str(self.pk) + ' - ' + self.name


class WareLevel(BaseModel):
    NATURE = 0
    GROUP = 1
    CATEGORY = 2
    WARE_LEVELS = (
        (NATURE, 'nature'),
        (GROUP, 'group'),
        (CATEGORY, 'category'),
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='wareLevels')
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)
    level = models.IntegerField(choices=WARE_LEVELS)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        unique_together = ('name', 'level')

    def __str__(self):
        return str(self.pk) + ' - ' + self.name


class Ware(BaseModel):
    FIFO = 0
    WEIGHTED_MEAN = 1
    PRICING_TYPES = {
        (FIFO, 'فایفو'),
        (WEIGHTED_MEAN, 'میانگین موزون'),
    }

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='wares')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    isDisabled = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=24, decimal_places=0)
    pricingType = models.IntegerField(choices=PRICING_TYPES, null=True, blank=True)
    minSale = models.IntegerField(blank=True, null=True)
    maxSale = models.IntegerField(blank=True, null=True)
    minInventory = models.IntegerField(blank=True, null=True)
    maxInventory = models.IntegerField(blank=True, null=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    category = models.ForeignKey(WareLevel, on_delete=models.PROTECT, related_name='wares')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='wares', null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='wares')
    supplier = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True)

    isService = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        ordering = ['code', ]
        backward_financial_year = True

    def has_factorItem(self):
        return self.factorItems.count() != 0

    def has_inventory(self):
        pass

    def last_factor_item(self, user, exclude_factors=None, other_filters=None):
        try:
            from factors.models import FactorItem
            from factors.models import Factor
            from django.db.models import Q
            last_factor_item = FactorItem.objects.inFinancialYear().filter(ware=self) \
                .filter(factor__is_definite=True, factor__type__in=(*Factor.SALE_GROUP, *Factor.BUY_GROUP)) \
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

    def calculated_output_value(self, user, count, last_factor_item=None):
        if not last_factor_item:
            last_factor_item = self.last_factor_item(user)
        if self.pricingType == self.WEIGHTED_MEAN:
            return self.calculated_output_value_for_weighted_mean(user, count, last_factor_item)
        else:
            return self.calculated_output_value_for_fifo(user, count, last_factor_item)

    def calculated_output_value_for_weighted_mean(self, user, count, last_factor_item):
        remain_value = last_factor_item.remain_value
        remain_count = last_factor_item.remain_count
        fee = remain_value / remain_count

        return fee * count, [{'fee': fee, 'count': count}]

    def initial_factor_item_and_count_for_fifo(self, user, last_factor_item):
        from factors.models import Factor

        total_output = last_factor_item.total_output_count

        # find first usable factor item
        initialFactorItem = self.factorItems.inFinancialYear() \
            .filter(factor__type__in=Factor.BUY_GROUP, factor__is_definite=True) \
            .order_by('factor__definition_date', 'id') \
            .filter(total_input_count__gt=total_output) \
            .first()

        count = initialFactorItem.total_input_count - total_output

        return initialFactorItem, count

    def calculated_output_value_for_fifo(self, user, needed_count, last_factor_item):
        from factors.models import Factor

        initialFactorItem, count = self.initial_factor_item_and_count_for_fifo(user, last_factor_item)

        factorItems = self.factorItems.inFinancialYear() \
            .filter(factor__is_definite=True, factor__type__in=Factor.BUY_GROUP) \
            .order_by('factor__definition_date', 'id')

        initial_factor_definition_date = initialFactorItem.factor.definition_date
        initial_factor_item_id = initialFactorItem.id
        if initial_factor_definition_date:
            factorItems = factorItems.filter(factor__definition_date__gte=initial_factor_definition_date,
                                             id__gte=initial_factor_item_id)

        total_value = 0
        fees = []
        uneditableFactorItemIds = []
        for factorItem in factorItems.all():

            if needed_count == 0:
                break

            uneditableFactorItemIds.append(factorItem.id)

            if factorItem != initialFactorItem:
                count = factorItem.count

            fee = factorItem.fee
            if needed_count < count:
                total_value += needed_count * fee
                count -= needed_count
                fees.append({
                    'fee': fee,
                    'count': needed_count
                })
                break
            elif needed_count > count:
                total_value += count * fee
                needed_count -= count
                fees.append({
                    'fee': fee,
                    'count': count
                })
            else:
                total_value += count * fee
                fees.append({
                    'fee': fee,
                    'count': count
                })
                needed_count = 0

        return total_value, fees


class WareInventory(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='waresBalance')
    ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='balance')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='balance')
    count = models.DecimalField(max_digits=24, decimal_places=6, default=0)

    class Meta(BaseModel.Meta):
        pass

    @staticmethod
    def update_inventory(ware: Ware, warehouse: Warehouse, change):
        user = get_current_user()
        ware_balance, created = WareInventory.objects.get_or_create(
            ware=ware,
            warehouse=warehouse,
            financial_year=user.active_financial_year
        )
        ware_balance.count += change
        ware_balance.save()

    @staticmethod
    def get_inventory_count(ware: Ware, warehouse: Warehouse):
        user = get_current_user()
        ware_balance, created = WareInventory.objects.get_or_create(
            ware=ware,
            warehouse=warehouse,
            financial_year=user.active_financial_year
        )
        return ware_balance.count

    @staticmethod
    def get_inventory(ware: Ware):
        ware_balances = WareInventory.objects.inFinancialYear().filter(ware=ware)
        return ware_balances
