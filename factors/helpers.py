from django.db.models import Sum

from factors.models import FactorItem, Factor


def getInventoryCount(user, warehouse, ware):
    qs = FactorItem.objects.inFinancialYear(user).filter(warehouse=warehouse, ware=ware)
    input_count = qs.filter(factor__type__in=(Factor.FIRST_PERIOD_INVENTORY,
                                              Factor.BUY,
                                              Factor.BACK_FROM_SALE)).aggregate(Sum('count'))['count__sum']
    if not input_count:
        input_count = 0
    output_count = qs.filter(factor__type__in=(Factor.SALE,
                                               Factor.BACK_FROM_BUY)).aggregate(Sum('count'))['count__sum']
    if not output_count:
        output_count = 0
    # print(input_count, output_count)
    return input_count - output_count
