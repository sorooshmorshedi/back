from typing import Type

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer

from _dashtbashi.models import Driver, Car, Driving
from _dashtbashi.serializers import DriverSerializer, CarSerializer, DrivingCreateUpdateSerializer, \
    DrivingListRetrieveSerializer
from helpers.auth import BasicCRUDPermission


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
