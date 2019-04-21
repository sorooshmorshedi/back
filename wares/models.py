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

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        ordering = ['code', ]

    def has_factorItem(self):
        # print(self.factorItems.count())
        return self.factorItems.count() != 0

    def has_inventory(self):
        pass

    @property
    def remain_value(self):
        from factors.models import Factor
        total_input = self.factorItems\
            .filter(Q(factor__type__in=Factor.BUY_GROUP))\
            .aggregate(total_value=Sum(F('fee')*F('count'), output_field=models.DecimalField()),
                       total_count=Sum('count'))

        total_output_count = self.factorItems \
            .filter(Q(factor__type__in=Factor.SALE_GROUP)) \
            .aggregate(total_count=Sum('count'))['total_count']

        print(total_input, total_output_count,
              total_input['total_value'] - total_output_count * total_input['total_value'] / total_input['total_count'])
        return 'ha'
        # if self.pricingType == self.WEIGHTED_MEAN:


