from django.db.models import Sum, DecimalField
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from reports.buySale.serializers import BuySaleSerializer
from reports.lists.filters import *
from reports.lists.serializers import *


def addSum(queryset, data, report_type):
    input_count = queryset.filter(factor__type__in=Factor.BUY_GROUP).aggregate(Sum('count'))['count__sum']
    output_count = queryset.filter(factor__type__in=Factor.SALE_GROUP).aggregate(Sum('count'))['count__sum']

    input_value = queryset.filter(factor__type__in=Factor.BUY_GROUP) \
        .annotate(value=Sum(F('fee') * F('count'), output_field=DecimalField())) \
        .aggregate(Sum('value'))['value__sum']
    output_value = queryset.filter(factor__type__in=Factor.SALE_GROUP) \
        .annotate(value=Sum(F('fee') * F('count'), output_field=DecimalField())) \
        .aggregate(Sum('value'))['value__sum']

    input_discount = queryset.filter(factor__type__in=Factor.BUY_GROUP) \
        .annotate(value=Sum('discountValue')) \
        .aggregate(Sum('value'))['value__sum']
    output_discount = queryset.filter(factor__type__in=Factor.SALE_GROUP) \
        .annotate(value=Sum('discountValue')) \
        .aggregate(Sum('value'))['value__sum']

    input_count = input_count if input_count else 0
    output_count = output_count if output_count else 0
    remain_count = input_count - output_count

    input_value = input_value if input_value else 0
    output_value = output_value if output_value else 0
    remain_value = input_value - output_value

    input_discount = input_discount if input_discount else 0
    output_discount = output_discount if output_discount else 0
    remain_discount = input_discount - output_discount

    if report_type == Factor.SALE:
        remain_count = -remain_count
        remain_discount = -remain_discount
        remain_value = -remain_value

    remain_total_value = remain_value - remain_discount

    data.append({
        'count': remain_count,
        'value': remain_value,
        'discount': remain_discount,
        'total_value': remain_total_value
    })


class BuySaleView(generics.ListAPIView):
    serializer_class = BuySaleSerializer
    filterset_class = FactorItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return FactorItem.objects.inFinancialYear(self.request.user)\
            .filter(factor__is_definite=True)\
            .prefetch_related('factor__account')\
            .prefetch_related('ware') \
            .prefetch_related('warehouse')\
            .order_by('id')\
            .all()

    def list(self, request, *args, **kwargs):

        params = self.request.GET

        report_type = Factor.SALE if params['factor__type__in'] == 'sale,backFromSale' else Factor.BUY

        factor_items = self.get_queryset()

        queryset = self.filterset_class(params, queryset=factor_items).qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            addSum(queryset, data, report_type)

        response = paginator.get_paginated_response(data)
        # print(len(connection.queries))
        return response

