from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from factors.helpers import getInventoryCount
from helpers.views import ListCreateAPIViewWithAutoFinancialYear, RetrieveUpdateDestroyAPIViewWithAutoFinancialYear
from wares.models import *
from wares.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class WarehouseListCreate(ListCreateAPIViewWithAutoFinancialYear):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    serializer_class = WarehouseSerializer


class WarehouseDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    serializer_class = WarehouseSerializer


class UnitDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    serializer_class = UnitSerializer


class UnitListCreate(ListCreateAPIViewWithAutoFinancialYear):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    serializer_class = UnitSerializer


class WareListCreate(ListCreateAPIViewWithAutoFinancialYear):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    serializer_class = WareSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = WareListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)


class WareDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    serializer_class = WareSerializer

    def retrieve(self, request, **kwargs):
        ware = self.get_object()
        serializer = WareListRetrieveSerializer(ware)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        ware = self.get_object()
        if not ware.has_factorItem():
            return super().destroy(self, request, *args, **kwargs)

        return Response(['کالا های دارای گردش در سال مالی جاری غیر قابل حذف می باشند'],
                        status=status.HTTP_400_BAD_REQUEST)


class WareLevelDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    serializer_class = WareLevelSerializer


class WareLevelListCreate(ListCreateAPIViewWithAutoFinancialYear):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    serializer_class = WareLevelSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset().filter(level=0)
        serializer = WareLevelSerializer(queryset, many=True)
        return Response(serializer.data)


class WarehouseInventoryView(APIView):
    def post(self, request):
        res = []
        data = request.data
        for o in data:
            if 'warehouse' not in o or 'ware' not in o:
                return Response(['لطفا کالا و انبار را انتخاب کنید'], status.HTTP_400_BAD_REQUEST)
            warehouse = o['warehouse']
            ware = o['ware']

            res.append({
                'ware': ware,
                'warehouse': warehouse,
                'count': getInventoryCount(warehouse, ware)
            })

        return Response(res, status.HTTP_200_OK)
