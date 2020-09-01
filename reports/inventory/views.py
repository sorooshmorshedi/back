from django.db.models import Sum, F, DecimalField, Window, Q, Prefetch, Subquery, OuterRef
from django.db.models.functions.comparison import Coalesce
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from factors.models import FactorItem, Factor
from helpers.auth import BasicCRUDPermission
from reports.inventory.filters import InventoryFilter, AllWaresInventoryFilter
from reports.inventory.serializers import WareInventorySerializer, AllWaresInventorySerializer, \
    WarehouseInventorySerializer, AllWarehousesInventorySerializer
from wares.models import Ware


def addSum(queryset, data):
    data.append({
        'factor': {
            'explanation': 'مجموع',
        },
        'remain': data[-1]['remain'],
        'input': {
            'count': queryset.filter(factor__type__in=Factor.BUY_GROUP).aggregate(Sum('count'))['count__sum'],
            'fee': '-',
            'value': queryset.filter(factor__type__in=Factor.BUY_GROUP).aggregate(value=Sum('calculated_value'))[
                'value'
            ]
        },
        'output': {
            'count': queryset.filter(factor__type__in=Factor.SALE_GROUP).aggregate(Sum('count'))['count__sum'],
            'fee': '-',
            'value': queryset.filter(factor__type__in=Factor.SALE_GROUP).aggregate(
                value=Sum('calculated_value')
            )['value'],
        }
    })


class WareInventoryListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.wareInventoryReport'
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
        return response


class AllWaresInventoryListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.allWaresInventoryReport'
    serializer_class = AllWaresInventorySerializer
    filter_class = AllWaresInventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        last_factor_item = Subquery(
            FactorItem.objects.inFinancialYear().filter(
                ware_id=OuterRef('ware_id')
            ).filter(
                factor__is_definite=True,
                factor__type__in=(*Factor.SALE_GROUP, *Factor.BUY_GROUP)
            ).order_by('factor__definition_date').values_list('id', flat=True)[:1]
        )

        input_filter = Q(
            factorItems__factor__is_definite=True,
            factorItems__factor__type__in=Factor.BUY_GROUP
        )

        output_filter = Q(
            factorItems__factor__is_definite=True,
            factorItems__factor__type__in=Factor.SALE_GROUP
        )

        queryset = Ware.objects.inFinancialYear().prefetch_related(
            Prefetch('factorItems', queryset=FactorItem.objects.filter(id__in=last_factor_item))
        ).annotate(
            input_count=Coalesce(Sum('factorItems__count', filter=input_filter), 0),
            input_value=Coalesce(Sum(
                F('factorItems__fee') * F('factorItems__count'),
                filter=input_filter,
                output_field=DecimalField()
            ), 0),
            output_count=Coalesce(Sum('factorItems__count', filter=output_filter), 0),
            output_value=Coalesce(Sum(
                F('factorItems__calculated_value'),
                filter=output_filter,
                output_field=DecimalField()
            ), 0)
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
            totals = queryset.aggregate(
                total_input_count=Sum('input_count'),
                total_input_value=Sum('input_value'),
                total_output_count=Sum('output_count'),
                total_output_value=Sum('output_value'),
            )
            data.append({
                'name': 'مجموع',
                'input': {
                    'count': totals['total_input_count'],
                    'fee': ' - ',
                    'value': totals['total_input_value']
                },
                'output': {
                    'count': totals['total_output_count'],
                    'fee': ' - ',
                    'value': totals['total_output_value']
                },
                'remain': {
                    'count': totals['total_input_count'] - totals['total_output_count'],
                    'fee': ' - ',
                    'value': totals['total_input_value'] - totals['total_output_value']
                },
            })

        response = paginator.get_paginated_response(data)
        return response


class WarehouseInventoryListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.warehouseInventoryReport'
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
                'factor': {
                    'account': {
                        'name': 'جمع'
                    }
                },
                'input': data[-1]['cumulative_count']['input'],
                'output': data[-1]['cumulative_count']['output'],
                'remain': data[-1]['remain']
            })

        response = paginator.get_paginated_response(data)
        # print(len(connection.queries))
        return response


class AllWarehousesInventoryListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.allWarehousesInventoryReport'
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

        queryset = Ware.objects.inFinancialYear().annotate(
            input_count=Coalesce(Sum('factorItems__count', filter=input_filter), 0),
            output_count=Coalesce(Sum('factorItems__count', filter=output_filter), 0)
        )

        queryset = queryset.annotate(
            remaining_count=Coalesce(F('input_count') - F('output_count'), 0)
        )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            totals = queryset.aggregate(
                total_input_count=Sum('input_count'),
                total_output_count=Sum('output_count'),
            )
            data.append({
                'name': 'جمع',
                'input_count': totals['total_input_count'],
                'output_count': totals['total_output_count'],
                'remaining_count': totals['total_input_count'] - totals['total_output_count']
            })

        response = paginator.get_paginated_response(data)
        return response
