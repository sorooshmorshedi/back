from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from _dashtbashi.filters import RemittanceFilter, LadingBillSeriesFilter, LadingFilter, OilCompanyLadingFilter, \
    OilCompanyLadingItemFilter
from _dashtbashi.models import Remittance, Lading, LadingBillSeries, OilCompanyLading, OilCompanyLadingItem, Car
from _dashtbashi.serializers import RemittanceListRetrieveSerializer, LadingListSerializer, \
    LadingBillSeriesSerializer, OilCompanyLadingListRetrieveSerializer, OilCompanyLadingItemCreateUpdateSerializer, \
    OilCompanyLadingItemListRetrieveSerializer
from helpers.auth import BasicCRUDPermission
from helpers.querysets import add_sum
from transactions.models import Transaction
from transactions.serializers import TransactionListRetrieveSerializer


class OtherDriverPaymentReport(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'otherDriverPayment'

    def get(self, request):
        data = request.GET
        remittance = get_object_or_404(Remittance.objects.hasAccess('get'), pk=data.get('remittance'))

        ladings = Lading.objects.hasAccess('get', 'lading').filter(
            remittance=remittance,
            driving__car__owner=Car.OTHER
        )

        imprest_accounts = [lading.driving.car.payableAccount for lading in ladings]

        imprests = Transaction.get_not_settled_imprests_queryset().filter(account__in=imprest_accounts)

        return Response({
            'ladings': LadingListSerializer(ladings, many=True).data,
            'imprests': TransactionListRetrieveSerializer(imprests, many=True).data,
        })


class RemittanceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.remittance'

    serializer_class = RemittanceListRetrieveSerializer

    pagination_class = LimitOffsetPagination
    filterset_class = RemittanceFilter
    ordering_fields = '__all__'

    def get_queryset(self):
        qs = Remittance.objects.hasAccess('get').all()
        qs = self.filter_queryset(queryset=qs)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            response = self.get_paginated_response(data)
        else:
            response = Response({})

        sum_fields = [
            'contractor_price',
            'driver_tip_price',
            'lading_bill_difference',
            'fare_price',
            'amount'
        ]
        add_sum(response, sum_fields, queryset, page)

        return response


class LadingBillSeriesListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.ladingBillSeries'

    serializer_class = LadingBillSeriesSerializer

    pagination_class = LimitOffsetPagination
    filterset_class = LadingBillSeriesFilter
    ordering_fields = '__all__'

    def get_queryset(self):
        return LadingBillSeries.objects.hasAccess('get').all()


class LadingListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.lading'

    serializer_class = LadingListSerializer

    pagination_class = LimitOffsetPagination
    filterset_class = LadingFilter
    ordering_fields = '__all__'

    def get_queryset(self):

        ordering = self.request.GET.get('ordering')
        qs = Lading.objects.hasAccess('get')
        if ordering:
            qs = qs.order_by(ordering)

        return self.filter_queryset(qs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            response = self.get_paginated_response(data)
        else:
            response = Response({})

        sum_fields = [
            'contractor_price',
            'fare_price',
            'bill_price',
            'driver_tip_price',
            'lading_bill_difference',
            'origin_amount',
            'destination_amount',
            'cargo_tip_price',
            'association_price'
        ]
        add_sum(response, sum_fields, queryset, page)

        return response


class OilCompanyLadingListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.oilCompanyLading'

    serializer_class = OilCompanyLadingListRetrieveSerializer

    pagination_class = LimitOffsetPagination
    filterset_class = OilCompanyLadingFilter
    ordering_fields = '__all__'

    def get_queryset(self):
        return OilCompanyLading.objects.hasAccess('get').all()


class OilCompanyLadingItemListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.oilCompanyLading'

    serializer_class = OilCompanyLadingItemListRetrieveSerializer

    pagination_class = LimitOffsetPagination
    filterset_class = OilCompanyLadingItemFilter
    ordering_fields = '__all__'

    def get_queryset(self):
        return OilCompanyLadingItem.objects.hasAccess('get', 'oilCompanyLading').all()
