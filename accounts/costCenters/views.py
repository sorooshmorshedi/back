from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.costCenters.serializers import *
from helpers.auth import BasicCRUDPermission


@method_decorator(csrf_exempt, name='dispatch')
class CostCenterListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = CostCenterSerializer

    def get_queryset(self):
        return CostCenter.objects.inFinancialYear(self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class CostCenterDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = CostCenterSerializer

    def get_queryset(self):
        return CostCenter.objects.inFinancialYear(self.request.user)


class CostCenterGroupListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = CostCenterGroupSerializer

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return CostCenterGroup.objects.inFinancialYear(self.request.user)


class CostCenterGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = CostCenterGroupSerializer

    def get_queryset(self):
        return CostCenterGroup.objects.inFinancialYear(self.request.user)
