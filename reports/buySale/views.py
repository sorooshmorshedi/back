from django.db.models import Sum, DecimalField
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from reports.lists.filters import *
from reports.lists.serializers import *


def addSum(queryset, data):
    input_count = queryset.filter(factor__type__in=Factor.INPUT_GROUP).aggregate(Sum('count'))['count__sum']
    output_count = queryset.filter(factor__type__in=Factor.OUTPUT_GROUP).aggregate(Sum('count'))['count__sum']
    input_value = queryset.filter(factor__type__in=Factor.INPUT_GROUP) \
        .annotate(value=Sum(F('fee') * F('count'), output_field=DecimalField())) \
        .aggregate(Sum('value'))['value__sum']
    output_value = queryset.filter(factor__type__in=Factor.OUTPUT_GROUP) \
        .annotate(value=Sum(F('fee') * F('count'), output_field=DecimalField())) \
        .aggregate(Sum('value'))['value__sum']
    data.append({
        'count': input_count if input_count else 0 - output_count if output_count else 0,
        'value': input_value if input_value else 0 - output_value if output_value else 0
    })


class BuySaleView(generics.ListAPIView):
    serializer_class = FactorItemListSerializer
    filterset_class = FactorItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return FactorItem.objects.inFinancialYear(self.request.user)\
            .filter(factor__is_definite=True) \
            .prefetch_related('factor__account')\
            .prefetch_related('ware') \
            .prefetch_related('warehouse')\
            .all()

    def list(self, request, *args, **kwargs):

        params = self.request.GET

        factor_items = self.get_queryset()

        queryset = self.filterset_class(params, queryset=factor_items).qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            addSum(queryset, data)

        response = paginator.get_paginated_response(data)
        # print(len(connection.queries))
        return response

