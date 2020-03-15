from django.db import connection
from django.db.models import Q, Count
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from factors.models import Transfer
from factors.serializers import TransferListRetrieveSerializer
from reports.lists.filters import *
from reports.lists.serializers import *
from sanads.transactions.models import Transaction


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionListSerializer
    filterset_class = TransactionFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Transaction.objects.inFinancialYear().all()


class ChequeListView(generics.ListAPIView):
    serializer_class = ChequeListSerializer
    filterset_class = ChequeFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Cheque.objects.inFinancialYear().all()


class ChequebookListView(generics.ListAPIView):
    serializer_class = ChequebookListSerializer
    filterset_class = ChequebookFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Chequebook.objects.inFinancialYear().all()


class SanadListView(generics.ListAPIView):
    serializer_class = SanadSerializer
    filterset_class = SanadFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Sanad.objects.inFinancialYear().all()


class UnbalancedSanadListView(SanadListView):
    def get_queryset(self):
        return Sanad.objects.inFinancialYear().filter(~Q(bed=F('bes')))


class EmptySanadListView(SanadListView):
    def get_queryset(self):
        return Sanad.objects.inFinancialYear().annotate(items_count=Count('items')).filter(items_count=0)


class FactorListView(generics.ListAPIView):
    serializer_class = FactorListSerializer
    filterset_class = FactorFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Factor.objects.inFinancialYear().prefetch_related('items').prefetch_related('account').all()


class TransferListView(generics.ListAPIView):
    serializer_class = TransferListRetrieveSerializer
    filterset_class = TransferFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Transfer.objects.inFinancialYear().all()


class FactorItemListView(generics.ListAPIView):
    serializer_class = FactorItemListSerializer
    filterset_class = FactorItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return FactorItem.objects.inFinancialYear()\
            .prefetch_related('factor__account')\
            .prefetch_related('ware') \
            .prefetch_related('warehouse')\
            .all()
