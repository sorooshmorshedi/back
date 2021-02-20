from django.db.models import Sum

from factors.models import Factor
from factors.models.factor import FactorItem


# remain by considering definition
def getInventoryCount(user, warehouse, ware):
    qs = FactorItem.objects.inFinancialYear().filter(warehouse=warehouse, ware=ware)
    input_count = qs.filter(factor__type__in=Factor.INPUT_GROUP,
                            factor__is_definite=True).aggregate(Sum('count'))['count__sum']
    if not input_count:
        input_count = 0
    output_count = qs.filter(factor__type__in=Factor.OUTPUT_GROUP,
                             factor__is_definite=True).aggregate(Sum('count'))['count__sum']
    if not output_count:
        output_count = 0
    return input_count - output_count
