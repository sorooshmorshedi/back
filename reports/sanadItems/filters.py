import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from helpers.filters import BASE_FIELD_FILTERS
from sanads.models import SanadItem


class SanadItemReportFilter(filters.FilterSet):
    class Meta:
        model = SanadItem
        fields = {
            'account': ['exact', 'in'],
            'account__code': ['startswith'] + BASE_FIELD_FILTERS,
            'account__name': BASE_FIELD_FILTERS,
            'account__floatAccountGroup': ['exact'],
            'account__costCenterGroup': ['exact'],
            'floatAccount': ['exact'],
            'costCenter': ['exact'],

            'floatAccount': ['exact', 'in'],

            'sanad__date': BASE_FIELD_FILTERS,
            'sanad__code': BASE_FIELD_FILTERS,
            'sanad__type': BASE_FIELD_FILTERS,

            'financial_year': ['exact'],
            'financial_year__name': BASE_FIELD_FILTERS,

            'bed': BASE_FIELD_FILTERS,
            'bes': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }
