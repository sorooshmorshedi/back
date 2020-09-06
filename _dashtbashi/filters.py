import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from _dashtbashi.models import LadingBillSeries, Remittance, Lading
from helpers.filters import BASE_FIELD_FILTERS


class LadingFilter(filters.FilterSet):
    class Meta:
        model = Lading
        fields = {
            'driving': ['exact'],
            'remittance': ['exact'],
            'is_paid': ['exact'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class LadingBillSeriesFilter(filters.FilterSet):
    class Meta:
        model = LadingBillSeries
        fields = {
            'id': BASE_FIELD_FILTERS,
            'serial': BASE_FIELD_FILTERS,
            'from_bill_number': BASE_FIELD_FILTERS,
            'to_bill_number': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class RemittanceFilter(filters.FilterSet):
    class Meta:
        model = Remittance
        fields = {
            'id': BASE_FIELD_FILTERS,
            'code': BASE_FIELD_FILTERS,
            'issue_date': BASE_FIELD_FILTERS,
            'amount': BASE_FIELD_FILTERS,
            'origin__name': ['exact', 'icontains'],
            'destination__name': ['exact', 'icontains'],
            'contractor__name': ['exact', 'icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }
