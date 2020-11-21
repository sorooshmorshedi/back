from django.db.models.query import Prefetch
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from factors.models import Adjustment, FactorItem
from factors.serializers import AdjustmentListRetrieveSerializer, AdjustmentCreateUpdateSerializer
from factors.views.definite_factor import DefiniteFactor
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_object_by_code


class WarehouseHandlingModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'warehouseHandling'

    serializer_class = AdjustmentListRetrieveSerializer

    def get_queryset(self):
        return Adjustment.objects.inFinancialYear()

    def destroy(self, request, *args, **kwargs):
        self.delete_object()
        return Response({}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data

        serialized = AdjustmentCreateUpdateSerializer(instance=self.get_object(), data=data['adjustment'])
        serialized.is_valid(raise_exception=True)
        serialized.save()

        adjustment = serialized.instance

        res = Response(AdjustmentListRetrieveSerializer(instance=adjustment).data, status=status.HTTP_200_OK)
        return res

    def create(self, request, *args, **kwargs):
        data = request.data

        serialized = AdjustmentCreateUpdateSerializer(data=data['adjustment'], context={
            'financial_year': request.user.active_financial_year
        })
        serialized.is_valid(raise_exception=True)
        serialized.save()

        adjustment = serialized.instance

        res = Response(AdjustmentListRetrieveSerializer(instance=adjustment).data, status=status.HTTP_200_OK)
        return res

    def delete_object(self):
        instance = self.get_object()
        factor = instance.factor
        if not factor.is_deletable:
            raise ValidationError('تعدیل غیر قابل حذف می باشد')
        DefiniteFactor.undoDefinition(self.request.user, factor)
        instance.delete()
        factor.delete()


class GetAdjustmentByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'adjustment'

    def get(self, request):
        data = request.GET

        item = get_object_by_code(
            Adjustment.objects.hasAccess(request.method, self.permission_basename).filter(
                type=data.get('type')
            ),
            data.get('position'),
            data.get('id')
        )
        if item:
            return Response(AdjustmentListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)
