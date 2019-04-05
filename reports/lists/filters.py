import django_filters
from django.db.models import F
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from cheques.models import Cheque, Chequebook
from factors.models import Factor
from sanads.sanads.models import Sanad
from sanads.transactions.models import Transaction


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
            'code': ['icontains'],
            'serial_from': ['icontains'],
            'serial_to': ['icontains'],
            'explanation': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.DateFilter,
            },
        }


class SanadFilter(filters.FilterSet):
    class Meta:
        model = Sanad
        fields = {
            'id': ['exact'],
            'code': ['exact', 'icontains'],
            'bed': ['icontains'],
            'bes': ['icontains'],
            'explanation': ['icontains'],
            'date': ['gte', 'lte'],
            'type': ['exact'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.DateFilter,
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

