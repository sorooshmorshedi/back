from sanads.sanads.models import clearSanad
from wares.models import WareInventory


def clearFactorSanad(sender, instance, **kwargs):
    clearSanad(instance.sanad)


def updateInventoryOnSave(sender, instance, **kwargs):
    from factors.models import Factor
    from factors.models import FactorItem

    factor = instance.factor
    if not factor.is_definite:
        return

    ware = instance.ware
    warehouse = instance.warehouse

    if ware.isService:
        return

    if instance.id:
        factorItem = FactorItem.objects.get(pk=instance.id)
        change = instance.count - factorItem.count
    else:
        change = instance.count

    if instance.factor.type in Factor.INPUT_GROUP:
        WareInventory.update_inventory(ware, warehouse, change)
    else:
        WareInventory.update_inventory(ware, warehouse, -change)


def updateInventoryOnDelete(sender, instance, **kwargs):
    from factors.models import Factor

    factor = instance.factor
    if not factor.is_definite:
        return

    ware = instance.ware
    warehouse = instance.warehouse
    change = instance.count

    if ware.isService:
        return

    if instance.factor.type in Factor.INPUT_GROUP:
        WareInventory.update_inventory(ware, warehouse, -change)
    else:
        WareInventory.update_inventory(ware, warehouse, change)
