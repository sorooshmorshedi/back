from django.db import models
from django.db.models import F
from django.db.models import Q
from django.db.models import Sum
from django_jalali.db import models as jmodels
from accounts.accounts.models import Account
from helpers.models import BaseModel


class Unit(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        default_permissions = ()

    def __str__(self):
        return self.name


class Warehouse(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        default_permissions = ()

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

    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)
    level = models.IntegerField(choices=WARE_LEVELS)

    class Meta(BaseModel.Meta):
        default_permissions = ()
        unique_together = ('name', 'level')

    def __str__(self):
        return str(self.pk) + ' - ' + self.name


class WareMetaData(BaseModel):

    factor_item_id = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)


class Ware(BaseModel):

    FIFO = 0
    WEIGHTED_MEAN = 1
    PRICING_TYPES = {
        (FIFO, 'فایفو'),
        (WEIGHTED_MEAN, 'میانگین موزون'),
    }

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    isDisabled = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=24, decimal_places=0)
    pricingType = models.IntegerField(choices=PRICING_TYPES)
    minSale = models.IntegerField(blank=True, null=True)
    maxSale = models.IntegerField(blank=True, null=True)
    minInventory = models.IntegerField(blank=True, null=True)
    maxInventory = models.IntegerField(blank=True, null=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    category = models.ForeignKey(WareLevel, on_delete=models.PROTECT, related_name='wares')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='wares')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='wares')
    supplier = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True)
    metadata = models.OneToOneField(WareMetaData, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        ordering = ['code', ]

    def has_factorItem(self):
        return self.factorItems.count() != 0

    def has_inventory(self):
        pass

    def last_factor_item(self, user):
        try:
            return self.factorItems.inFinancialYear(user)\
                .filter(factor__is_definite=True)\
                .order_by('-factor__definition_date')[0]
        except IndexError:
            return None

    def remain(self, user):
        res = {
            'count': 0,
            'value': 0,
        }
        factorItem = self.last_factor_item(user)
        if factorItem:
            res['count'] = factorItem.remain_count
            res['value'] = factorItem.remain_value
        return res

    def calculated_output_value(self, user, count):
        if self.pricingType == self.WEIGHTED_MEAN:
            return self.calculated_output_value_for_weighted_mean(user, count)
        else:
            return self.calculated_output_value_for_fifo(user, count)

    def calculated_output_value_for_weighted_mean(self, user, count):
        lastFactorItem = self.last_factor_item(user)
        remain_value = lastFactorItem.remain_value
        remain_count = lastFactorItem.remain_count
        fee = remain_value / remain_count
        return fee * count

    def calculated_output_value_for_fifo(self, user, needed_count):
        from factors.models import Factor
        if not self.metadata:
            initialFactorItem = self.factorItems.inFinancialYear(user)\
                .filter(factor__is_definite=True, factor__type__in=Factor.BUY_GROUP)\
                .order_by('factor__definition_date')[0]
            metadata = WareMetaData(
                factor_item_id=initialFactorItem.id,
                count=initialFactorItem.count
            )
            metadata.save()
            self.metadata = metadata
            self.save()
        else:
            initialFactorItem = self.factorItems.get(pk=self.metadata.factor_item_id)
            metadata = self.metadata

        factorItems = self.factorItems.inFinancialYear(user) \
            .filter(factor__is_definite=True, factor__type__in=Factor.BUY_GROUP) \
            .order_by('factor__definition_date')

        initial_factor_definition_date = initialFactorItem.factor.definition_date
        if initial_factor_definition_date:
            factorItems = factorItems.filter(factor__definition_date__gte=initial_factor_definition_date)

        total_value = 0
        factorItem = initialFactorItem
        count = metadata.count
        fees = []
        for factorItem in factorItems.all():

            if count == 0:
                break

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
                count = 0

        metadata.factor_item_id = factorItem.id
        metadata.count = count
        metadata.save()

        # print(fees)
        return total_value
