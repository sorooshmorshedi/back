import django_filters
from django_filters import rest_framework as filters
from factors.models.factor import FactorItem
from django_jalali.db import models as jmodels

from helpers.filters import BASE_FIELD_FILTERS
from wares.models import Ware


class InventoryFilter(filters.FilterSet):
    class Meta:
        model = FactorItem
        fields = {
            'ware': ['exact'],
            'ware__code': ['gte', 'lte'],
            'ware__name': BASE_FIELD_FILTERS,

            'warehouse': ['exact'],
            'warehouse__name': ['icontains'],

            'factor__code': ['exact'],
            'factor__date': ['gte', 'lte'],
            'factor__type': ['exact'],
            'factor__explanation': ['icontains'],

            'factor__account__name': ['exact', 'icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class AllWaresInventoryFilter(filters.FilterSet):
    class Meta:
        model = Ware
        fields = {
            'id': BASE_FIELD_FILTERS,
            'code': BASE_FIELD_FILTERS,
            'name': BASE_FIELD_FILTERS,
            'level': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }
