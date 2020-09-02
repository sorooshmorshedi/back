from django.db.models import Q, Count
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from cheques.views import get_cheque_permission_basename
from factors.serializers import TransferListRetrieveSerializer, AdjustmentListRetrieveSerializer
from factors.views.factorViews import get_factor_permission_basename
from helpers.auth import BasicCRUDPermission
from reports.lists.filters import *
from reports.lists.serializers import *
from transactions.models import Transaction
from transactions.views import get_transaction_permission_basename


class TransactionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_codename(self):
        return "get.{}".format(get_transaction_permission_basename(self.request.GET.get('type')))

    serializer_class = TransactionListSerializer
    filterset_class = TransactionFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Transaction.objects.hasAccess('get').all()


class ChequeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_codename(self):
        received_or_paid = self.request.GET.get('received_or_paid')
        return "get.{}".format(get_cheque_permission_basename(received_or_paid))

    serializer_class = ChequeListSerializer
    filterset_class = ChequeFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Cheque.objects.hasAccess('get').all()


class ChequebookListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = "get.chequebook"
    serializer_class = ChequebookListSerializer
    filterset_class = ChequebookFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Chequebook.objects.hasAccess('get').all()


class SanadListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = "get.sanad"

    serializer_class = SanadSerializer

    pagination_class = LimitOffsetPagination

    ordering_fields = '__all__'
    filterset_class = SanadFilter
    search_fields = SanadFilter.Meta.fields.keys()

    def get_queryset(self):
        return Sanad.objects.hasAccess('get').order_by('code').all()


class UnbalancedSanadListView(SanadListView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = "get.sanad"

    def get_queryset(self):
        return Sanad.objects.hasAccess('get').order_by('code').filter(~Q(bed=F('bes')))


class EmptySanadListView(SanadListView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = "get.sanad"

    def get_queryset(self):
        return Sanad.objects.hasAccess('get').annotate(items_count=Count('items')).filter(items_count=0).order_by(
            'code')


class FactorListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_codename(self):
        return "get.{}".format(get_factor_permission_basename(self.request.GET.get('type')))

    serializer_class = FactorListCreateUpdateSerializer
    filterset_class = FactorFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Factor.objects.hasAccess('get').prefetch_related('items').prefetch_related('account').all()


class TransferListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = "get.transfer"
    serializer_class = TransferListRetrieveSerializer
    filterset_class = TransferFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Transfer.objects.hasAccess('get').all()


class FactorItemListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_codename(self):
        return "get.{}".format(get_factor_permission_basename(self.request.GET.get('type')))

    serializer_class = FactorItemListSerializer
    filterset_class = FactorItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return FactorItem.objects.hasAccess('get') \
            .prefetch_related('factor__account') \
            .prefetch_related('ware') \
            .prefetch_related('warehouse') \
            .all()


class AdjustmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = "get.adjustment"
    serializer_class = AdjustmentListRetrieveSerializer
    filterset_class = AdjustmentFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Adjustment.objects.hasAccess('get').all()
