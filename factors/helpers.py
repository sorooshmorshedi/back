from django.db.models import Sum

from factors.models import FactorItem, Factor


def getInventoryCount(user, warehouse, ware):
    qs = FactorItem.objects.inFinancialYear(user).filter(warehouse=warehouse, ware=ware)
    input_count = qs.filter(factor__type__in=Factor.BUY_GROUP, factor__is_definite=True).aggregate(Sum('count'))['count__sum']
    if not input_count:
        input_count = 0
    output_count = qs.filter(factor__type__in=Factor.SALE_GROUP).aggregate(Sum('count'))['count__sum']
    if not output_count:
        output_count = 0
    return input_count - output_count
