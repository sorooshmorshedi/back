import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels
from distributions.models.distribution_model import Distribution
from helpers.filters import BASE_FIELD_FILTERS


class DistributionFilter(filters.FilterSet):
    class Meta:
        model = Distribution
        fields = {
            'id': ['exact'],
            'local_id': ['exact'],
            'code': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
            'time': BASE_FIELD_FILTERS,
            'car': ['exact'],
            'explanation': ['icontains'],
            'created_by': ['exact'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }
