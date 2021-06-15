from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.functions.comparison import Coalesce
from django.db.models.query_utils import Q
from typing import List
from django.db.models import Model
from django.db.models.fields.reverse_related import (
    ManyToOneRel,
    ForeignObjectRel,
)


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


def get_all_relations(model: Model) -> List[ForeignObjectRel]:
    """
    Return all Many to One Relation to point to the given model
    """
    result: List[ForeignObjectRel] = []
    for field in model._meta.get_fields(include_hidden=True):
        if isinstance(field, ManyToOneRel):
            result.append(field)
    return result


def delete_object_recursively(obj: Model, d=0):
    for field in get_all_relations(obj):
        field: ManyToOneRel

        if field.on_delete == models.CASCADE or field.on_delete == models.PROTECT:
            target_model: Model = field.related_model
            target_field: str = field.remote_field.name

            print('- ' * d, target_field, ':')

            related_objs = target_model.objects.filter(
                **{target_field: obj}
            )
            for related_obj in related_objs:
                delete_object_recursively(related_obj, d=d + 1)

    obj.delete()
