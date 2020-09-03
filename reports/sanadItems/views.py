from django.db.models.aggregates import Sum
from django.db.models.expressions import Window, F, Value
from django.db.models.fields import IntegerField
from django.db.models.functions.comparison import Coalesce
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helpers.auth import BasicCRUDPermission
from helpers.exports import get_xlsx_response
from reports.sanadItems.filters import SanadItemLedgerFilter
from reports.sanadItems.serializers import SanadItemLedgerSerializer
from sanads.models import SanadItem

"""
Used for sanadItems, journal & bill reports
"""


class SanadItemListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.sanadItems'
    serializer_class = SanadItemLedgerSerializer
    filterset_class = SanadItemLedgerFilter
    pagination_class = LimitOffsetPagination
    ordering_fields = '__all__'

    def get_queryset(self):
        qs = SanadItem.objects.hasAccess(self.request.method, 'get.sanadItemsReport', use_financial_year=False)

        order_sanads_by = self.request.GET.copy().get('order_sanads_by', None)

        if order_sanads_by:
            qs = qs.order_by('sanad__{}'.format(order_sanads_by))
        else:
            ordering = self.request.GET.copy().get('ordering', None)
            if ordering:
                qs = qs.order_by(ordering)

        qs = qs.annotate(
            sanad_date=F('sanad__date'),
            sanad_code=F('sanad__code')
        )

        order_by = [F('sanad__{}'.format(order_sanads_by or 'code')).asc(), F('id').asc()]

        qs = qs.annotate(
            comulative_bed=Window(expression=Sum('bed'), order_by=order_by),
            comulative_bes=Window(expression=Sum('bes'), order_by=order_by)
        )

        previous_sum = self.get_previous_sum()

        qs = qs.annotate(
            previous_bed=Value(previous_sum['bed'], IntegerField()),
            previous_bes=Value(previous_sum['bes'], IntegerField())
        )

        return qs

    def get_previous_sum(self):

        filters = {}
        request_filters = self.request.GET.copy()

        for key in request_filters.keys():
            value = request_filters[key]
            if value and key.startswith(tuple(self.filterset_class.Meta.fields.keys())):
                filters[key] = value

        has_range_filter = False
        if 'sanad__date__gte' in filters:
            filters['sanad__date__lt'] = filters.get('sanad__date__gte') or None
            has_range_filter = True
            del filters['sanad__date__gte']
        if 'sanad__code__gte' in filters:
            filters['sanad__code__lt'] = filters['sanad__code__gte']
            has_range_filter = True
            del filters['sanad__code__gte']

        if has_range_filter:
            result = self.get_queryset().filter(**filters).aggregate(
                bed=Coalesce(Sum('bed'), 0),
                bes=Coalesce(Sum('bes'), 0)
            )
        else:
            result = {
                'bed': 0,
                'bes': 0
            }

        return result

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SanadItemExportView(SanadItemListView):

    def get(self, request, **kwargs):
        sheet_name = 'sanadItems.xlsx'

        data = [[
            '#',
            'تاریخ',
            'شماره سند',
            'شرح',
            'حساب',
            'بدهکار',
            'بستانکار',
            'مانده',
            'تشخیص'
        ]]

        rows = self.serializer_class(self.get_queryset(), many=True).data
        row = None
        for row in rows:
            sanad = row['sanad']
            data.append([
                rows.index(row) + 1,
                sanad['date'],
                sanad['code'],
                row['explanation'],
                row['account']['code'] + " " + row['account']['name'],
                row['bed'],
                row['bes'],
                row['remain'],
                row['remain_type'],
            ])

        if row:
            data.append([
                '',
                '',
                '',
                '',
                'مجموع',
                row['comulative_bed'],
                row['comulative_bes'],
                row['remain'],
                row['remain_type'],
            ])

        return get_xlsx_response(sheet_name, data)
