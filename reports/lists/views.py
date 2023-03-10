from django.db.models import Q, Count
from django.db.models.query import Prefetch
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from cheques.views import get_cheque_permission_basename
from contracting.serializers import TenderSerializer, ContractSerializer, StatementSerializer, SupplementSerializer
from factors.models.warehouse_handling import WarehouseHandlingItem
from factors.serializers import TransferListRetrieveSerializer, AdjustmentListRetrieveSerializer, \
    WarehouseHandlingListRetrieveSerializer, FactorsAggregatedSanadListSerializer
from factors.models.factor import get_factor_permission_basename, FactorsAggregatedSanad
from helpers.auth import BasicCRUDPermission
from reports.lists.filters import *
from reports.lists.serializers import *
from transactions.models import Transaction
from transactions.views import get_transaction_permission_basename
from wares.models import WareSalePriceChange


class TransactionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_basename(self):
        return get_transaction_permission_basename(self.request.GET.get('type'))

    serializer_class = TransactionListSerializer
    filterset_class = TransactionFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Transaction.objects.hasAccess('get', self.permission_basename).all()


class ChequeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_basename(self):
        return get_cheque_permission_basename(self.request.GET.get('is_paid', False) == 'true')

    serializer_class = ChequeListSerializer
    filterset_class = ChequeFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Cheque.objects.hasAccess('get', self.permission_basename).all()


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

    serializer_class = SanadListSerializer

    pagination_class = LimitOffsetPagination

    ordering_fields = '__all__'
    filterset_class = SanadFilter
    search_fields = SanadFilter.Meta.fields.keys()

    def get_queryset(self):
        return Sanad.objects.hasAccess('get').order_by('-pk').all()


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
        return "get.{}".format(get_factor_permission_basename(self.type))

    @property
    def type(self):
        return self.request.GET.get('type')

    @property
    def is_pre_factor(self):
        return self.request.GET.get('is_pre_factor') == 'true'

    serializer_class = FactorListCreateUpdateSerializer
    filterset_class = FactorFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Factor.objects.hasAccess(
            'get',
            permission_basename=get_factor_permission_basename(self.type)
        ).prefetch_related('items').prefetch_related('account').all()


class FactorsAggregatedSanadListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_basename(self):
        return "{}sAggregatedSanad".format(get_factor_permission_basename(self.type))

    @property
    def type(self):
        return self.request.GET.get('type')

    serializer_class = FactorsAggregatedSanadListSerializer
    filterset_class = FactorsAggregatedSanadFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return FactorsAggregatedSanad.objects.hasAccess(
            'get',
            permission_basename=self.permission_basename
        ).all()


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
    def permission_basename(self):
        return get_factor_permission_basename(self.request.GET.get('type'))

    serializer_class = FactorItemListSerializer
    filterset_class = FactorItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return FactorItem.objects.hasAccess('get', self.permission_basename) \
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


class WarehouseHandlingListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = "get.warehouseHandling"
    serializer_class = WarehouseHandlingListRetrieveSerializer
    filterset_class = WarehouseHandlingFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return WarehouseHandling.objects.hasAccess('get').prefetch_related(
            Prefetch('items', WarehouseHandlingItem.objects.order_by('order'))
        ).all()


class SalePriceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.salePrice"
    serializer_class = SalePriceListSerializer
    filterset_class = SalePriceFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return SalePrice.objects.hasAccess('get').all()


class SalePriceChangeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.salePriceChange"
    serializer_class = SalePriceChangeListSerializer
    filterset_class = SalePriceChangeFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return SalePriceChange.objects.hasAccess('get').all()


class WareSalePriceChangeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.salePriceChange"
    serializer_class = WareSalePriceChangeListSerializer
    filterset_class = WareSalePriceChangeFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return WareSalePriceChange.objects.hasAccess('get', self.permission_codename).all()


class TenderListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.tender"
    serializer_class = TenderSerializer
    filterset_class = TenderFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Tender.objects.hasAccess('get', self.permission_codename).all()


class ContractListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.contract"
    serializer_class = ContractSerializer
    filterset_class = ContractFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Contract.objects.hasAccess('get', self.permission_codename).all()


class StatementListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.statement"
    serializer_class = StatementSerializer
    filterset_class = StatementFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Statement.objects.hasAccess('get', self.permission_codename).all()


class SupplementListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.supplement"
    serializer_class = SupplementSerializer
    filterset_class = SupplementFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Supplement.objects.hasAccess('get', self.permission_codename).all()
