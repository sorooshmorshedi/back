from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from accounts.costCenter.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class CostCenterListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, AccountListCreate,)
    queryset = CostCenter.objects.all()
    serializer_class = CostCenterSerializer


class CostCenterDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, AccountListDetail,)
    queryset = CostCenter.objects.all()
    serializer_class = CostCenterSerializer


class CostCenterGroupListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, AccountListCreate,)
    queryset = CostCenterGroup.objects.all()
    serializer_class = CostCenterGroupSerializer


class CostCenterGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, AccountListDetail,)
    queryset = CostCenterGroup.objects.all()
    serializer_class = CostCenterGroupSerializer
