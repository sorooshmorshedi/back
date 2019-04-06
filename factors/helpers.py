from django.db.models import Sum

from factors.models import FactorItem


def getInventoryCount(warehouse, ware):
    qs = FactorItem.objects.filter(warehouse=warehouse, ware=ware)
    input_count = qs.filter(factor__type__in=('buy', 'backFromSale')).aggregate(Sum('count'))['count__sum']
    if not input_count:
        input_count = 0
    output_count = qs.filter(factor__type__in=('sale', 'backFromBuy')).aggregate(Sum('count'))['count__sum']
    if not output_count:
        output_count = 0
    # print(input_count, output_count)
    return input_count - output_count
