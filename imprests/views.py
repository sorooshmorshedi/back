from django.db.models import QuerySet
from django.db.models.query import Prefetch
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.auth import BasicCRUDPermission
from helpers.functions import get_object_by_code, get_new_code
from helpers.views.MassRelatedCUD import MassRelatedCUD
from helpers.views.confirm_view import ConfirmView
from imprests.models import ImprestSettlement, ImprestSettlementItem
from imprests.serializers import ImprestSettlementCreateUpdateSerializer, ImprestSettlementItemCreateUpdateSerializer
from transactions.serializers import TransactionListRetrieveSerializer


class ImprestSettlementModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'imprestSettlement'
    serializer_class = TransactionListRetrieveSerializer

    def get_queryset(self) -> QuerySet:
        return ImprestSettlement.objects.hasAccess(self.request.method, self.permission_basename)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        form_data = data['item']
        items_data = data['items']

        serializer = ImprestSettlementCreateUpdateSerializer(data=form_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            code=get_new_code(ImprestSettlement)
        )

        instance = serializer.instance
        MassRelatedCUD(
            user,
            items_data.get('items'),
            items_data.get('ids_to_delete'),
            'imprestSettlement',
            serializer.instance.id,
            ImprestSettlementItemCreateUpdateSerializer,
            ImprestSettlementItemCreateUpdateSerializer
        ).sync()

        instance.sync()

        return Response(
            TransactionListRetrieveSerializer(instance=instance.transaction).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        user = request.user
        form_data = request.data['item']
        items_data = request.data['items']

        serialized = ImprestSettlementCreateUpdateSerializer(instance=instance, data=form_data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        MassRelatedCUD(
            user,
            items_data.get('items', []),
            items_data.get('ids_to_delete', []),
            'imprestSettlement',
            instance.id,
            ImprestSettlementItemCreateUpdateSerializer,
            ImprestSettlementItemCreateUpdateSerializer
        ).sync()

        instance.sync()

        return Response(
            TransactionListRetrieveSerializer(instance=instance.transaction).data,
            status=status.HTTP_200_OK
        )


class ImprestSettlementByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'imprestSettlement'

    def get(self, request):
        item = get_object_by_code(
            ImprestSettlement.objects.hasAccess('get'),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(TransactionListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class ConfirmImprest(ConfirmView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'imprestSettlement'
    model = ImprestSettlement
