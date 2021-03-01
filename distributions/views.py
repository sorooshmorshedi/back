from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from distributions.models import CommissionRange, Visitor
from distributions.models.car_model import Car
from distributions.models.distribution_model import Distribution
from distributions.models.distributor_model import Distributor
from distributions.models.driver_model import Driver
from distributions.models.path_model import Path
from distributions.serializers.car_serializers import CarListRetrieveSerializer, CarCreateUpdateSerializer
from distributions.serializers.commission_range_serializers import CommissionRangeCreateUpdateSerializer, \
    CommissionRangeListRetrieveSerializer
from distributions.serializers.distribution_serializers import DistributionListRetrieveSerializer, \
    DistributionCreateUpdateSerializer
from distributions.serializers.distributor_serializers import DistributorListRetrieveSerializer, \
    DistributorCreateUpdateSerializer
from distributions.serializers.driver_serializers import DriverListRetrieveSerializer, DriverCreateUpdateSerializer
from distributions.serializers.path_serializers import PathListRetrieveSerializer, PathCreateUpdateSerializer
from distributions.serializers.visitor_serializers import VisitorCreateUpdateSerializer, VisitorListRetrieveSerializer
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_new_code


class CommissionRangeModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'commissionRange'
    serializer_class = CommissionRangeListRetrieveSerializer

    def get_queryset(self):
        return CommissionRange.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = CommissionRangeCreateUpdateSerializer(instance=self.get_object(), data=data['item'])
        serializer.is_valid(raise_exception=True)

        instance = serializer.instance
        instance.sync(data['items'])

        return Response(CommissionRangeListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = CommissionRangeCreateUpdateSerializer(data=data['item'])
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=request.user.active_financial_year
        )

        instance = serializer.instance
        instance.sync(data['items'])

        return Response(CommissionRangeListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)


class VisitorModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'visitor'
    serializer_class = VisitorListRetrieveSerializer

    def get_queryset(self):
        return Visitor.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = VisitorCreateUpdateSerializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance

        return Response(VisitorListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = VisitorCreateUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        level = data['level']
        if level == 0:
            code = Visitor.get_new_code()
        else:
            parent = get_object_or_404(Visitor, pk=data.get('parent'))
            code = parent.get_new_child_code()

        serializer.save(
            financial_year=request.user.active_financial_year,
            code=code
        )

        return Response(
            VisitorListRetrieveSerializer(instance=serializer.instance).data,
            status=status.HTTP_200_OK
        )


class PathModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'path'
    serializer_class = PathListRetrieveSerializer

    def get_queryset(self):
        return Path.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = PathCreateUpdateSerializer(
            instance=self.get_object(),
            data=data,
            context={"visitors": data.get('visitors', [])}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance

        return Response(PathListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = PathCreateUpdateSerializer(
            data=data,
            context={"visitors": data.get('visitors', [])}
        )
        serializer.is_valid(raise_exception=True)

        level = data['level']
        if level == 0:
            code = Path.get_new_code()
        else:
            parent = get_object_or_404(Path, pk=data.get('parent'))
            code = parent.get_new_child_code()

        serializer.save(
            financial_year=request.user.active_financial_year,
            code=code
        )

        instance = serializer.instance

        return Response(
            PathListRetrieveSerializer(instance=instance).data,
            status=status.HTTP_200_OK
        )


class DriverModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'driver'
    serializer_class = DriverListRetrieveSerializer

    def get_queryset(self):
        return Driver.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = DriverCreateUpdateSerializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance

        return Response(DriverListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = DriverCreateUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            financial_year=request.user.active_financial_year,
        )

        return Response(
            DriverListRetrieveSerializer(instance=serializer.instance).data,
            status=status.HTTP_200_OK
        )


class DistributorModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'distributor'
    serializer_class = DistributorListRetrieveSerializer

    def get_queryset(self):
        return Distributor.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = DistributorCreateUpdateSerializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance

        return Response(DistributorListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = DistributorCreateUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            financial_year=request.user.active_financial_year,
        )

        return Response(
            DistributorListRetrieveSerializer(instance=serializer.instance).data,
            status=status.HTTP_200_OK
        )


class CarModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'car'
    serializer_class = CarListRetrieveSerializer

    def get_queryset(self):
        return Car.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = CarCreateUpdateSerializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance

        return Response(CarListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = CarCreateUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            financial_year=request.user.active_financial_year,
        )

        return Response(
            CarListRetrieveSerializer(instance=serializer.instance).data,
            status=status.HTTP_200_OK
        )


class DistributionModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'distribution'
    serializer_class = DistributionListRetrieveSerializer

    def get_queryset(self):
        return Distribution.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = DistributionCreateUpdateSerializer(
            instance=self.get_object(),
            data=data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance

        return Response(DistributionListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = DistributionCreateUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            financial_year=request.user.active_financial_year,
            code=get_new_code(Distribution)
        )

        instance = serializer.instance

        return Response(
            DistributionListRetrieveSerializer(instance=instance).data,
            status=status.HTTP_200_OK
        )
