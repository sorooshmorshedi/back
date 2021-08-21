from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from factors.models.transfer_model import Transfer
from factors.serializers import TransferListRetrieveSerializer, TransferCreateUpdateSerializer
from factors.views.definite_factor import DefiniteFactor
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_object_by_code, get_new_code
from helpers.views.lock_view import ToggleItemLockView


class TransferModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'transfer'

    serializer_class = TransferListRetrieveSerializer

    def get_queryset(self):
        return Transfer.objects.inFinancialYear()

    def destroy(self, request, *args, **kwargs):
        self.delete_transfer_object()
        return Response({}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serialized = TransferCreateUpdateSerializer(self.get_object(), data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        transfer = serialized.instance

        return Response(TransferListRetrieveSerializer(instance=transfer).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        serialized = TransferCreateUpdateSerializer(data=data, context={
            'financial_year': request.user.active_financial_year
        })
        serialized.is_valid(raise_exception=True)
        serialized.save(
            financial_year=self.request.user.active_financial_year,
            code=get_new_code(Transfer)
        )

        transfer = serialized.instance

        res = Response(TransferListRetrieveSerializer(instance=transfer).data, status=status.HTTP_200_OK)
        return res

    def delete_transfer_object(self):
        instance = self.get_object()
        input_factor = instance.input_factor
        output_factor = instance.output_factor
        if not input_factor.is_deletable and not output_factor.is_deletable:
            raise ValidationError('انتقال غیر قابل ویرایش می باشد')
        instance.delete()

        if not input_factor.is_deletable or not output_factor.is_deletable:
            raise ValidationError('انتقال غیر قابل حذف می باشد')

        DefiniteFactor.updateFactorInventory(input_factor, revert=True)
        DefiniteFactor.updateFactorInventory(output_factor, revert=True)

        input_factor.delete()
        output_factor.delete()


class GetTransferByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'transfer'

    def get(self, request):
        item = get_object_by_code(
            Transfer.objects.hasAccess(request.method, self.permission_basename),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(TransferListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class DefineTransferView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_codename = 'define.transfer'
    serializer_class = TransferListRetrieveSerializer

    def post(self, request):
        data = request.data
        item_data = data.pop('item')
        item = get_object_or_404(
            self.serializer_class.Meta.model,
            pk=item_data['id']
        )

        if not item.is_defined:
            DefiniteFactor.updateFactorInventory(item.output_factor)
            DefiniteFactor.updateFactorInventory(item.input_factor)
            item.define()
            serializer = TransferCreateUpdateSerializer(instance=item, data=item_data)
            serializer.is_valid()
            serializer.save()

        return Response(self.serializer_class(instance=item).data)


class ToggleTransferLockView(ToggleItemLockView):
    serializer_class = TransferListRetrieveSerializer
    permission_codename = 'lock.transfer'
