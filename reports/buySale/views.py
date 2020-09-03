from django.db.models import Sum, DecimalField
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from helpers.auth import BasicCRUDPermission
from helpers.exports import get_xlsx_response
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
        'warehouse': {
            'name': 'جمع'
        },
        'count': remain_count,
        'value': remain_value,
        'discount': remain_discount,
        'total_value': remain_total_value
    })


class BuySaleView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_codename(self):
        if self.request.GET['factor__type__in'] == 'sale,backFromSale':
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
        params = self.request.GET.copy()
        return Factor.SALE if params['factor__type__in'] == 'sale,backFromSale' else Factor.BUY

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


class BuySaleExportView(BuySaleView):
    def get(self, request, **kwargs):
        queryset = self.get_queryset()
        items = self.serializer_class(queryset, many=True).data
        addSum(queryset, items, self.report_type)

        data = [[
            '#',
            'تاریخ',
            'نوع فاکتور',
            'عطف فاکتور',
            'شماره فاکتور',
            'خریدار/فروشنده',
            'انبار',
            'تعداد',
            'فی',
            'مبلغ',
            'تخفیف',
            'مبلغ کل',
            'شرح فاکتور',
            'توضیحات',
        ]]

        for item in items[:-1]:
            print(item['factor']['account'], item['factor']['type'])
            data.append([
                items.index(item) + 1,
                item['factor']['date'],
                Factor.get_type_label(item['factor']['type']),
                item['factor']['id'],
                item['factor']['code'],
                item['factor']['account']['name'],
                item['warehouse']['name'],
                item['count'],
                item['fee'],
                item['value'],
                item['discount'],
                item['total_value'],
                item['factor']['explanation'],
                item['explanation'],
            ])

        item = items[-1]
        data.append([
            '', '', '', '', '', '', '',
            item['warehouse']['name'],
            item['count'],
            item['value'],
            item['discount'],
            item['total_value'],
        ])

        if self.report_type == Factor.BUY:
            file_name = "Buy Report"
        else:
            file_name = "Sale Report"

        return get_xlsx_response(file_name, data)
