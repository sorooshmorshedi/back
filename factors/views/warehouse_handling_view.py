from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from factors.models import Factor
from factors.models.warehouse_handling import WarehouseHandling
from factors.serializers import WarehouseHandlingCreateUpdateSerializer, WarehouseHandlingItemCreateUpdateSerializer, \
    WarehouseHandlingListRetrieveSerializer, AdjustmentCreateUpdateSerializer
from factors.views.adjustment_views import AdjustmentModelView
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_object_by_code, get_new_code
from helpers.views.MassRelatedCUD import MassRelatedCUD


class WarehouseHandlingModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'warehouseHandling'

    serializer_class = WarehouseHandlingListRetrieveSerializer

    def get_queryset(self):
        return WarehouseHandling.objects.inFinancialYear()

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = WarehouseHandlingCreateUpdateSerializer(
            data=data['item'],
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=request.user.active_financial_year
        )

        items_data = data.get('items')
        MassRelatedCUD(
            request.user,
            items_data['items'],
            items_data['ids_to_delete'],
            'warehouseHandling',
            serializer.instance.id,
            WarehouseHandlingItemCreateUpdateSerializer,
            WarehouseHandlingItemCreateUpdateSerializer
        ).sync()

        return Response(
            WarehouseHandlingListRetrieveSerializer(instance=serializer.instance).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = WarehouseHandlingCreateUpdateSerializer(instance=self.get_object(), data=data['item'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance

        items_data = data.get('items')
        MassRelatedCUD(
            request.user,
            items_data['items'],
            items_data['ids_to_delete'],
            'warehouseHandling',
            instance.id,
            WarehouseHandlingItemCreateUpdateSerializer,
            WarehouseHandlingItemCreateUpdateSerializer
        ).sync()

        if instance.is_defined:
            WarehouseHandlingDefiniteView.definite(instance)

        return Response(
            WarehouseHandlingListRetrieveSerializer(instance=instance).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        output_adjustment = instance.outputAdjustment
        input_adjustment = instance.inputAdjustment
        if output_adjustment: AdjustmentModelView.delete_adjustment(output_adjustment)
        if input_adjustment: AdjustmentModelView.delete_adjustment(input_adjustment)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WarehouseHandlingDefiniteView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'warehouseHandling'

    def post(self, request):
        instance = get_object_or_404(WarehouseHandling, pk=request.data['id'])
        WarehouseHandlingDefiniteView.definite(instance)

        return Response(
            WarehouseHandlingListRetrieveSerializer(instance=instance).data,
            status=status.HTTP_200_OK
        )

    @staticmethod
    def definite(instance: WarehouseHandling):
        input_items = []
        output_items = []
        for item in instance.items.all():

            if item.warehouse_remain is None:
                raise ValidationError("موجودی شمارش شده همه ردیف ها را وارد کنید")

            contradiction = item.contradiction
            if contradiction is not None:
                adjustment_item = {
                    'ware': item.ware.id,
                    'warehouse': instance.warehouse.id,
                    'count': abs(contradiction),
                    'unit': item.ware.main_unit.id,
                    'unit_count': abs(contradiction),
                    'is_auto_created': True
                }
                if contradiction > 0:
                    input_items.append(adjustment_item)
                elif contradiction < 0:
                    output_items.append(adjustment_item)

        adjustment_data = {
            'explanation': instance.explanation,
            'date': str(instance.submit_date),
            'time': str(instance.submit_time),
            'is_auto_created': True,
            'items': []
        }

        input_adjustment = instance.inputAdjustment
        output_adjustment = instance.outputAdjustment

        adjustment_data['items'] = input_items
        adjustment_data['type'] = Factor.INPUT_ADJUSTMENT
        input_serializer = AdjustmentCreateUpdateSerializer(
            instance=input_adjustment,
            data=adjustment_data,
            context={
                'financial_year': instance.financial_year
            }
        )
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()

        adjustment_data['items'] = output_items
        adjustment_data['type'] = Factor.OUTPUT_ADJUSTMENT
        output_serializer = AdjustmentCreateUpdateSerializer(
            instance=output_adjustment,
            data=adjustment_data,
            context={
                'financial_year': instance.financial_year
            }
        )
        output_serializer.is_valid(raise_exception=True)
        output_serializer.save()

        instance.inputAdjustment = input_serializer.instance
        instance.outputAdjustment = output_serializer.instance
        instance.is_defined = True
        if instance.code is None:
            instance.code = get_new_code(WarehouseHandling)
        instance.save()


class GetWarehouseHandlingByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'warehouseHandling'

    def get(self, request):
        data = request.GET

        item = get_object_by_code(
            WarehouseHandling.objects.hasAccess(request.method, self.permission_basename),
            data.get('position'),
            data.get('id')
        )
        if item:
            return Response(WarehouseHandlingListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)
