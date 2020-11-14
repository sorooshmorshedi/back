from django.db.models import F
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.auth import BasicCRUDPermission
from helpers.exceptions.ConfirmationError import ConfirmationError
from helpers.functions import get_object_by_code
from helpers.views.confirm_view import ConfirmView
from factors.serializers import *
from server.settings import TESTING


class ExpenseModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = ExpenseSerializer
    permission_basename = 'expense'

    def get_queryset(self):
        return Expense.objects.hasAccess(self.request.method)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serialized = ExpenseListRetrieveSerializer(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serialized = ExpenseListRetrieveSerializer(instance)
        return Response(serialized.data)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class FactorModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    serializer_class = FactorCreateUpdateSerializer

    @property
    def permission_basename(self):
        if self.request.method.lower() == 'post':
            factor_data = self.request.data['item']
            factor_type = factor_data.get('type')
        else:
            factor_type = Factor.objects.get(pk=self.kwargs['pk']).type
        return get_factor_permission_basename(factor_type)

    def get_queryset(self):
        return Factor.objects.hasAccess(self.request.method, self.permission_basename)

    # Disabled
    def list(self, request, *ergs, **kwargs):
        return Response([])

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset().prefetch_related(
            Prefetch('items', FactorItem.objects.order_by('pk'))
        )
        instance = get_object_or_404(queryset, pk=pk)
        serialized = FactorListRetrieveSerializer(instance)
        return Response(serialized.data)

    def create(self, request, *args, **kwargs):

        data = request.data
        user = request.user

        factor_data = data['item']

        serializer = FactorCreateUpdateSerializer(data=factor_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            temporary_code=Factor.get_new_temporary_code(factor_type=factor_data.get('type'))
        )

        factor = serializer.instance
        factor.sync(user, data)

        self.check_confirmations(request, factor)

        res = Response(FactorListRetrieveSerializer(instance=factor).data, status=status.HTTP_200_OK)
        return res

    def update(self, request, *args, **kwargs):
        factor = self.get_object()

        data = request.data
        user = request.user

        factor.verify_items(data['items']['items'], data['items']['ids_to_delete'])

        is_definite = factor.is_definite
        if is_definite:
            DefiniteFactor.undoDefinition(user, factor)

        serialized = FactorCreateUpdateSerializer(instance=factor, data=data['item'])
        serialized.is_valid(raise_exception=True)
        serialized.save()

        factor.sync(user, data)

        if is_definite:
            DefiniteFactor.definiteFactor(user, factor.pk, is_confirmed=request.data.get('_confirmed'))

        self.check_confirmations(request, factor)

        return Response(FactorListRetrieveSerializer(instance=factor).data, status=status.HTTP_200_OK)

    def check_confirmations(self, request, factor: Factor, for_delete=False):

        is_confirmed = request.data.get('_confirmed', False)
        if is_confirmed:
            return

        confirmations = []
        for item in factor.items.all():
            ware = item.ware
            warehouse = item.warehouse
            count = item.count
            is_output = factor.type in Factor.OUTPUT_GROUP

            if is_output and not for_delete:
                if ware.minSale and item.count < ware.minSale:
                    confirmations.append("حداقل مبلغ فروش {} برابر {} می باشد".format(ware.name, ware.minSale))

                if ware.maxSale and item.count > ware.maxSale:
                    confirmations.append("حداکثر مبلغ فروش {} برابر {} می باشد".format(ware.name, ware.maxSale))

            if for_delete:
                is_output = not is_output

            if not ware.is_service:
                balance = ware.get_inventory_count(warehouse)
                if is_output:
                    if ware.minInventory and balance - count < ware.minInventory:
                        confirmations.append("حداقل موجودی {} برابر {} {} می باشد. موجودی فعلی {}".format(
                            ware.name,
                            ware.minInventory,
                            ware.unit.name,
                            balance
                        ))
                else:
                    if ware.maxInventory and balance + count > ware.maxInventory:
                        confirmations.append("حداکثر موجودی {} برابر {} {} می باشد. موجودی فعلی {}".format(
                            ware.name,
                            ware.minInventory,
                            ware.unit.name,
                            balance
                        ))

        if len(confirmations):

            if not TESTING:
                raise ConfirmationError(confirmations)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        queryset = self.get_queryset()
        factor = get_object_or_404(queryset, pk=pk)
        if not factor.is_deletable:
            raise ValidationError('فاکتور غیر قابل حذف می باشد')

        self.check_confirmations(request, factor, for_delete=True)

        if factor.is_definite:
            DefiniteFactor.undoDefinition(request.user, factor)

        res = super().destroy(request, *args, **kwargs)
        return res


class NotPaidFactorsView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_basename(self):

        transaction_type = self.request.GET.get('transactionType')
        if transaction_type == Transaction.RECEIVE:
            return 'notReceivedFactor'
        else:
            return 'notPaidFactor'

    def get(self, request):

        filters = Q()

        if 'transactionType' not in request.GET:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        tType = request.GET['transactionType']

        if 'transactionId' in request.GET:
            tId = request.GET['transactionId']
            filters &= (~Q(sanad__bed=F('paidValue')) | Q(payments__transaction_id=tId))
        else:
            filters &= ~Q(sanad__bed=F('paidValue'))

        if tType == 'receive':
            filters &= Q(type__in=("sale", "backFromBuy"))
        else:
            filters &= Q(type__in=("buy", "backFromSale"))

        if 'accountId' in request.GET:
            account_id = request.GET['accountId']
            filters &= Q(account=account_id)

        qs = Factor.objects.hasAccess('get', self.permission_basename) \
            .exclude(sanad__bed=0) \
            .filter(filters) \
            .distinct() \
            .prefetch_related('items') \
            .prefetch_related('payments') \
            .prefetch_related('account') \
            .prefetch_related('floatAccount') \
            .prefetch_related('costCenter')
        res = Response(NotPaidFactorsCreateUpdateSerializer(qs, many=True).data)
        return res


class GetFactorByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_basename(self):
        return get_factor_permission_basename(self.request.GET.get('type'))

    def get(self, request):
        item = get_object_by_code(
            Factor.objects.hasAccess(request.method, self.permission_basename).filter(
                type=request.GET['type']
            ).prefetch_related(
                Prefetch('items', FactorItem.objects.order_by('pk'))
            ),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(FactorListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class ConfirmFactor(ConfirmView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    model = Factor

    @property
    def permission_codename(self):
        return get_factor_permission_basename(self.get_object().type)
