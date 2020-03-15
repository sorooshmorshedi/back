from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from factors.helpers import getInventoryCount
from factors.models import Transfer, FactorItem
from factors.serializers import TransferListRetrieveSerializer, TransferCreateSerializer
from wares.models import Ware, Warehouse


class TransferModelView(viewsets.ModelViewSet):
    serializer_class = TransferListRetrieveSerializer

    def get_queryset(self):
        return Transfer.objects.inFinancialYear()

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        return res

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)
        return res

    def destroy(self, request, *args, **kwargs):
        self.delete_transfer_object()
        return Response({}, status=status.HTTP_200_OK)

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        self.delete_transfer_object()

        data = request.data
        data['transfer']['financial_year'] = request.user.active_financial_year.id
        items = data['transfer']['items']

        self.check_inventory(items)

        serialized = TransferCreateSerializer(data=data['transfer'])
        serialized.is_valid(raise_exception=True)
        serialized.save()

        transfer = serialized.instance

        res = Response(TransferListRetrieveSerializer(instance=transfer).data, status=status.HTTP_200_OK)
        return res

    @transaction.atomic()
    def create(self, request, *args, **kwargs):

        data = request.data

        data['transfer']['financial_year'] = request.user.active_financial_year.id

        items = data['transfer']['items']

        self.check_inventory(items)

        serialized = TransferCreateSerializer(data=data['transfer'])
        serialized.is_valid(raise_exception=True)
        serialized.save()

        transfer = serialized.instance

        res = Response(TransferListRetrieveSerializer(instance=transfer).data, status=status.HTTP_200_OK)
        return res

    def check_inventory(self, items):
        user = self.request.user
        inventories = []
        for item in items:
            ware = Ware.objects.inFinancialYear().get(pk=item['ware'])
            warehouse = Warehouse.objects.inFinancialYear().get(pk=item['output_warehouse'])
            if 'id' in item:
                old_count = FactorItem.objects.inFinancialYear().get(pk=item['id']).count
            else:
                old_count = 0
            remain = getInventoryCount(user, warehouse, ware)
            remain += old_count

            is_duplicate_row = False
            for inventory in inventories:
                if inventory['ware'] == ware and inventory['warehouse'] == warehouse:
                    inventory['remain'] += remain
                    is_duplicate_row = True
            if not is_duplicate_row:
                inventories.append({
                    'ware': ware,
                    'warehouse': warehouse,
                    'remain': remain
                })

        for item in items:
            count = int(item['count'])
            for inventory in inventories:
                if inventory['ware'].id == item['ware'] and inventory['warehouse'].id == item['output_warehouse']:
                    inventory['remain'] -= count

                if inventory['remain'] < 0:
                    raise ValidationError("موجودی انبار برای کالای {} کافی نیست.".format(inventory['ware']))

    def delete_transfer_object(self):
        instance = self.get_object()
        input_factor = instance.input_factor
        output_factor = instance.output_factor
        if not input_factor.is_last_definite_factor and not output_factor.is_last_definite_factor:
            raise ValidationError('انتقال غیر قابل ویرایش می باشد')
        instance.delete()
        input_factor.delete()
        output_factor.delete()


@api_view(['get'])
def getTransferByPosition(request):
    if 'position' not in request.GET or request.GET['position'] not in ('next', 'prev', 'first', 'last'):
        return Response(['موقعیت وارد نشده است'], status.HTTP_400_BAD_REQUEST)

    id = request.GET.get('id', None)
    position = request.GET['position']
    queryset = Transfer.objects.inFinancialYear()

    try:
        if position == 'next':
            factor = queryset.filter(pk__gt=id).order_by('id')[0]
        elif position == 'prev':
            if id:
                queryset = queryset.filter(pk__lt=id)
            factor = queryset.order_by('-id')[0]
        elif position == 'first':
            factor = queryset.order_by('id')[0]
        elif position == 'last':
            factor = queryset.order_by('-id')[0]
    except IndexError:
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)

    serializer = TransferListRetrieveSerializer(factor)
    return Response(serializer.data)