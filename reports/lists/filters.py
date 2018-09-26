import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from cheques.models import Cheque, Chequebook
from factors.models import Factor, Receipt
from sanads.sanads.models import Sanad
from sanads.transactions.models import Transaction


class TransactionFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
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
            'code': ['icontains'],
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
    class Meta:
        model = Factor
        fields = {
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


class ReceiptFilter(filters.FilterSet):
    class Meta:
        model = Receipt
        fields = {
            'code': ['icontains'],
            'date': ['gte', 'lte'],
            'time': ['gte', 'lte'],
            'explanation': ['icontains'],
            'type': ['exact'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.DateFilter,
            },
        }
