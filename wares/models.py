from django.db import models
from django_jalali.db import models as jmodels
from accounts.accounts.models import Account

WARE_LEVELS = (
    (0, 'nature'),
    (1, 'group'),
    (2, 'category'),
)

PRICING_TYPES = {
    (0, 'فایفو'),
    (1, 'میانگین موزون'),
}


class Unit(models.Model):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return str(self.pk) + ' - ' + self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return str(self.pk) + ' - ' + self.name


class WareLevel(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)
    level = models.IntegerField(choices=WARE_LEVELS)

    class Meta:
        default_permissions = ()
        unique_together = ('name', 'level')

    def __str__(self):
        return str(self.pk) + ' - ' + self.name


class Ware(models.Model):
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
        return "{0} - {1}".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]

    def has_factorItem(self):
        # print(self.factorItems.count())
        return self.factorItems.count() == 0

    def has_inventory(self):
        pass


class WarehouseInventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='inventory')
    ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='inventory')
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'ware')

    def __str__(self):
        return "{0} -> {1} : {2}".format(self.warehouse.name, self.ware.name, self.count)


def updateInventory(warehouse, ware, count):
    inventory = WarehouseInventory.objects.filter(warehouse=warehouse, ware=ware)
    if len(inventory):
        inventory = inventory[0]
        inventory.count += count
    else:
        try:
            inventory = WarehouseInventory(
                warehouse=Warehouse.objects.get(pk=warehouse),
                ware=Ware.objects.get(pk=ware),
                count=count,
            )
        except:
            raise {'error': 'invalid ware or warehouse'}
    inventory.save()
    return inventory.count
