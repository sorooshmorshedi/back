from sanads.sanads.models import clearSanad
from wares.models import WareBalance


def clearFactorSanad(sender, instance, **kwargs):
    clearSanad(instance.sanad)


def updateWareBalanceOnSave(sender, instance, **kwargs):
    from factors.models import Factor
    from factors.models import FactorItem

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
        WareBalance.update_balance(ware, warehouse, change)
    else:
        WareBalance.update_balance(ware, warehouse, -change)


def updateWareBalanceOnDelete(sender, instance, **kwargs):
    from factors.models import Factor

    ware = instance.ware
    warehouse = instance.warehouse
    change = instance.count

    if ware.isService:
        return

    if instance.factor.type in Factor.INPUT_GROUP:
        WareBalance.update_balance(ware, warehouse, -change)
    else:
        WareBalance.update_balance(ware, warehouse, change)
