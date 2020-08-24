import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from _dashtbashi.models import LadingBillSeries, Remittance, Lading


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
            'serial': ['icontains'],
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
            'code': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }
