from django.db.models import F
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.defaultAccounts.models import getDefaultAccount
from factors.helpers import getInventoryCount
from helpers.exceptions.ConfirmationError import ConfirmationError
from helpers.functions import get_current_user
from sanads.sanads.models import clearSanad, newSanadCode
from factors.serializers import *
from server.settings import TESTING
from wares.models import WareInventory, Ware


class ExpenseModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.inFinancialYear()

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
    permission_classes = [IsAuthenticated]

    serializer_class = FactorCreateUpdateSerializer

    def get_queryset(self):
        return Factor.objects.inFinancialYear()

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serialized = FactorListRetrieveSerializer(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serialized = FactorListRetrieveSerializer(instance)
        return Response(serialized.data)

    def create(self, request, *args, **kwargs):

        data = request.data
        user = request.user

        factor_data = data['factor']

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

        serialized = FactorCreateUpdateSerializer(instance=factor, data=data['factor'])
        serialized.is_valid(raise_exception=True)
        serialized.save()

        factor.sync(user, data)

        if factor.is_definite:
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
            clearSanad(factor.sanad)

        res = super().destroy(request, *args, **kwargs)
        return res


@api_view(['get'])
def newCodesForFactor(request):
    res = Factor.newCodes()
    return Response(res)


@api_view(['get'])
def getNotPaidFactors(request):
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

    qs = Factor.objects.inFinancialYear() \
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


@api_view(['get'])
def getFactorByPosition(request):
    if 'type' not in request.GET:
        return Response(['نوع وارد نشده است'], status.HTTP_400_BAD_REQUEST)
    if 'position' not in request.GET or request.GET['position'] not in ('next', 'prev', 'first', 'last'):
        return Response(['موقعیت وارد نشده است'], status.HTTP_400_BAD_REQUEST)

    type = request.GET['type']
    id = request.GET.get('id', None)
    position = request.GET['position']
    queryset = Factor.objects.inFinancialYear().filter(type=type)

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

    serializer = FactorListRetrieveSerializer(factor)
    return Response(serializer.data)


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

    def post(self, request, pk):
        user = request.user
        factor = DefiniteFactor.definiteFactor(user, pk, is_confirmed=request.data.get('_confirmed'))
        return Response(FactorListRetrieveSerializer(factor).data)

    @staticmethod
    def definiteFactor(user, pk, perform_inventory_check=True, is_confirmed=False):
        factor = get_object_or_404(Factor.objects.inFinancialYear(), pk=pk)

        sanad = DefiniteFactor.getFactorSanad(user, factor)
        factor.sanad = sanad

        DefiniteFactor.setFactorItemsRemains(user, factor)

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
            second_row_bes = factor.sum
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
            first_row_bed,
            first_row_bes,
            second_row_bed,
            second_row_bes,
            account,
            explanation
        )
        DefiniteFactor.submitTaxSanadItems(
            user,
            factor,
            first_row_bed,
            first_row_bes,
            second_row_bed,
            second_row_bes,
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
                createType=Sanad.AUTO,
                type=Sanad.TEMPORARY,
                explanation=factor.explanation,
                financial_year=user.active_financial_year
            )
        else:
            sanad = factor.sanad
            clearSanad(sanad)
            sanad.date = factor.date
            sanad.createType = Sanad.AUTO
            sanad.type = Sanad.TEMPORARY
            sanad.explanation = factor.explanation
        sanad.save()

        return sanad

    @staticmethod
    def setFactorItemsRemains(user, factor):
        prev_items = {}
        for item in factor.items.order_by('id').all():

            if item.ware.isService:
                continue

            ware_id = item.ware.id
            if ware_id in prev_items:
                last_definite_factor = prev_items[ware_id]
            else:
                last_definite_factor = item.ware.last_factor_item(user, exclude_factors=[factor.id])

            if last_definite_factor:
                item.remain_value = last_definite_factor.remain_value
                item.total_input_count = last_definite_factor.total_input_count
                item.total_output_count = last_definite_factor.total_output_count
            else:
                item.remain_value = 0
                item.total_input_count = 0
                item.total_output_count = 0

            if factor.type in Factor.BUY_GROUP:
                item.remain_value += item.value
                item.total_input_count += item.count
                if factor.type == Factor.BACK_FROM_SALE:
                    last_sale = item.ware.last_factor_item(user, other_filters={'factor__type': Factor.SALE})
                    item.calculated_output_value = item.count * last_sale.fees[-1]['fee']
            else:
                calculated_output_value, fees = item.ware.calculated_output_value(user, item.count,
                                                                                  last_definite_factor)
                item.calculated_output_value = calculated_output_value

                item.remain_value -= calculated_output_value
                item.total_output_count += item.count
                for fee in fees:
                    fee['count'] = float(fee['count'])
                    fee['fee'] = float(fee['fee'])

                item.fees = fees

            if not factor.is_definite:
                DefiniteFactor.updateInventoryOnFactorItemSave(item, perform_revert=False)
            else:
                DefiniteFactor.updateInventoryOnFactorItemSave(item)

            item.save()

            prev_items[ware_id] = item

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
                account=getDefaultAccount(account).account,
                floatAccount=getDefaultAccount(account).floatAccount,
                costCenter=getDefaultAccount(account).costCenter,
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
                account=getDefaultAccount(account).account,
                floatAccount=getDefaultAccount(account).floatAccount,
                costCenter=getDefaultAccount(account).costCenter,
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
                account=getDefaultAccount('tax').account,
                floatAccount=getDefaultAccount('tax').floatAccount,
                costCenter=getDefaultAccount('tax').costCenter,
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
                account=getDefaultAccount('profitAndLossFromBuying').account,
                floatAccount=getDefaultAccount('profitAndLossFromBuying').floatAccount,
                costCenter=getDefaultAccount('profitAndLossFromBuying').costCenter,
                bed=bed,
                bes=bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )

    @staticmethod
    def updateInventoryOnFactorItemSave(factor_item, financial_year=None, perform_revert=True):
        from factors.models import Factor
        from factors.models import FactorItem

        if not financial_year:
            financial_year = get_current_user().active_financial_year

        ware = factor_item.ware
        warehouse = factor_item.warehouse

        if ware.isService:
            return

        factorItem = None
        if factor_item.id:
            factorItem = FactorItem.objects.get(pk=factor_item.id)

        if factor_item.factor.type in Factor.INPUT_GROUP:
            if factorItem and perform_revert:
                WareInventory.decrease_inventory(ware, warehouse, factorItem.count, financial_year, revert=True)
            WareInventory.increase_inventory(ware, warehouse, factor_item.count, factor_item.fee, financial_year)
        else:
            if factorItem and perform_revert:
                ware = factorItem.ware
                if ware.pricingType == Ware.FIFO:
                    fees = factorItem.fees.copy()
                    fees.reverse()
                    for fee in fees:
                        WareInventory.increase_inventory(ware, warehouse, fee['count'], fee['fee'], financial_year,
                                                         revert=True)

            WareInventory.decrease_inventory(ware, warehouse, factor_item.count, financial_year)

        next_financial_year = FinancialYear.objects.filter(start__gt=financial_year.start).order_by('start').first()
        if next_financial_year:
            next_year_first_period_inventory = Factor.get_first_period_inventory(next_financial_year)
            if next_year_first_period_inventory and Factor.objects.inFinancialYear(next_financial_year).filter(
                    code__gte=1).exists():
                count = ware.get_inventory_count(warehouse)
                has_changed = True
                for item in next_year_first_period_inventory.items.all():
                    if item.ware == ware and item.warehouse == warehouse and item.count == count:
                        has_changed = False
                        break

                if has_changed:
                    raise ValidationError("ابتدا فاکتور های سال مالی بعدی را پاک نمایید")
