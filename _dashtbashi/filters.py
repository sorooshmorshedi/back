import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from _dashtbashi.models import LadingBillSeries


class LadingBillSeriesFilter(filters.FilterSet):
    class Meta:
        model = LadingBillSeries
        fields = {
            'serial': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.DateFilter,
            },
        }
