from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.costCenters.serializers import *
from helpers.auth import BasicCRUDPermission


@method_decorator(csrf_exempt, name='dispatch')
class CostCenterListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    queryset = CostCenter.objects.all()
    serializer_class = CostCenterSerializer


class CostCenterDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    queryset = CostCenter.objects.all()
    serializer_class = CostCenterSerializer


class CostCenterGroupListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    queryset = CostCenterGroup.objects.all()
    serializer_class = CostCenterGroupSerializer


class CostCenterGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    queryset = CostCenterGroup.objects.all()
    serializer_class = CostCenterGroupSerializer
