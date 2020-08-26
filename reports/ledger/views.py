from django.db.models.aggregates import Sum
from django.db.models.expressions import Window, F, Value
from django.db.models.fields import IntegerField
from django.db.models.functions.comparison import Coalesce
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helpers.auth import BasicCRUDPermission
from reports.ledger.filters import SanadItemLedgerFilter
from reports.ledger.serializers import SanadItemLedgerSerializer
from sanads.models import SanadItem


class LedgerListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.ledgerReport'
    serializer_class = SanadItemLedgerSerializer
    filterset_class = SanadItemLedgerFilter
    pagination_class = LimitOffsetPagination
    ordering_fields = '__all__'

    def get_queryset(self):
        qs = SanadItem.objects.hasAccess(self.request.method, 'get.ledgerReport', use_financial_year=False)

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

        previous_sum = self.get_previous_sum()

        queryset = queryset.annotate(
            previous_bed=Value(previous_sum['bed'], IntegerField()),
            previous_bes=Value(previous_sum['bes'], IntegerField())
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
