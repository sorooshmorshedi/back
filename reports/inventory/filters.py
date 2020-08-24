import django_filters
from django_filters import rest_framework as filters
from factors.models import FactorItem
from django_jalali.db import models as jmodels

from wares.models import Ware


class InventoryFilter(filters.FilterSet):
    class Meta:
        model = FactorItem
        fields = {
            'ware': ['exact'],
            'ware__code': ['gte', 'lte'],
            'ware__name': ['icontains'],

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
            'id': ['exact'],
            'code': ['gte', 'lte'],
            'name': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


