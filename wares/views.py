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
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class UnitDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class UnitListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class WareListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    queryset = Ware.objects.all()
    serializer_class = WareSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = Ware.objects.all()
        serializer = WareListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)


class WareDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    queryset = Ware.objects.all()
    serializer_class = WareSerializer

    def retrieve(self, request, pk=None):
        queryset = Ware.objects.all()
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
    queryset = WareLevel.objects.all()
    serializer_class = WareLevelSerializer


class WareLevelListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    queryset = WareLevel.objects.all()
    serializer_class = WareLevelSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = WareLevel.objects.filter(level=0)
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

            res.append(getInventoryCount(warehouse, ware))

        return Response(res, status.HTTP_200_OK)
