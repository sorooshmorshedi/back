from django.db.models import Sum, F, Window, Q, Prefetch, Subquery, OuterRef
from django.db.models.functions.comparison import Coalesce
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from factors.models import Factor
from factors.models.factor import FactorItem
from helpers.auth import BasicCRUDPermission
from helpers.querysets import get_deep_sum
from reports.inventory.filters import InventoryFilter, AllWaresInventoryFilter
from reports.inventory.serializers import WareInventorySerializer, AllWaresInventorySerializer, \
    WarehouseInventorySerializer, AllWarehousesInventorySerializer
from reports.lists.export_views import BaseListExportView
from wares.models import Ware, Warehouse

INVENTORY_INPUT_GROUP = Factor.INPUT_GROUP
INVENTORY_OUTPUT_GROUP = Factor.OUTPUT_GROUP


def addSum(queryset, data):
    if len(data) > 0:
        remain = data[-1]['remain']
    else:
        remain = 0
    data.append({
        'factor': {
            'explanation': 'مجموع',
        },
        'remain': remain,
        'input': {
            'count': queryset.filter(factor__type__in=INVENTORY_INPUT_GROUP).aggregate(Sum('count'))['count__sum'],
            'fee': '-',
            'value': queryset.filter(factor__type__in=INVENTORY_INPUT_GROUP).aggregate(value=Sum('calculated_value'))[
                'value'
            ]
        },
        'output': {
            'count': queryset.filter(factor__type__in=INVENTORY_OUTPUT_GROUP).aggregate(Sum('count'))['count__sum'],
            'fee': '-',
            'value': queryset.filter(factor__type__in=INVENTORY_OUTPUT_GROUP).aggregate(
                value=Sum('calculated_value')
            )['value'],
        }
    })


ware_common_headers = [
    'مقدار وارده',
    'فی وارده',
    'مبلغ وارده',
    'مقدار صادره',
    'فی صادره',
    'مبلغ صادره',
    'مقدار مانده',
    'فی مانده',
    'مبلغ مانده',
]


def get_ware_common_columns(item):
    return [
        item['input']['count'],
        item['input']['fee'],
        item['input']['value'],
        item['output']['count'],
        item['output']['fee'],
        item['output']['value'],
        item['remain']['count'],
        item['remain']['fee'],
        item['remain']['value'],
    ]


warehouse_common_headers = [
    'مقدار وارده',
    'مقدار صادره',
    'مقدار مانده',
]


def get_warehouse_common_columns(item):
    return [
        item['input'],
        item['output'],
        item['remain'],
    ]


class WareInventoryListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.wareInventoryReport'
    serializer_class = WareInventorySerializer
    filterset_class = InventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = FactorItem.objects.inFinancialYear().filter(
            factor__is_defined=True,
            # factor__type__in=(
            #     *Factor.SALE_GROUP,
            #     *Factor.BUY_GROUP,
            #     Factor.INPUT_ADJUSTMENT,
            #     Factor.OUTPUT_ADJUSTMENT,
            #     Factor.INPUT_TRANSFER,
            #     Factor.OUTPUT_TRANSFER,
            #     Factor.CONSUMPTION_WARE
            # )
        ).prefetch_related(
            'factor__account',
            'factor__sanad'
        ).order_by('factor__definition_date', 'id')

        queryset = queryset.annotate(
            definition_date=F('factor__definition_date'),
            type=F('factor__type')
        )

        queryset = queryset.annotate(
            comulative_input_count=Window(
                expression=Sum('count', filter=Q(type__in=INVENTORY_INPUT_GROUP)),
                order_by=(F('definition_date'), F('id'))
            ),
            comulative_output_count=Window(
                expression=Sum('count', filter=Q(type__in=INVENTORY_OUTPUT_GROUP)),
                order_by=(F('definition_date'), F('id'))
            ),
        )

        queryset = self.filter_queryset(queryset)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            addSum(queryset, data)

        response = paginator.get_paginated_response(data)
        return response


class WareInventoryExportView(WareInventoryListView, BaseListExportView):
    filename = 'Ware Inventory'
    title = 'کاردکس کالا'

    def get_additional_data(self):
        item = self.get_queryset().first()
        if item:
            return [
                {
                    'text': 'کالا',
                    'value': item.ware.name
                },
                {
                    'text': 'انبار',
                    'value': item.warehouse.name
                }
            ]
        return []

    def get_rows(self):
        qs = super().get_rows()
        data = self.serializer_class(qs, many=True).data
        addSum(qs, data)
        return data

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)


class AllWaresInventoryListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.allWaresInventoryReport'
    serializer_class = AllWaresInventorySerializer
    filterset_class = AllWaresInventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        financial_year = self.request.user.active_financial_year
        last_factor_item = Subquery(
            FactorItem.objects.inFinancialYear().filter(
                ware_id=OuterRef('ware_id')
            ).filter(
                factor__is_defined=True,
                # factor__type__in=(
                #     *Factor.SALE_GROUP,
                #     *Factor.BUY_GROUP,
                #     Factor.INPUT_ADJUSTMENT,
                #     Factor.OUTPUT_ADJUSTMENT,
                #     Factor.CONSUMPTION_WARE
                # )
            ).order_by('factor__definition_date').values_list('id', flat=True)[:1]
        )

        input_filter = {
            'factorItems__factor__is_defined': True,
            # 'factorItems__factor__type__in': Factor.BUY_GROUP,
            'factorItems__factor__type__in': INVENTORY_INPUT_GROUP,
            'factorItems__financial_year': financial_year,
        }

        output_filter = {
            'factorItems__factor__is_defined': True,
            # 'factorItems__factor__type__in': (*Factor.SALE_GROUP, Factor.CONSUMPTION_WARE),
            'factorItems__factor__type__in': INVENTORY_OUTPUT_GROUP,
            'factorItems__financial_year': financial_year,
        }

        queryset = Ware.objects.inFinancialYear().prefetch_related(
            Prefetch('factorItems', queryset=FactorItem.objects.filter(id__in=last_factor_item))
        ).annotate(
            input_count=get_deep_sum('factorItems__count', filters=input_filter),
            input_value=get_deep_sum('factorItems__calculated_value', filters=input_filter),
            output_count=get_deep_sum('factorItems__count', filters=output_filter),
            output_value=get_deep_sum('factorItems__calculated_value', filters=output_filter),
        )

        queryset = queryset.annotate(
            remain_count=Coalesce(F('input_count') - F('output_count'), 0)
        )

        status = self.request.GET.get('status', 'all')
        if status == 'withRemain':
            queryset = queryset.filter(~Q(remain_count=0))
        elif status == 'withoutRemain':
            queryset = queryset.filter(remain_count=0)
        elif status == 'withTransaction':
            queryset = queryset.filter(~Q(input_count=0) | ~Q(output_count=0))
        elif status == 'withoutTransaction':
            queryset = queryset.filter(input_count=0, output_count=0)

        return queryset

    def add_sum(self, queryset, data):
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

    def list(self, request, *args, **kwargs):
        params = self.request.GET

        factor_items = self.get_queryset()

        queryset = self.filterset_class(params, queryset=factor_items).qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            self.add_sum(queryset, data)

        response = paginator.get_paginated_response(data)
        return response


class AllWaresInventoryExportView(AllWaresInventoryListView, BaseListExportView):
    filename = 'All Ware Inventory'
    title = 'کاردکس همه کالا ها'

    def get_rows(self):
        qs = super().get_rows()
        data = self.serializer_class(qs, many=True).data
        self.add_sum(qs, data)
        return data

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)


class WarehouseInventoryListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.warehouseInventoryReport'
    serializer_class = WarehouseInventorySerializer
    filterset_class = InventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = FactorItem.objects.inFinancialYear().filter(
            factor__is_defined=True
        ).prefetch_related(
            'factor__account',
            'factor__sanad',
            'warehouse'
        ).order_by(
            'factor__definition_date', 'id'
        ).annotate(
            definition_date=F('factor__definition_date'),
            type=F('factor__type')
        ).annotate(
            cumulative_input_count=Window(
                expression=Sum('count', filter=Q(type__in=INVENTORY_INPUT_GROUP)),
                order_by=[F('definition_date').asc(), F('id').asc()]
            ),
            cumulative_output_count=Window(
                expression=Sum('count', filter=Q(type__in=INVENTORY_OUTPUT_GROUP)),
                order_by=[F('definition_date').asc(), F('id').asc()]
            )
        )

        return queryset

    def add_sum(self, data):
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

    def list(self, request, *args, **kwargs):
        params = self.request.GET

        factor_items = self.get_queryset()

        queryset = self.filterset_class(params, queryset=factor_items).qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            self.add_sum(data)

        response = paginator.get_paginated_response(data)
        return response


class WarehouseInventoryExportView(WarehouseInventoryListView, BaseListExportView):
    filename = 'Warehouse Inventory'
    title = 'کاردکس کالا'

    def get_additional_data(self):
        item = self.get_queryset().first()
        if item:
            return [
                {
                    'text': 'کالا',
                    'value': item.ware.name
                },
                {
                    'text': 'انبار',
                    'value': item.warehouse.name if self.request.GET.get('warehouse') else 'همه انبار ها'
                }
            ]
        return []

    def get_rows(self):
        qs = super().get_rows()
        data = self.serializer_class(qs, many=True).data
        self.add_sum(data)
        return data

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)


class AllWarehousesInventoryListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.allWarehousesInventoryReport'
    serializer_class = AllWarehousesInventorySerializer
    filterset_class = AllWaresInventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        warehouse = self.request.GET.get('warehouse', None)
        financial_year = self.request.user.active_financial_year

        input_filter = {
            'factorItems__factor__is_defined': True,
            'factorItems__factor__financial_year': financial_year,
            'factorItems__factor__type__in': INVENTORY_INPUT_GROUP
        }

        output_filter = {
            'factorItems__factor__is_defined': True,
            'factorItems__factor__financial_year': financial_year,
            'factorItems__factor__type__in': INVENTORY_OUTPUT_GROUP
        }

        queryset = Ware.objects.inFinancialYear()

        if warehouse:
            input_filter['factorItems__warehouse_id'] = warehouse
            output_filter['factorItems__warehouse_id'] = warehouse

            queryset = queryset.filter(
                Q(warehouse_id=warehouse) |
                Q(children__warehouse_id=warehouse) |
                Q(children__children__warehouse_id=warehouse) |
                Q(children__children__children__warehouse_id=warehouse) |

                (
                        Q(factorItems__warehouse_id=warehouse) &
                        Q(factorItems__factor__financial_year=financial_year)
                ) | (
                        Q(children__factorItems__warehouse_id=warehouse) &
                        Q(children__factorItems__factor__financial_year=financial_year)
                ) | (
                        Q(children__children__factorItems__warehouse_id=warehouse) &
                        Q(children__children__factorItems__factor__financial_year=financial_year)
                ) | (
                        Q(children__children__children__factorItems__warehouse_id=warehouse) &
                        Q(children__children__factorItems__factor__financial_year=financial_year)
                )

            )

        queryset = queryset.annotate(
            input=get_deep_sum('factorItems__count', filters=input_filter),
            output=get_deep_sum('factorItems__count', filters=output_filter)
        )

        queryset = queryset.annotate(
            remain=Coalesce(F('input') - F('output'), 0)

        )

        status = self.request.GET.get('status', 'all')
        if status == 'withRemain':
            queryset = queryset.filter(~Q(remain=0))
        elif status == 'withoutRemain':
            queryset = queryset.filter(remain=0)
        elif status == 'withTransaction':
            queryset = queryset.filter(~Q(input=0) | ~Q(output=0))
        elif status == 'withoutTransaction':
            queryset = queryset.filter(input=0, output=0)

        return queryset

    def add_sum(self, queryset, data):
        totals = queryset.aggregate(
            total_input_count=Sum('input'),
            total_output_count=Sum('output'),
        )
        data.append({
            'name': 'جمع',
            'input': totals['total_input_count'],
            'output': totals['total_output_count'],
            'remain': totals['total_input_count'] - totals['total_output_count']
        })

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            self.add_sum(queryset, data)

        response = paginator.get_paginated_response(data)
        return response


class AllWarehousesInventoryExportView(AllWarehousesInventoryListView, BaseListExportView):
    filename = 'All Warehouses Inventory'
    title = 'کاردکس انبار همه کالا ها'

    def get_additional_data(self):
        data = self.request.GET.copy()
        warehouse = data.get('warehouse')
        if warehouse:
            warehouse = Warehouse.objects.get(pk=warehouse).name
        else:
            warehouse = 'همه انبار ها'

        return [
            {
                'text': 'انبار',
                'value': warehouse
            }
        ]

    def get_rows(self):
        qs = super().get_rows()
        data = self.serializer_class(qs, many=True).data
        self.add_sum(qs, data)
        return data

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)
