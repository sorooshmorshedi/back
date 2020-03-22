from sanads.sanads.models import clearSanad
from wares.models import WareInventory, Ware


def clearFactorSanad(sender, instance, **kwargs):
    clearSanad(instance.sanad)


def updateInventoryOnFactorDelete(sender, instance, **kwargs):
    for factor_item in instance.items.all():
        updateInventoryOnSanadItemDelete(sender, factor_item)


def updateInventoryOnSanadItemDelete(sender, instance, **kwargs):
    from factors.models import Factor

    factor = instance.factor
    if not factor.is_definite:
        return

    ware = instance.ware
    warehouse = instance.warehouse

    if ware.isService:
        return

    if instance.factor.type in Factor.INPUT_GROUP:
        WareInventory.decrease_inventory(ware, warehouse, instance.count, instance.financial_year, revert=True)
    else:
        ware = instance.ware
        if ware.pricingType == Ware.FIFO:
            for fee in instance.fees:
                WareInventory.increase_inventory(ware, warehouse, fee['count'], fee['fee'], instance.financial_year,
                                                 revert=True)
