from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.db.models.query import Prefetch
from django.db.models.query_utils import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.auth import BasicCRUDPermission
from helpers.db import queryset_iterator
from helpers.functions import get_object_by_code
from helpers.views.MassRelatedCUD import MassRelatedCUD
from helpers.views.confirm_view import ConfirmView
from sanads.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class SanadListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'sanad'
    serializer_class = SanadSerializer

    def get_queryset(self):
        return Sanad.objects.hasAccess(self.request.method)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = SanadListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        sanad_data = data.get('item')
        items_data = data.get('items')

        serializer = SanadSerializer(data=sanad_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            code=newSanadCode(),
            is_auto_created=False,
        )

        MassRelatedCUD(
            user,
            items_data.get('items'),
            items_data.get('ids_to_delete'),
            'sanad',
            serializer.instance.id,
            SanadItemSerializer,
            SanadItemSerializer,
        ).sync()

        serializer.instance.update_values()

        is_confirmed = data.get('_confirmed')
        if not is_confirmed:
            serializer.instance.check_account_balance_confirmations()

        return Response(SanadListRetrieveSerializer(instance=serializer.instance).data, status=status.HTTP_201_CREATED)


class SanadDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'sanad'
    serializer_class = SanadSerializer

    def get_queryset(self):
        return Sanad.objects.hasAccess(self.request.method)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset().prefetch_related(
            'created_by',
            Prefetch('items', SanadItem.objects.order_by('pk')),
            'items__account',
            'items__account__floatAccountGroup',
            'items__account__costCenterGroup',
            'items__floatAccount',
            'items__costCenter',
            'items__floatAccount__floatAccountGroups',
            'items__costCenter__floatAccountGroups',
        )
        sanad = get_object_or_404(queryset, pk=pk)
        serializer = SanadListRetrieveSerializer(sanad)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        sanad_data = data.get('item')
        items_data = data.get('items')

        serializer = SanadSerializer(instance=self.get_object(), data=sanad_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        MassRelatedCUD(
            user,
            items_data.get('items'),
            items_data.get('ids_to_delete'),
            'sanad',
            serializer.instance.id,
            SanadItemSerializer,
            SanadItemSerializer,
        ).sync()

        serializer.instance.update_values()

        is_confirmed = data.get('_confirmed')
        if not is_confirmed:
            serializer.instance.check_account_balance_confirmations()

        return Response(SanadListRetrieveSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)


class ReorderSanadsApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_codename = 'reorder.sanad'

    def post(self, request):
        qs = Sanad.objects.inFinancialYear().annotate(
            items_count=Count('items')
        )
        order = request.data.get('order', None)

        max_code = qs.aggregate(max_code=Max('code'))['max_code']
        code = max_code + 1

        if order is None:
            self._update_sanads_code(code, qs, 'local_id')
        else:
            next_code = self._update_sanads_code(code, qs.filter(~Q(items_count=0)), order)
            self._update_sanads_code(next_code, qs.filter(Q(items_count=0)), order)

        qs.update(code=F('code') - max_code)

        return Response([])

    @staticmethod
    def _update_sanads_code(from_code, qs, order):
        next_code = from_code
        for sanad in queryset_iterator(qs, key=order):
            sanad.code = next_code
            sanad.save()
            next_code += 1
        return next_code


class SanadByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_codename = 'get.sanad'

    def get(self, request):
        item = get_object_by_code(
            Sanad.objects.hasAccess(request.method, 'sanad').prefetch_related(
                Prefetch('items', SanadItem.objects.order_by('pk')),
            ),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(SanadListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class ConfirmSanad(ConfirmView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'sanad'
    model = Sanad
