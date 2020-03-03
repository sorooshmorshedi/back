from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated

from accounts.costCenters.serializers import *
from helpers.auth import BasicCRUDPermission
from helpers.views.RetrieveUpdateDestroyAPIViewWithAutoFinancialYear import RetrieveUpdateDestroyAPIViewWithAutoFinancialYear
from helpers.views.ListCreateAPIViewWithAutoFinancialYear import ListCreateAPIViewWithAutoFinancialYear


@method_decorator(csrf_exempt, name='dispatch')
class CostCenterListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = CostCenterSerializer


class CostCenterDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = CostCenterSerializer


class CostCenterGroupListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = CostCenterGroupSerializer


class CostCenterGroupDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = CostCenterGroupSerializer
