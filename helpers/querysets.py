from django.db.models.aggregates import Sum
from django.db.models.functions.comparison import Coalesce


def add_sum(response, sum_fields, qs, page=None):
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
