from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from wares.models import *
from wares.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class WareHouseListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, WareListCreate,)
    queryset = WareHouse.objects.all()
    serializer_class = WareHouseSerializer


class WareHouseDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, WareListDetail,)
    queryset = WareHouse.objects.all()
    serializer_class = WareHouseSerializer


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


