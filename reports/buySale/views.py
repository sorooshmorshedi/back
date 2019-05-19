from django.db.models import Sum, DecimalField
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from reports.lists.filters import *
from reports.lists.serializers import *


def addSum(queryset, data):
    data.append({
        'count': queryset.aggregate(Sum('count'))['count__sum'],
        'value': queryset.annotate(value=Sum(F('fee') * F('count'), output_field=DecimalField()))
            .aggregate(Sum('value'))['value__sum']
    })


class BuySaleView(generics.ListAPIView):
    serializer_class = FactorItemListSerializer
    filterset_class = FactorItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return FactorItem.objects.inFinancialYear(self.request.user)\
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

