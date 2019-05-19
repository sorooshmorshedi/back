from django.db import connection
from django.db.models import Sum, F, DecimalField, Window, Q
from rest_framework import generics
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from factors.models import FactorItem, Factor
from reports.inventory.filters import InventoryFilter
from reports.inventory.serializers import FactorItemInventorySerializer


def addSum(queryset, data):
    data.append({
        'remain': data[-1]['remain'],
        'input': {
            'count': queryset.filter(factor__type__in=Factor.BUY_GROUP).aggregate(Sum('count'))['count__sum'],
            'fee': '-',
            'value': queryset.filter(factor__type__in=Factor.BUY_GROUP).aggregate(
                value=Sum(F('fee') * F('count'), output_field=DecimalField())
            )['value'],
        },
        'output': {
            'count': queryset.filter(factor__type__in=Factor.SALE_GROUP).aggregate(Sum('count'))['count__sum'],
            'fee': '-',
            'value': queryset.filter(factor__type__in=Factor.SALE_GROUP).aggregate(
                value=Sum(F('fee') * F('count'), output_field=DecimalField())
            )['value'],
        }
    })


class InventoryListView(generics.ListAPIView):
    serializer_class = FactorItemInventorySerializer
    filter_class = InventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = FactorItem.objects.inFinancialYear(self.request.user).filter(factor__is_definite=True) \
            .prefetch_related('factor__account') \
            .prefetch_related('factor__sanad') \
            .order_by('factor__definition_date') \
            .annotate(
                cumulative_input_count=Window(
                    expression=Sum('count', filter=Q(calculated_output_value=0)),
                    order_by=F('id').asc()
                ),
                cumulative_output_count=Window(
                    expression=Sum('count', filter=~Q(calculated_output_value=0)),
                    order_by=F('id').asc()
                )
            )

        return queryset

    def list(self, request, *args, **kwargs):

        params = self.request.GET

        factor_items = self.get_queryset()

        queryset = self.filter_class(params, queryset=factor_items).qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            addSum(queryset, data)

        response = paginator.get_paginated_response(data)
        # print(len(connection.queries))
        return response


class WarehouseInventoryListView(InventoryListView):
    def get_queryset(self):
        return FactorItem.objects.inFinancialYear(self.request.user).filter(factor__is_definite=True)\
            .prefetch_related('ware') \
            .prefetch_related('factor__account') \
            .prefetch_related('factor__sanad') \
            .order_by('factor__definition_date')
