from django.db.models import Sum, DecimalField
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from helpers.auth import BasicCRUDPermission
from reports.buySale.serializers import BuySaleSerializer
from reports.lists.export_views import BaseListExportView
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
        'warehouse': {
            'name': 'جمع'
        },
        'count': remain_count,
        'value': remain_value,
        'discount': remain_discount,
        'total_value': remain_total_value
    })


class BuySaleReportView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def is_buy_report(self):
        return not self.request.GET['factor__type__in'] == 'sale,backFromSale'

    @property
    def permission_codename(self):
        if not self.is_buy_report:
            return 'get.saleReport'
        else:
            return 'get.buyReport'

    serializer_class = BuySaleSerializer
    pagination_class = LimitOffsetPagination

    filterset_class = FactorItemFilter
    ordering_fields = '__all__'

    def get_queryset(self):
        qs = FactorItem.objects.inFinancialYear() \
            .filter(factor__is_definite=True) \
            .prefetch_related('factor__account') \
            .prefetch_related('ware') \
            .prefetch_related('warehouse') \
            .all()

        params = self.request.GET.copy()
        ordering = params.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)

        qs = self.filter_queryset(queryset=qs)

        return qs

    @property
    def report_type(self):
        return Factor.BUY if self.is_buy_report else Factor.SALE

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            addSum(queryset, data, self.report_type)

        response = paginator.get_paginated_response(data)
        return response


class BuySaleReportExportView(BuySaleReportView, BaseListExportView):
    filename = None
    title = None

    def get_additional_data(self):
        item = self.get_queryset().first()
        if item:
            return [
                {
                    'text': 'کالا',
                    'value': item.ware.name
                },
            ]
        return []

    def get_rows(self):
        qs = super().get_rows()
        data = self.serializer_class(qs, many=True).data
        addSum(qs, data, self.report_type)
        return data

    def get(self, request, *args, **kwargs):
        if self.is_buy_report:
            self.filename = 'Buy Report'
            self.title = 'گزارش خرید'
        else:
            self.title = 'گزارش فروش'
            self.filename = 'Sale Report'
        return self.get_response(request, *args, **kwargs)
