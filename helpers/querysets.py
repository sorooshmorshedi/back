from django.db.models.aggregates import Sum
from django.db.models.functions.comparison import Coalesce
from django.db.models.query_utils import Q


def add_sum(response, sum_fields, qs, page=None):
    """
        Adds sum of fields in sum_fields to `response.data[sum_field]`
        Can add page_sum too
        runs one query with qs for sum and calculate page sum in python
    """

    aggregates = {}
    for field in sum_fields:
        aggregates[field] = Coalesce(Sum(field), 0)
    response.data['sum'] = qs.aggregate(**aggregates)

    if page:
        page_sum = {}
        for field in sum_fields:
            page_sum[field] = 0
            for item in page:
                page_sum[field] += getattr(item, field)
        response.data['page_sum'] = page_sum


def get_deep_sum(field, filters, related_name='children', depth=4):
    """
        Ex: sum of bed for each level of account tree
    """

    if depth == 1:
        next_depth = 0
    else:
        next_filters = {}
        for key in filters.keys():
            next_filters["{}__{}".format(related_name, key)] = filters[key]

        next_depth = get_deep_sum("{}__{}".format(related_name, field), next_filters, related_name, depth - 1)

    return Coalesce(
        Sum(field, filter=Q(**filters)),
        next_depth
    )


