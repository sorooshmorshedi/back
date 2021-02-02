from decimal import Decimal
from typing import Any

from django.core.management import call_command
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from werkzeug.routing import ValidationError

from helpers.auth import BasicCRUDPermission
from helpers.views.RetrieveUpdateDestroyAPIViewWithAutoFinancialYear import \
    RetrieveUpdateDestroyAPIViewWithAutoFinancialYear
from helpers.views.ListCreateAPIViewWithAutoFinancialYear import ListCreateAPIViewWithAutoFinancialYear
from reports.lists.filters import SalePriceFilter
from wares.models import SalePriceChange, WareSalePriceChange
from wares.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class WarehouseListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'warehouse'
    serializer_class = WarehouseSerializer

    def perform_create(self, serializer: WarehouseSerializer) -> None:
        serializer.save(financial_year=self.request.user.active_financial_year)


class WarehouseDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'warehouse'
    serializer_class = WarehouseSerializer


class UnitDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'unit'
    serializer_class = UnitSerializer


class UnitListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'unit'
    serializer_class = UnitSerializer

    def perform_create(self, serializer: UnitSerializer) -> None:
        serializer.save(financial_year=self.request.user.active_financial_year)


class SalePriceTypeDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'salePriceType'
    serializer_class = SalePriceTypeSerializer


class SalePriceTypeListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'salePriceType'
    serializer_class = SalePriceTypeSerializer

    def perform_create(self, serializer: SalePriceTypeSerializer) -> None:
        serializer.save(financial_year=self.request.user.active_financial_year)


class WareListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'ware'
    serializer_class = WareSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = WareListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer: WareSerializer) -> None:
        level = serializer.validated_data.get('level')

        if level == Ware.NATURE:
            code = Ware.get_new_nature_code()
        else:
            parent = serializer.validated_data.get('parent')
            code = parent.get_new_child_code()

        serializer.save(
            code=code,
            financial_year=self.request.user.active_financial_year
        )


def update_sale_prices(ware: Ware, data: list):
    data = list(filter(lambda o: o['unit'], data))
    if len(data) == 0:
        raise ValidationError("واحد اصلی کالا اجباری می باشد")

    ware.salePrices.all().delete()
    for row in data:
        unit = Unit.objects.get(pk=row['unit'])
        prices = row['prices']
        for price_type_id in prices.keys():
            price_type = SalePriceType.objects.get(pk=price_type_id)
            price = prices[price_type_id]
            if price:
                ware.salePrices.create(
                    unit=unit,
                    type=price_type,
                    price=price,
                    conversion_factor=row['conversion_factor'],
                )


class WareDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'ware'
    serializer_class = WareSerializer

    def retrieve(self, request, **kwargs):
        ware = self.get_object()
        serializer = WareRetrieveSerializer(ware)
        return Response(serializer.data)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        ware = self.get_object()
        if ware.pricingType != request.data.get('pricingType') and ware.has_factorItem():
            return Response(['نحوه قیمت گذاری کالا های دارای گردش غیر قابل تغییر می باشد'],
                            status=status.HTTP_400_BAD_REQUEST)
        update_sale_prices(ware, request.data.get('salePrices', []))
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        ware = self.get_object()
        if not ware.has_factorItem():
            return super().destroy(request, *args, **kwargs)

        return Response(['کالا های دارای گردش در سال مالی جاری غیر قابل حذف می باشند'],
                        status=status.HTTP_400_BAD_REQUEST)


class SortInventoryView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'sort.inventory'

    def post(self, request):
        user = request.user
        financial_year = user.active_financial_year
        if not financial_year.is_advari:
            raise ValidationError("فقط سیستم های ادواری امکان مرتب سازی کاردکس را دارند")

        call_command('refresh_inventory', user.id)

        return Response([])


class ChangeSalePricesView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = "salePrice"

    def put(self, request):
        qs = SalePrice.objects.hasAccess('get').all()
        qs = SalePriceFilter(request.data['filters'], qs).qs

        try:
            is_percent = request.data['operation']['is_percent']
            is_increase = request.data['operation']['is_increase']
            rate = Decimal(request.data['operation']['rate'])
        except IndexError:
            raise ValidationError("لطفا همه فیلد ها را وارد کنید")

        sale_price_change = SalePriceChange.objects.create(
            is_percent=is_percent,
            is_increase=is_increase,
            rate=rate
        )

        for sale_price in qs.all():
            price = sale_price.price
            previous_price = price

            if is_percent:
                diff = price * rate / 100
            else:
                diff = rate

            if is_increase:
                new_price = price + diff
            else:
                new_price = price - diff

            sale_price.price = new_price
            sale_price.save()

            WareSalePriceChange.objects.create(
                salePriceChange=sale_price_change,
                salePrice=sale_price,
                previous_price=previous_price,
                new_price=new_price
            )

        return Response([])
