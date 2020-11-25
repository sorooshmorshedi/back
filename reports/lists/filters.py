import django_filters
from django.db.models import F
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from cheques.models.ChequeModel import Cheque
from cheques.models.ChequebookModel import Chequebook
from factors.models import Factor, FactorItem, Transfer, Adjustment, WarehouseHandling
from helpers.filters import BASE_FIELD_FILTERS
from sanads.models import Sanad
from transactions.models import Transaction


class TransactionFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'id': ['exact'],
            'code': ['icontains'],
            'account__name': ['exact', 'icontains'],
            'sanad__bed': ['icontains'],
            'date': ['gte', 'lte'],
            'explanation': ['icontains'],
            'type': ['exact'],
            'sanad__bed': BASE_FIELD_FILTERS
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ChequeFilter(filters.FilterSet):
    class Meta:
        model = Cheque
        fields = {
            'id': ['exact'],
            'serial': ['icontains'],
            'explanation': ['icontains'],
            'date': ['gte', 'lte'],
            'due': BASE_FIELD_FILTERS,
            'value': ['exact'],
            'status': BASE_FIELD_FILTERS,
            'bankName': ['icontains'],
            'type': ['exact'],
            'received_or_paid': ['exact'],
            'chequebook__id': ['exact'],
            'chequebook__explanation': ['icontains'],
            'chequebook__account__name': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ChequebookFilter(filters.FilterSet):
    class Meta:
        model = Chequebook
        fields = {
            'id': ['exact'],
            'account__name': ['icontains'],
            'serial': ['icontains'],
            'serial_from': ['icontains'],
            'serial_to': ['icontains'],
            'explanation': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class SanadFilter(filters.FilterSet):
    class Meta:
        model = Sanad
        fields = {
            'id': ['exact', 'in'],
            'local_id': ['exact', 'in'],
            'code': BASE_FIELD_FILTERS,
            'bed': BASE_FIELD_FILTERS,
            'bes': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
            'is_auto_created': ['exact'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class FactorFilter(filters.FilterSet):
    isPaid = filters.BooleanFilter(method='filterIsPaid')

    class Meta:
        model = Factor
        fields = {
            'id': ['exact'],
            'temporary_code': ['icontains'],
            'code': ['icontains'],
            'isPaid': ['exact'],
            'date': ['gte', 'lte'],
            'time': ['gte', 'lte'],
            'account__name': ['icontains'],
            'explanation': ['icontains'],
            'sanad__bed': ['icontains'],
            'type': ['exact', 'in'],
            'is_definite': ['exact']
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }

    def filterIsPaid(self, queryset, name, value):
        if value:
            return queryset.filter(sanad__bed=F('paidValue'))
        else:
            return queryset


class TransferFilter(filters.FilterSet):
    class Meta:
        model = Transfer
        fields = {
            'id': ['exact'],
            # 'code': ['gte', 'lte', 'exact'],
            'date': ['gte', 'lte'],
            'explanation': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class FactorItemFilter(filters.FilterSet):
    class Meta:
        model = FactorItem
        fields = {
            'ware': ['exact'],
            'warehouse': ['exact'],
            'warehouse__name': BASE_FIELD_FILTERS,
            'factor__type': ['exact', 'in'],
            'id': ['exact'],
            'factor__code': BASE_FIELD_FILTERS,
            'factor__is_definite': ['exact'],
            'factor__date': BASE_FIELD_FILTERS,
            'factor__account__name': BASE_FIELD_FILTERS,
            'count': ['exact'],
            'fee': ['exact'],
            'factor__explanation': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class AdjustmentFilter(filters.FilterSet):
    class Meta:
        model = Adjustment
        fields = {
            'id': ['exact'],
            'type': ['exact'],
            'code': ['gte', 'lte', 'exact'],
            'date': ['gte', 'lte'],
            'explanation': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class WarehouseHandlingFilter(filters.FilterSet):
    class Meta:
        model = WarehouseHandling
        fields = {
            'id': BASE_FIELD_FILTERS,
            'code': BASE_FIELD_FILTERS,
            'start_date': BASE_FIELD_FILTERS,
            'counting_date': BASE_FIELD_FILTERS,
            'submit_date': BASE_FIELD_FILTERS,
            'warehouse__name': BASE_FIELD_FILTERS,
            'handler': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }

