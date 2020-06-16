from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from helpers.auth import BasicCRUDPermission
from helpers.views.RetrieveUpdateDestroyAPIViewWithAutoFinancialYear import \
    RetrieveUpdateDestroyAPIViewWithAutoFinancialYear
from helpers.views.ListCreateAPIViewWithAutoFinancialYear import ListCreateAPIViewWithAutoFinancialYear
from wares.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class WarehouseListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'warehouse'
    serializer_class = WarehouseSerializer

    def perform_create(self, serializer: WarehouseSerializer) -> None:
        serializer.save(financial_year=self.request.user.active_financial_year)


class WarehouseDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'warehouse'
    serializer_class = WarehouseSerializer


class UnitDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'unit'
    serializer_class = UnitSerializer


class UnitListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'unit'
    serializer_class = UnitSerializer

    def perform_create(self, serializer: UnitSerializer) -> None:
        serializer.save(financial_year=self.request.user.active_financial_year)


class WareListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'ware'
    serializer_class = WareSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = WareListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer: WareSerializer) -> None:
        category = serializer.validated_data.get('category')
        code = category.get_new_child_code()
        print(category.code, code)
        serializer.save(
            code=code,
            financial_year=self.request.user.active_financial_year
        )


class WareDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'ware'
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
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'wareLevel'
    serializer_class = WareLevelSerializer


class WareLevelListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'wareLevel'
    serializer_class = WareLevelSerializer

    def perform_create(self, serializer: WareLevelSerializer) -> None:
        parent = serializer.validated_data.get('parent')
        if parent:
            code = parent.get_new_child_code()
        else:
            code = WareLevel.get_new_nature_code()
        serializer.save(
            code=code,
            financial_year=self.request.user.active_financial_year
        )
