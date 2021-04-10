from django.db.models.aggregates import Sum
from django.db.models.expressions import Window, F, Value
from django.db.models.fields import IntegerField
from django.db.models.functions.comparison import Coalesce
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helpers.auth import BasicCRUDPermission
from reports.lists.export_views import BaseListExportView
from reports.sanadItems.filters import SanadItemLedgerFilter
from reports.sanadItems.serializers import SanadItemReportSerializer
from sanads.models import SanadItem

"""
Used for sanadItems (ledger), journal & bill reports
"""


class SanadItemListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.sanad'
    serializer_class = SanadItemReportSerializer
    filterset_class = SanadItemLedgerFilter
    pagination_class = LimitOffsetPagination
    ordering_fields = '__all__'

    def get_queryset(self, *args, **kwargs):
        qs = SanadItem.objects.hasAccess(self.request.method, 'sanadItemsReport', use_financial_year=False).filter(
            financial_year__company=self.request.user.active_company
        )

        order_sanads_by = self.request.GET.copy().get('order_sanads_by', None)

        if order_sanads_by:
            qs = qs.order_by('sanad__{}'.format(order_sanads_by))
            order_by = [F('sanad_{}'.format(order_sanads_by)).asc(), F('id').asc()]
        else:
            ordering = self.request.GET.copy().get('ordering', None)
            if ordering:
                qs = qs.order_by(ordering)
                order_by = [F(ordering), F('id').asc()]
            else:
                qs = qs.order_by('sanad_date')
                order_by = [F('sanad_date').asc(), F('id').asc()]

        qs = qs.annotate(
            sanad_date=F('sanad__date'),
            sanad_code=F('sanad__code')
        )

        qs = qs.annotate(
            comulative_bed=Window(expression=Sum('bed'), order_by=order_by),
            comulative_bes=Window(expression=Sum('bes'), order_by=order_by)
        )

        if kwargs.get('getting_previous_sum', False):
            previous_sum = {
                'bed': 0,
                'bes': 0,
            }
        else:
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
            qs = self.get_queryset(getting_previous_sum=True)
            qs = self.filterset_class(filters, qs).qs
            result = qs.aggregate(
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
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        context = {
            'consider_previous_remain': request.GET.get('consider_previous_remain', False) == 'true'
        }

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, context=context, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, context=context, many=True)
        return Response(serializer.data)


class SanadItemListExportView(SanadItemListView, BaseListExportView):
    filename = 'sanad-items'

    @property
    def title(self):
        return self.request.GET.get('title')

    def get_additional_data(self):
        return [{
            'text': 'حساب',
            'value': self.request.GET.get('account_title', '-')
        }]

    def get_rows(self):
        return self.serializer_class(
            self.filterset_class(self.request.GET, queryset=self.get_queryset()).qs.all(),
            many=True,
            context={
                'consider_previous_remain': self.request.GET.get('consider_previous_remain', False) == 'true'
            }
        ).data

    def get_appended_rows(self):
        last_item = self.get_rows()[-1]
        return [{
            'explanation': 'جمع',
            'bed': last_item['comulative_bed'],
            'bes': last_item['comulative_bes'],
            'remain': last_item['remain'],
            'remain_type': last_item['remain_type'],
        }]

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)
