import django_filters
from django.db.models import F
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from cheques.models.ChequeModel import Cheque
from cheques.models.ChequebookModel import Chequebook
from factors.models import Factor, FactorItem, Transfer
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
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.DateFilter,
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
            'due': ['gte', 'lte'],
            'value': ['exact'],
            'status': ['exact'],
            'bankName': ['icontains'],
            'type': ['exact'],
            'received_or_paid': ['exact'],
            'chequebook__id': ['exact'],
            'chequebook__explanation': ['icontains'],
            'chequebook__account__name': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.DateFilter,
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
                'filter_class': django_filters.DateFilter,
            },
        }


BASE_FIELD_FILTERS = ('exact', 'in', 'icontains', 'lte', 'gte')


class SanadFilter(filters.FilterSet):
    class Meta:
        model = Sanad
        fields = {
            'id': ['exact', 'in'],
            'code': BASE_FIELD_FILTERS,
            'bed': BASE_FIELD_FILTERS,
            'bes': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
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
                'filter_class': django_filters.DateFilter,
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
                'filter_class': django_filters.DateFilter,
            },
        }


class FactorItemFilter(filters.FilterSet):
    class Meta:
        model = FactorItem
        fields = {
            'ware': ['exact'],
            'warehouse': ['exact'],
            'factor__type': ['exact', 'in'],
            'id': ['exact'],
            'factor__code': ['exact'],
            'factor__is_definite': ['exact'],
            'factor__date': ['gte', 'lte'],
            'factor__account__name': ['icontains'],
            'warehouse__name': ['icontains'],
            'count': ['exact'],
            'fee': ['exact'],
            'factor__explanation': ['icontains'],
            'explanation': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.DateFilter,
            },
        }
