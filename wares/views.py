from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from factors.helpers import getInventoryCount
from wares.models import *
from wares.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class WarehouseListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        return Warehouse.objects.inFinancialYear(self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class WarehouseDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        return Warehouse.objects.inFinancialYear(self.request.user)


class UnitDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    serializer_class = UnitSerializer

    def get_queryset(self):
        return Unit.objects.inFinancialYear(self.request.user)


class UnitListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    serializer_class = UnitSerializer

    def get_queryset(self):
        return Unit.objects.inFinancialYear(self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class WareListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    serializer_class = WareSerializer

    def get_queryset(self):
        return Ware.objects.inFinancialYear(self.request.user)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = WareListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class WareDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    serializer_class = WareSerializer

    def get_queryset(self):
        return Ware.objects.inFinancialYear(self.request.user)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        ware = get_object_or_404(queryset, pk=pk)
        serializer = WareListRetrieveSerializer(ware)
        return Response(serializer.data)

    def destroy(self, request, pk, *args, **kwargs):
        ware = get_object_or_404(Ware, pk=pk)
        if ware.has_factorItem():
            return super().destroy(self, request, *args, **kwargs)

        return Response(['کالا های دارای گردش در سال مالی جاری غیر قابل حذف می باشند'],
                        status=status.HTTP_400_BAD_REQUEST)


class WareLevelDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    serializer_class = WareLevelSerializer

    def get_queryset(self):
        return WareLevel.objects.inFinancialYear(self.request.user)


class WareLevelListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    serializer_class = WareLevelSerializer

    def get_queryset(self):
        return WareLevel.objects.inFinancialYear(self.request.user)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset().filter(level=0)
        serializer = WareLevelSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class WarehouseInventoryView(APIView):
    def post(self, request):
        res = []
        data = request.data
        for o in data:
            if 'warehouse' not in o or 'ware' not in o:
                return Response(['لطفا کالا و انبار را انتخاب کنید'], status.HTTP_400_BAD_REQUEST)
            warehouse = o['warehouse']
            ware = o['ware']

            res.append(getInventoryCount(warehouse, ware))

        return Response(res, status.HTTP_200_OK)
