from django.db.models import F
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.defaultAccounts.models import DefaultAccount
from factors.helpers import getInventoryCount
from helpers.auth import BasicCRUDPermission
from helpers.exceptions.ConfirmationError import ConfirmationError
from helpers.functions import get_current_user, get_object_by_code
from helpers.views.confirm_view import ConfirmView
from sanads.models import clearSanad, newSanadCode
from factors.serializers import *
from server.settings import TESTING
from wares.models import WareInventory, Ware


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


def get_factor_permission_basename(factor_type):
    base_codename = ''
    if factor_type == Factor.BUY:
        base_codename = 'buy'
    elif factor_type == Factor.SALE:
        base_codename = 'sale'
    elif factor_type == Factor.BACK_FROM_BUY:
        base_codename = 'backFromBuy'
    elif factor_type == Factor.BACK_FROM_SALE:
        base_codename = 'backFromSale'
    return "{}Factor".format(base_codename)


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
            code=Factor.newCodes(factor_type=factor_data.get('type'))
        )

        factor = serializer.instance
        factor.sync(user, data)

        self.check_confirmations(request, factor)

        res = Response(FactorListRetrieveSerializer(instance=factor).data, status=status.HTTP_200_OK)
        return res

    def update(self, request, *args, **kwargs):

        factor = self.get_object()

        if not factor.is_editable:
            raise ValidationError('فاکتور غیر قابل ویرایش می باشد')

        data = request.data
        user = request.user

        is_definite = factor.is_definite
        if is_definite:
            DefiniteFactor.undoDefinition(user, factor)

        serialized = FactorCreateUpdateSerializer(instance=factor, data=data['item'])
        serialized.is_valid(raise_exception=True)
        serialized.save()

        factor.sync(user, data)

        if is_definite:
            DefiniteFactor.definiteFactor(user, factor.pk, perform_inventory_check=True,
                                          is_confirmed=request.data.get('_confirmed'))

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

            if not ware.isService:
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
            Factor.objects.hasAccess(request.method, self.permission_basename).filter(type=request.GET['type']),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(FactorListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


def check_inventory(user, factor_items, consider_old_count):
    inventories = []
    for item in factor_items:
        if type(item) is FactorItem:
            ware = item.ware
            warehouse = item.warehouse
            old_count = item.count
        else:
            ware = Ware.objects.inFinancialYear().get(pk=item['ware'])
            warehouse = Warehouse.objects.inFinancialYear().get(pk=item['warehouse'])
            if 'id' in item:
                old_count = FactorItem.objects.inFinancialYear().get(pk=item['id']).count
            else:
                old_count = 0

        if not consider_old_count:
            old_count = 0

        is_duplicate_row = False
        for inventory in inventories:
            if inventory['ware'] == ware and inventory['warehouse'] == warehouse:
                inventory['remain'] += old_count
                is_duplicate_row = True
        if not is_duplicate_row:
            remain = getInventoryCount(user, warehouse, ware) + old_count
            inventories.append({
                'ware': ware,
                'warehouse': warehouse,
                'remain': remain
            })

    for item in factor_items:
        if type(item) is FactorItem:
            ware = item.ware
            warehouse = item.warehouse
            count = Decimal(item.count)
        else:
            ware = Ware.objects.inFinancialYear().get(pk=item['ware'])
            warehouse = Warehouse.objects.inFinancialYear().get(pk=item['warehouse'])
            count = Decimal(item['count'])

        if ware.isService:
            continue

        for inventory in inventories:
            if inventory['ware'] == ware and inventory['warehouse'] == warehouse:
                inventory['remain'] -= count

            if inventory['remain'] < 0:
                raise ValidationError("موجودی انبار برای کالای {} کافی نیست.".format(inventory['ware']))


class DefiniteFactor(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_codename(self):
        if self.request.method.lower() == 'post':
            factor_data = self.request.data['item']
            factor_type = factor_data.get('type')
        else:
            factor_type = self.get_object().type
        return "definite.".format(get_factor_permission_basename(factor_type))

    def post(self, request, pk):
        user = request.user
        factor = DefiniteFactor.definiteFactor(user, pk, is_confirmed=request.data.get('_confirmed'))
        return Response(FactorListRetrieveSerializer(factor).data)

    @staticmethod
    def undoDefinition(user, factor: Factor):
        sanad = DefiniteFactor.getFactorSanad(user, factor)
        clearSanad(sanad)

        sanad.is_auto_created = True
        factor.is_definite = False
        factor.definition_date = None
        factor.save()

        financial_year = user.active_financial_year

        for factor_item in factor.items.all():

            ware = factor_item.ware
            warehouse = factor_item.warehouse

            if ware.isService:
                continue

            if factor_item.factor.type in Factor.INPUT_GROUP:
                WareInventory.decrease_inventory(ware, warehouse, factor_item.count, financial_year, revert=True)
            else:
                ware = factor_item.ware
                if ware.pricingType == Ware.FIFO:
                    fees = factor_item.fees.copy()
                    fees.reverse()
                    for fee in fees:
                        WareInventory.increase_inventory(ware, warehouse, fee['count'], fee['fee'], financial_year,
                                                         revert=True)

            factor_item.fees = []
            factor_item.remain_fees = []
            factor_item.save()

    @staticmethod
    def definiteFactor(user, pk, perform_inventory_check=True, is_confirmed=False):
        factor = get_object_or_404(Factor.objects.inFinancialYear(), pk=pk)
        permission_codename = "definite.".format(get_factor_permission_basename(factor.type))
        user.has_object_perm(factor, permission_codename, raise_exception=True)

        sanad = DefiniteFactor.getFactorSanad(user, factor)
        factor.sanad = sanad

        DefiniteFactor.setFactorItemsFeesAndUpdateInventory(factor)

        first_row_bed = 0
        first_row_bes = 0

        second_row_bed = 0
        second_row_bes = 0

        if factor.type in Factor.SALE_GROUP:
            first_row_bed = factor.sum
            second_row_bes = factor.sum
            if factor.type == Factor.SALE:
                account = 'sale'
            else:
                account = 'backFromBuy'
        else:
            first_row_bes = factor.sum
            second_row_bed = factor.sum
            if factor.type == Factor.BUY:
                account = 'buy'
            else:
                account = 'backFromSale'

        code = factor.code

        explanation = "فاکتور {} شماره {} به تاریخ {} {} مشتری".format(
            factor.type_label,
            code,
            str(factor.date),
            "از" if factor.type in Factor.BUY_GROUP else "به"
        )

        if factor.type != Factor.BACK_FROM_BUY:
            DefiniteFactor.submitSumSanadItems(
                user,
                factor,
                first_row_bed,
                first_row_bes,
                second_row_bed,
                second_row_bes,
                account,
                explanation
            )

        if factor.type == Factor.SALE:
            DefiniteFactor.submitSaleSanadItems(user, factor, explanation)
        elif factor.type == Factor.BACK_FROM_SALE:
            DefiniteFactor.submitBackFromSaleSanadItems(user, factor, explanation)
        elif factor.type == Factor.BACK_FROM_BUY:
            DefiniteFactor.submitBackFromBuySanadItems(user, factor, explanation)

        DefiniteFactor.submitDiscountSanadItems(
            user,
            factor,
            factor.discountSum if first_row_bed != 0 else 0,
            factor.discountSum if first_row_bes != 0 else 0,
            factor.discountSum if second_row_bed != 0 else 0,
            factor.discountSum if second_row_bes != 0 else 0,
            account,
            explanation
        )
        DefiniteFactor.submitTaxSanadItems(
            user,
            factor,
            factor.taxSum if first_row_bed != 0 else 0,
            factor.taxSum if first_row_bes != 0 else 0,
            factor.taxSum if second_row_bed != 0 else 0,
            factor.taxSum if second_row_bes != 0 else 0,
            account,
            explanation
        )
        DefiniteFactor.submitExpenseSanadItems(factor, explanation)

        factor.definition_date = now()
        factor.sanad = sanad
        factor.is_definite = True
        factor.save()

        if not is_confirmed:
            sanad.check_account_balance_confirmations()

        if perform_inventory_check and factor.type in Factor.SALE_GROUP:
            factor.check_inventory()

        return factor

    @staticmethod
    def getFactorSanad(user, factor):
        if not factor.sanad:
            sanad = Sanad(
                code=newSanadCode(),
                date=factor.date,
                is_auto_created=True,
                explanation=factor.explanation,
                financial_year=user.active_financial_year
            )
        else:
            sanad = factor.sanad
            clearSanad(sanad)
            sanad.date = factor.date
            sanad.is_auto_created = True
            sanad.explanation = factor.explanation
        sanad.save()

        return sanad

    @staticmethod
    def setFactorItemsFeesAndUpdateInventory(factor):
        for item in factor.items.order_by('id').all():

            if item.ware.isService:
                continue

            if factor.type in Factor.SALE_GROUP:
                item.fees = WareInventory.get_fees(item.ware, item.warehouse, item.count)

            DefiniteFactor.updateInventoryOnFactorItemSave(item)

            item.remain_fees = WareInventory.get_remain_fees(item.ware)
            item.save()

    @staticmethod
    def submitSumSanadItems(user, factor, first_row_bed, first_row_bes, second_row_bed, second_row_bes, account,
                            explanation):
        sanad = factor.sanad
        if factor.sum:
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                costCenter=factor.costCenter,
                bed=first_row_bed,
                bes=first_row_bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )

            sanad.items.create(
                account=DefaultAccount.get(account).account,
                floatAccount=DefaultAccount.get(account).floatAccount,
                costCenter=DefaultAccount.get(account).costCenter,
                bed=second_row_bed,
                bes=second_row_bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )

    @staticmethod
    def submitDiscountSanadItems(user, factor, first_row_bed, first_row_bes, second_row_bed, second_row_bes, account,
                                 explanation):
        sanad = factor.sanad
        if factor.discountSum:
            sanad.items.create(
                account=DefaultAccount.get(account).account,
                floatAccount=DefaultAccount.get(account).floatAccount,
                costCenter=DefaultAccount.get(account).costCenter,
                bed=first_row_bed,
                bes=first_row_bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                costCenter=factor.costCenter,
                bed=second_row_bed,
                bes=second_row_bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )

    @staticmethod
    def submitTaxSanadItems(user, factor, first_row_bed, first_row_bes, second_row_bed, second_row_bes, account,
                            explanation):
        sanad = factor.sanad
        # Factor Tax Sum
        if factor.taxSum:
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                costCenter=factor.costCenter,
                bed=first_row_bed,
                bes=first_row_bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )
            sanad.items.create(
                account=DefaultAccount.get('tax').account,
                floatAccount=DefaultAccount.get('tax').floatAccount,
                costCenter=DefaultAccount.get('tax').costCenter,
                bed=second_row_bed,
                bes=second_row_bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )

    @staticmethod
    def submitExpenseSanadItems(factor, explanation):
        sanad = factor.sanad
        for e in factor.expenses.all():
            if e.value:
                sanad.items.create(
                    account=e.expense.account,
                    floatAccount=e.expense.floatAccount,
                    costCenter=e.expense.costCenter,
                    bed=e.value,
                    explanation=explanation,
                    financial_year=sanad.financial_year
                )
                sanad.items.create(
                    account=e.account,
                    floatAccount=e.floatAccount,
                    costCenter=e.costCenter,
                    bes=e.value,
                    explanation=explanation,
                    financial_year=sanad.financial_year
                )

    @staticmethod
    def submitSaleSanadItems(user, factor, explanation):
        sanad = factor.sanad
        value = 0
        for item in factor.items.all():
            value += item.calculated_output_value

        sanad.items.create(
            account=Account.get_cost_of_sold_wares_account(user),
            bed=value,
            explanation=explanation,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            account=Account.get_inventory_account(user),
            bes=value,
            explanation=explanation,
            financial_year=sanad.financial_year
        )

    @staticmethod
    def submitBackFromSaleSanadItems(user, factor, explanation):
        sanad = factor.sanad
        value = 0

        for item in factor.items.all():
            value += item.calculated_output_value

        sanad.items.create(
            account=Account.get_inventory_account(user),
            bed=value,
            explanation=explanation,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            account=Account.get_cost_of_sold_wares_account(user),
            bes=value,
            explanation=explanation,
            financial_year=sanad.financial_year
        )

    @staticmethod
    def submitBackFromBuySanadItems(user, factor, explanation):
        sanad = factor.sanad
        value = 0
        for item in factor.items.all():
            value += item.calculated_output_value

        sanad.items.create(
            account=factor.account,
            floatAccount=factor.floatAccount,
            costCenter=factor.costCenter,
            bed=factor.sum,
            explanation=explanation,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            account=Account.get_inventory_account(user),
            bes=value,
            explanation=explanation,
            financial_year=sanad.financial_year
        )

        profit_and_loss_value = value - factor.sum
        if profit_and_loss_value:
            bed = 0
            bes = 0
            if profit_and_loss_value > 0:
                bed = profit_and_loss_value
            else:
                profit_and_loss_value = abs(profit_and_loss_value)
                bes = profit_and_loss_value

            sanad.items.create(
                account=DefaultAccount.get('profitAndLossFromBuying').account,
                floatAccount=DefaultAccount.get('profitAndLossFromBuying').floatAccount,
                costCenter=DefaultAccount.get('profitAndLossFromBuying').costCenter,
                bed=bed,
                bes=bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )

    @staticmethod
    def updateInventoryOnFactorItemSave(factor_item, financial_year=None):
        from factors.models import Factor
        from factors.models import FactorItem

        if not financial_year:
            financial_year = get_current_user().active_financial_year

        ware = factor_item.ware
        warehouse = factor_item.warehouse

        if ware.isService:
            return

        if factor_item.factor.type in Factor.INPUT_GROUP:
            WareInventory.increase_inventory(ware, warehouse, factor_item.count, factor_item.fee, financial_year)
        else:
            WareInventory.decrease_inventory(ware, warehouse, factor_item.count, financial_year)

        is_used_in_next_years = FactorItem.objects.filter(
            factor__financial_year__start__gt=financial_year.start,
            factor__type__in=Factor.OUTPUT_GROUP,
            ware=ware
        ).exists()

        if is_used_in_next_years:
            raise ValidationError("ابتدا فاکتور های سال مالی بعدی را پاک نمایید")


class ConfirmFactor(ConfirmView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    model = Factor

    @property
    def permission_codename(self):
        return get_factor_permission_basename(self.get_object().type)
