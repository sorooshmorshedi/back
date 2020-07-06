from typing import Type, Any

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from _dashtbashi.filters import LadingBillSeriesFilter, RemittanceFilter
from _dashtbashi.models import Driver, Car, Driving, Association, Remittance, Lading, LadingBillSeries, \
    LadingBillNumber, OilCompanyLading
from _dashtbashi.serializers import DriverSerializer, CarSerializer, DrivingCreateUpdateSerializer, \
    DrivingListRetrieveSerializer, AssociationSerializer, RemittanceListRetrieveSerializer, \
    RemittanceCreateUpdateSerializer, LadingListRetrieveSerializer, LadingCreateUpdateSerializer, \
    LadingBillSeriesSerializer, OilCompanyLadingCreateUpdateSerializer, OilCompanyLadingItemSerializer, \
    OilCompanyLadingListRetrieveSerializer
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_new_code, get_object_by_code
from helpers.views.MassRelatedCUD import MassRelatedCUD


class DriverModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'driver'
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year
        )


class CarModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'car'
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year
        )


class DrivingModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'driving'
    queryset = Driving.objects.all()

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.request.method.lower() == 'get':
            return DrivingListRetrieveSerializer
        return DrivingCreateUpdateSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year
        )


class AssociationModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'association'
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year
        )


class LadingBillSeriesModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'ladingBillSeries'
    queryset = LadingBillSeries.objects.all()
    serializer_class = LadingBillSeriesSerializer
    filterset_class = LadingBillSeriesFilter
    pagination_class = LimitOffsetPagination
    page_size = 15

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        print(page)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LadingBillSeriesByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'ladingBillSeries'

    def get(self, request):
        item = get_object_by_code(
            LadingBillSeries.objects.all(),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(LadingBillSeriesSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class RemittanceModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'remittance'
    queryset = Remittance.objects.all()
    filterset_class = RemittanceFilter
    pagination_class = LimitOffsetPagination
    page_size = 15

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.request.method.lower() == 'get':
            return RemittanceListRetrieveSerializer
        return RemittanceCreateUpdateSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year,
        )


class RemittanceByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'remittance'

    def get(self, request):
        remittance = get_object_by_code(
            Remittance.objects.inFinancialYear(),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if remittance:
            return Response(RemittanceListRetrieveSerializer(instance=remittance).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class RemittanceByCodeView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'remittance'

    def get(self, request):
        remittance = get_object_or_404(Remittance, code=request.GET.get('code'))
        return Response(RemittanceListRetrieveSerializer(instance=remittance).data)


class LadingModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'lading'
    queryset = Lading.objects.all()

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.request.method.lower() == 'get':
            return LadingListRetrieveSerializer
        return LadingCreateUpdateSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year,
        )


class LadingByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'lading'

    def get(self, request):
        lading = get_object_by_code(
            Lading.objects.inFinancialYear(),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if lading:
            return Response(LadingListRetrieveSerializer(instance=lading).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class RevokeLadingBillNumber(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_codename = 'revoke.ladingBillNumber'

    def post(self, request):
        ladingBillNumber = get_object_or_404(LadingBillNumber, pk=request.data.get('id'))
        ladingBillNumber.is_revoked = request.data.get('is_revoked')
        ladingBillNumber.save()
        return Response()


class OilCompanyLadingModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'oilCompanyLading'
    serializer_class = OilCompanyLadingCreateUpdateSerializer

    def get_queryset(self) -> QuerySet:
        return OilCompanyLading.objects.inFinancialYear()

    # def retrieve(self, request, pk=None, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     instance = get_object_or_404(queryset, pk=pk)
    #     serialized = (instance)
    #     return Response(serialized.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        form_data = data['form']
        items_data = data['items']

        serializer = OilCompanyLadingCreateUpdateSerializer(data=form_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
        )

        instance = serializer.instance
        MassRelatedCUD(
            user,
            items_data.get('items'),
            items_data.get('ids_to_delete'),
            'oilCompanyLading',
            serializer.instance.id,
            OilCompanyLadingItemSerializer,
            OilCompanyLadingItemSerializer,
        ).sync()

        return Response(OilCompanyLadingListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        user = request.user
        form_data = request.data['form']
        items_data = request.data['items']

        serialized = self.serializer_class(instance=instance, data=form_data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        MassRelatedCUD(
            user,
            items_data.get('items'),
            items_data.get('ids_to_delete'),
            'oilCompanyLading',
            instance.id,
            OilCompanyLadingItemSerializer,
            OilCompanyLadingItemSerializer,
        ).sync()

        return Response(OilCompanyLadingListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)


class OilCompanyLadingByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'oilCompanyLading'

    def get(self, request):
        item = get_object_by_code(
            OilCompanyLading.objects.all(),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(OilCompanyLadingListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)
