import django_filters
from django_filters import rest_framework as filters
from factors.models import FactorItem
from django_jalali.db import models as jmodels


class InventoryFilter(filters.FilterSet):
    class Meta:
        model = FactorItem
        fields = {
            'factor__code': ['exact'],
            'factor__date': ['gte', 'lte'],
            'factor__type': ['exact'],
            'factor__explanation': ['icontains'],
            'factor__account__name': ['exact', 'icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.DateFilter,
            },
        }


class WarehouseInventoryFilter(filters.FilterSet):
    class Meta:
        model = FactorItem
        fields = {
            'ware__code': ['gte', 'lte'],
            'ware__name': ['icontains'],
            'warehouse__name': ['icontains'],
            'warehouse': ['exact']
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.DateFilter,
            },
        }
