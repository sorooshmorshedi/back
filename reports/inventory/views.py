from django.db.models import Sum, F, DecimalField, Window, Q, Prefetch, Subquery, OuterRef
from django.db.models.functions.comparison import Coalesce
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from factors.models import FactorItem, Factor
from reports.inventory.filters import InventoryFilter, AllWaresInventoryFilter
from reports.inventory.serializers import WareInventorySerializer, AllWaresInventorySerializer, \
    WarehouseInventorySerializer, AllWarehousesInventorySerializer
from wares.models import Ware


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
                # value=Sum(F('fee') * F('count'), output_field=DecimalField())
                value=Sum('calculated_output_value')
            )['value'],
        }
    })


class WareInventoryListView(generics.ListAPIView):
    serializer_class = WareInventorySerializer
    filter_class = InventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = FactorItem.objects.inFinancialYear() \
            .filter(factor__is_definite=True, factor__type__in=(*Factor.SALE_GROUP, *Factor.BUY_GROUP)) \
            .prefetch_related('factor__account') \
            .prefetch_related('factor__sanad') \
            .order_by('factor__definition_date', 'id')

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
        # p.rint(len(connection.queries))
        return response


class AllWaresInventoryListView(generics.ListAPIView):
    serializer_class = AllWaresInventorySerializer
    filter_class = AllWaresInventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        last_factor_item = Subquery(FactorItem.objects.inFinancialYear()
                                    .filter(ware_id=OuterRef('ware_id'))
                                    .filter(factor__is_definite=True,
                                            factor__type__in=(*Factor.SALE_GROUP, *Factor.BUY_GROUP)
                                            )
                                    .order_by('factor__definition_date')
                                    .values_list('id', flat=True)[:1])

        input_filter = Q(
            factorItems__factor__is_definite=True,
            factorItems__factor__type__in=Factor.BUY_GROUP
        )

        output_filter = Q(
            factorItems__factor__is_definite=True,
            factorItems__factor__type__in=Factor.SALE_GROUP
        )

        queryset = Ware.objects.inFinancialYear() \
            .prefetch_related(Prefetch('factorItems', queryset=FactorItem.objects.filter(id__in=last_factor_item))) \
            .annotate(
            input_count=Coalesce(Sum('factorItems__count', filter=input_filter), 0),
            input_value=Coalesce(Sum(F('factorItems__fee') * F('factorItems__count'), 0),
                                 filter=input_filter, output_field=DecimalField()),
            output_count=Coalesce(Sum('factorItems__count', filter=output_filter), 0),
            output_value=Coalesce(Sum(F('factorItems__calculated_output_value'),
                                      filter=output_filter, output_field=DecimalField()), 0)
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

        # if len(data) and paginator.offset + paginator.limit >= paginator.count:
        #     addSum(queryset, data)

        response = paginator.get_paginated_response(data)
        # print(len(connection.queries))
        return response


class WarehouseInventoryListView(generics.ListAPIView):
    serializer_class = WarehouseInventorySerializer
    filter_class = InventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = FactorItem.objects.inFinancialYear() \
            .filter(factor__is_definite=True) \
            .prefetch_related('factor__account') \
            .prefetch_related('factor__sanad') \
            .prefetch_related('warehouse') \
            .order_by('factor__definition_date', 'id') \
            .annotate(
            definition_date=F('factor__definition_date'),
            type=F('factor__type')
        ) \
            .annotate(
            cumulative_input_count=Window(
                expression=Sum('count', filter=Q(type__in=Factor.INPUT_GROUP)),
                order_by=[F('definition_date').asc(), F('id').asc()]
            ),
            cumulative_output_count=Window(
                expression=Sum('count', filter=Q(type__in=Factor.OUTPUT_GROUP)),
                order_by=[F('definition_date').asc(), F('id').asc()]
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
            data.append({
                'input': data[-1]['cumulative_count']['input'],
                'output': data[-1]['cumulative_count']['output'],
                'remain': data[-1]['remain']
            })

        response = paginator.get_paginated_response(data)
        # print(len(connection.queries))
        return response


class AllWarehousesInventoryListView(generics.ListAPIView):
    serializer_class = AllWarehousesInventorySerializer
    filter_class = AllWaresInventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        warehouse = self.request.GET.get('warehouse', None)

        input_filter = Q(
            factorItems__factor__is_definite=True,
            factorItems__factor__type__in=Factor.INPUT_GROUP
        )

        output_filter = Q(
            factorItems__factor__is_definite=True,
            factorItems__factor__type__in=Factor.OUTPUT_GROUP
        )

        if warehouse:
            input_filter &= Q(factorItems__warehouse=warehouse)
            output_filter &= Q(factorItems__warehouse=warehouse)

        queryset = Ware.objects.inFinancialYear() \
            .annotate(
            input_count=Sum('factorItems__count', filter=input_filter),
            output_count=Sum('factorItems__count', filter=output_filter),
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

        # if len(data) and paginator.offset + paginator.limit >= paginator.count:
        #     addSum(queryset, data)

        response = paginator.get_paginated_response(data)
        # print(len(connection.queries))
        return response
