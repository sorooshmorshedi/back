import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels
from sanads.sanads.models import SanadItem


class SanadItemJounalFilter(filters.FilterSet):
    class Meta:
        model = SanadItem
        fields = {
            'account__code': ['startswith', 'gte', 'lte'],
            'account__name': ['icontains'],

            'sanad__date': ['range'],
            'sanad__code': ['range', 'in'],

            'explanation': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.DateFilter,
            },
        }
