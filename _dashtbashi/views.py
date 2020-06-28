from typing import Type

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from _dashtbashi.models import Driver, Car, Driving, AssociationCommission, Remittance, Lading
from _dashtbashi.serializers import DriverSerializer, CarSerializer, DrivingCreateUpdateSerializer, \
    DrivingListRetrieveSerializer, AssociationCommissionSerializer, RemittanceListRetrieveSerializer, \
    RemittanceCreateUpdateSerializer, LadingListRetrieveSerializer, LadingCreateUpdateSerializer
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_new_code, get_object_by_code


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


class AssociationCommissionModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'associationCommission'
    queryset = AssociationCommission.objects.all()
    serializer_class = AssociationCommissionSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year
        )


class RemittanceModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_base_codename = 'remittance'
    queryset = Remittance.objects.all()

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
