from django.db.models import Sum, F, DecimalField, Window, Q, Prefetch, Subquery, OuterRef
from django.db.models.functions.comparison import Coalesce
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from factors.models import FactorItem, Factor
from helpers.auth import BasicCRUDPermission
from helpers.exports import get_xlsx_response
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
    filter_class = InventoryFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = FactorItem.objects.inFinancialYear() \
            .filter(factor__is_definite=True, factor__type__in=(*Factor.SALE_GROUP, *Factor.BUY_GROUP)) \
            .prefetch_related('factor__account') \
            .prefetch_related('factor__sanad') \
            .order_by('factor__definition_date', 'id')

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


class WareInventoryExportView(WareInventoryListView):
    def get(self, request, **kwargs):
        queryset = self.get_queryset()
        items = self.serializer_class(queryset, many=True).data
        addSum(queryset, items)

        data = [[
            '#',
            'تاریخ',
            'نوع فاکتور',
            'شماره فاکتور',
            'شرح فاکتور',
            'نام حساب',
            *ware_common_headers
        ]]

        for item in items[:-1]:
            data.append([
                items.index(item) + 1,
                item['factor']['date'],
                item['factor']['code'],
                item['factor']['explanation'],
                item['factor']['account']['name'],
                *get_ware_common_columns(item)
            ])

        item = items[-1]
        data.append([
            '', '', '', '',
            item['factor']['explanation'],
            '',
            *get_ware_common_columns(item)
        ])

        return get_xlsx_response('Ware Inventory', data)


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

        queryset = self.filter_class(params, queryset=factor_items).qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            self.add_sum(queryset, data)

        response = paginator.get_paginated_response(data)
        return response


class AllWaresInventoryExportView(AllWaresInventoryListView):
    def get(self, request, **kwargs):
        queryset = self.get_queryset()
        items = self.serializer_class(queryset, many=True).data
        self.add_sum(queryset, items)

        data = [[
            '#',
            'کالا',
            *ware_common_headers
        ]]

        for item in items[:-1]:
            data.append([
                items.index(item) + 1,
                item['name'],
                *get_ware_common_columns(item)
            ])

        item = items[-1]
        data.append([
            '',
            item['name'],
            *get_ware_common_columns(item)
        ])

        return get_xlsx_response('All Wares Inventory', data)


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

        queryset = self.filter_class(params, queryset=factor_items).qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        if len(data) and paginator.offset + paginator.limit >= paginator.count:
            self.add_sum(data)

        response = paginator.get_paginated_response(data)
        return response


class WarehouseInventoryExportView(WarehouseInventoryListView):
    def get(self, request, **kwargs):
        queryset = self.get_queryset()
        items = self.serializer_class(queryset, many=True).data
        self.add_sum(items)

        data = [[
            '#',
            'تاریخ',
            'نوع فاکتور',
            'عطف فاکتور',
            'شماره فاکتور',
            'شرح فاکتور',
            'انبار',
            'نام حساب',
            *warehouse_common_headers
        ]]

        for item in items[:-1]:
            account = item['factor']['account']
            account_name = account['name'] if account else ' - '

            data.append([
                items.index(item) + 1,
                item['factor']['date'],
                Factor.get_type_label(item['factor']['type']),
                item['factor']['id'],
                item['factor']['code'],
                item['factor']['explanation'],
                item['warehouse']['name'],
                account_name,
                *get_warehouse_common_columns(item)
            ])

        item = items[-1]
        data.append([
            '', '', '', '', '', '', '',
            item['factor']['account']['name'],
            *get_warehouse_common_columns(item)
        ])

        return get_xlsx_response('Warehouse Inventory', data)


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
            input=Coalesce(Sum('factorItems__count', filter=input_filter), 0),
            output=Coalesce(Sum('factorItems__count', filter=output_filter), 0)
        )

        queryset = queryset.annotate(
            remain=Coalesce(F('input') - F('output'), 0)
        )

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


class AllWarehousesInventoryExportView(AllWarehousesInventoryListView):
    def get(self, request, **kwargs):
        queryset = self.get_queryset()
        items = self.serializer_class(queryset, many=True).data
        self.add_sum(queryset, items)

        data = [[
            '#',
            'کالا',
            *warehouse_common_headers
        ]]

        for item in items[:-1]:
            data.append([
                items.index(item) + 1,
                item['name'],
                *get_warehouse_common_columns(item)
            ])

        item = items[-1]
        data.append([
            '',
            item['name'],
            *get_warehouse_common_columns(item)
        ])

        return get_xlsx_response('All Warehouses Inventory', data)
