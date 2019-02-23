from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from factors.serializers import ReceiptSerializer
from reports.lists.filters import *
from reports.lists.serializers import *
from sanads.transactions.models import Transaction


class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer
    filterset_class = TransactionFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination


class ChequeListView(generics.ListAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeListSerializer
    filterset_class = ChequeFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination


class ChequebookListView(generics.ListAPIView):
    queryset = Chequebook.objects.all()
    serializer_class = ChequebookListSerializer
    filterset_class = ChequebookFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination


class SanadListView(generics.ListAPIView):
    queryset = Sanad.objects.all()
    serializer_class = SanadSerializer
    filterset_class = SanadFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination


class FactorListView(generics.ListAPIView):
    queryset = Factor.objects.all()
    serializer_class = FactorListSerializer
    filterset_class = FactorFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination


class ReceiptListView(generics.ListAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    filterset_class = ReceiptFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination
