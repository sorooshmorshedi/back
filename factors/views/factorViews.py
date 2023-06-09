from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from factors.factor_sanad import FactorsAggregatedSanadSanad
from factors.models.factor import get_factor_permission_basename
from helpers.auth import BasicCRUDPermission
from helpers.exceptions.ConfirmationError import ConfirmationError
from helpers.functions import get_object_by_code, get_new_code
from helpers.views.confirm_view import ConfirmView
from factors.serializers import *
from helpers.views.lock_view import ToggleItemLockView
from home.models import DefaultText
from sanads.models import clearSanad
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
        queryset = self.get_queryset()
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
            temporary_code=Factor.get_new_temporary_code(
                factor_type=factor_data.get('type'),
                is_pre_factor=factor_data.get('is_pre_factor')
            )
        )

        factor = serializer.instance
        factor.sync(user, data)

        self.check_confirmations(request, factor)

        if factor.type == Factor.SALE:
            factor.after_rows_explanation = DefaultText.get('under_sale_factor_rows')
            factor.bottom_explanation = DefaultText.get('under_sale_factor')
        elif factor.type == Factor.BACK_FROM_BUY:
            factor.after_rows_explanation = DefaultText.get('under_back_from_buy_factor_rows')
            factor.bottom_explanation = DefaultText.get('under_back_from_buy_factor')

        factor.save()

        if factor.type == Factor.FIRST_PERIOD_INVENTORY:
            DefiniteFactor.definiteFactor(user, factor.pk, is_confirmed=request.data.get('_confirmed'))
            factor.refresh_from_db()

        res = Response(FactorListRetrieveSerializer(instance=factor).data, status=status.HTTP_200_OK)
        return res

    def update(self, request, *args, **kwargs):
        factor = self.get_object()

        data = request.data
        user = request.user

        factor.verify_items(data['items']['items'], data['items']['ids_to_delete'])

        is_defined = factor.is_defined
        if is_defined:
            DefiniteFactor.updateFactorInventory(factor, True)

        serialized = FactorCreateUpdateSerializer(instance=factor, data=data['item'])
        serialized.is_valid(raise_exception=True)
        serialized.save()

        factor.sync(user, data)

        if is_defined:
            DefiniteFactor.definiteFactor(user, factor.pk, is_confirmed=request.data.get('_confirmed'))

        factor.save()

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
                            ware.main_unit.name,
                            balance
                        ))
                else:
                    if ware.maxInventory and balance + count > ware.maxInventory:
                        confirmations.append("حداکثر موجودی {} برابر {} {} می باشد. موجودی فعلی {}".format(
                            ware.name,
                            ware.maxInventory,
                            ware.main_unit.name,
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

        if factor.is_defined:
            DefiniteFactor.updateFactorInventory(factor, True)
            clearSanad(factor.sanad)

        res = super().destroy(request, *args, **kwargs)
        return res


class GetFactorByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_basename(self):
        return get_factor_permission_basename(self.request.GET.get('type'))

    def get(self, request):
        item = get_object_by_code(
            Factor.objects.hasAccess(request.method, self.permission_basename).filter(
                type=request.GET['type'],
                is_pre_factor=request.GET['is_pre_factor'] == 'true'
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


class CreateBackFactorView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)

    @property
    def permission_codename(self):
        factor_type = self.get_object().type
        if factor_type == Factor.SALE:
            return 'create.backFromSaleFactor'
        else:
            return 'create.backFromBuyFactor'

    def get_object(self):
        factor_id = self.request.data.get('id')
        factor = get_object_or_404(Factor, pk=factor_id)
        return factor

    def post(self, request):
        factor = self.get_object()

        if factor.type not in [Factor.BUY, Factor.SALE]:
            raise ValidationError("امکان ثبت فاکتور برگشتی برای این نوع فاکتور وجود ندارد")

        if factor.type == Factor.SALE:
            back_factor_type = Factor.BACK_FROM_SALE
        else:
            back_factor_type = Factor.BACK_FROM_BUY

        back_factor = Factor.objects.create(
            financial_year=factor.financial_year,
            temporary_code=Factor.get_new_temporary_code(factor_type=factor.type),
            account=factor.account,
            floatAccount=factor.floatAccount,
            costCenter=factor.costCenter,
            type=back_factor_type,
            date=jdatetime.date.today(),
            time=now(),
            discountValue=factor.discountValue,
            discountPercent=factor.discountPercent,
            has_tax=factor.has_tax,
            taxValue=factor.taxValue,
            taxPercent=factor.taxPercent,
            visitor=factor.visitor,
            path=factor.path,
            backFrom=factor.id
        )

        for item in factor.items.all():
            item.pk = None
            item.factor = back_factor
            item.save()

        DefiniteFactor.definiteFactor(
            request.user,
            back_factor.pk,
            is_confirmed=request.data.get('_confirmed')
        )

        return Response(FactorListRetrieveSerializer(instance=back_factor).data)


class ToggleFactorLockView(ToggleItemLockView):
    serializer_class = FactorListRetrieveSerializer

    @property
    def permission_codename(self):
        return f'lock.{get_factor_permission_basename(self.request.data.get("type"))}'


class FactorsAggregatedSanadModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FactorsAggregatedSanadCreateUpdateSerializer

    @property
    def permission_basename(self):
        if self.request.method.lower() == 'post':
            factor_type = self.request.data.get('type')
        else:
            factor_type = FactorsAggregatedSanad.objects.get(pk=self.kwargs['pk']).type
        return get_factor_permission_basename(factor_type) + 'sAggregatedSanad'

    def get_queryset(self):
        return FactorsAggregatedSanad.objects.hasAccess(self.request.method, self.permission_basename)

    def perform_create(self, serializer: FactorsAggregatedSanadCreateUpdateSerializer) -> None:
        serializer.save(
        )

    def create(self, request, *args, **kwargs):

        data = request.data

        serializer = FactorsAggregatedSanadCreateUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=self.request.user.active_financial_year,
            code=get_new_code(FactorsAggregatedSanad)
        )
        FactorsAggregatedSanadSanad(serializer.instance).update()

        return Response(
            FactorsAggregatedSanadRetrieveSerializer(instance=serializer.instance).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        serialized = FactorsAggregatedSanadCreateUpdateSerializer(instance=instance, data=data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        FactorsAggregatedSanadSanad(instance).update()

        return Response(
            FactorsAggregatedSanadRetrieveSerializer(instance=instance).data,
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serialized = FactorsAggregatedSanadRetrieveSerializer(instance)
        return Response(serialized.data)


class GetFactorsAggregatedSanadsByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_basename(self):
        return get_factor_permission_basename(self.request.GET.get('type')) + 'AggregatedSanad'

    def get(self, request):
        item = get_object_by_code(
            FactorsAggregatedSanad.objects.hasAccess(request.method, self.permission_basename).filter(
                type=request.GET['type'],
            ),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(FactorsAggregatedSanadRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)
