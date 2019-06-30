from django.db import connection
from django.db import transaction
from django.db.models import F
from django.db.models import Q, Sum
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.defaultAccounts.models import getDA
from factors.helpers import getInventoryCount
from sanads.sanads.models import clearSanad, newSanadCode, SanadItem
from .serializers import *


class ExpenseModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.inFinancialYear(self.request.user)

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
    serializer_class = FactorSerializer

    def get_queryset(self):
        return Factor.objects.inFinancialYear(self.request.user)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serialized = FactorListRetrieveSerializer(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serialized = FactorListRetrieveSerializer(instance)
        return Response(serialized.data)

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        queryset = self.get_queryset()
        factor = get_object_or_404(queryset, pk=pk)
        if not factor.is_deletable:
            raise ValidationError('فاکتور غیر قابل حذف می باشد')

        if factor.is_definite:
            DefiniteFactor.undoDefinition(request.user, factor)

        res = super().destroy(request, *args, **kwargs)
        return res

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        request.data['factor']['financial_year'] = request.user.active_financial_year.id

        data = request.data
        user = request.user

        serialized = FactorSerializer(data=data['factor'])
        serialized.is_valid(raise_exception=True)
        serialized.save()

        factor = serialized.instance
        self.sync_items(user, factor, data)
        self.sync_expenses(user, factor, data)

        res = Response(FactorListRetrieveSerializer(instance=factor).data, status=status.HTTP_200_OK)
        return res

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        factor = self.get_object()

        if not factor.is_editable:
            raise ValidationError('فاکتور غیر قابل ویرایش می باشد')

        data = request.data
        user = request.user

        serialized = FactorSerializer(instance=factor, data=data['factor'])
        serialized.is_valid(raise_exception=True)
        serialized.save()

        self.sync_items(user, factor, data)
        self.sync_expenses(user, factor, data)

        if factor.is_definite:
            DefiniteFactor.definiteFactor(user, factor.pk, perform_inventory_check=False)

        res = Response(FactorListRetrieveSerializer(instance=factor).data, status=status.HTTP_200_OK)
        return res

    def sync_items(self, user, factor, data):
        factor_items = data.get('factor_items', [])

        # Check Inventory
        if factor.is_definite:
            if factor.type in Factor.SALE_GROUP:
                check_inventory(user, factor_items['items'], consider_old_count=True)

        return self.mass(user, factor, FactorItemSerializer, factor_items)

    def sync_expenses(self, user, factor, data):
        return self.mass(user, factor, FactorExpenseSerializer, data.get('factor_expenses', None))

    def mass(self, user, factor, serializer_class, data):

        if not data:
            return

        model = serializer_class.Meta.model
        items_to_create = []
        items_to_update = []

        for item in data.get('items', []):
            item['financial_year'] = factor.financial_year.id
            if 'id' in item:
                items_to_update.append(item)
            else:
                items_to_create.append(item)

        for item in items_to_create:
            item['factor'] = factor.id

        serialized = serializer_class(data=items_to_create, many=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        for item in items_to_update:
            instance = get_object_or_404(model.objects.inFinancialYear(user), id=item['id'])
            if hasattr(instance, 'is_editable'):
                if not instance.is_editable:
                    continue
            serialized = serializer_class(instance, data=item)
            serialized.is_valid(raise_exception=True)
            serialized.save()

        ids_to_delete = data.get('ids_to_delete', [])
        for id in ids_to_delete:
            instance = get_object_or_404(model.objects.inFinancialYear(user), id=id)
            if hasattr(instance, 'is_editable'):
                if not instance.is_editable:
                    continue
            instance.delete()


class FactorPaymentMass(APIView):
    serializer_class = FactorPaymentSerializer

    def post(self, request):
        data = []
        for item in request.data:
            item['financial_year'] = request.user.active_financial_year.id
            data.append(item)
        serialized = self.serializer_class(data=data, many=True)
        if serialized.is_valid():
            serialized.save()
            self.updateFactorPaidValue(request.data)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        for item in request.data:
            instance = FactorPayment.objects.inFinancialYear(request.user).get(id=item['id'])
            if int(item['value']) == 0:
                instance.delete()
                continue
            serialized = self.serializer_class(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        self.updateFactorPaidValue(request.data, request.user)
        return Response([], status=status.HTTP_200_OK)

    def updateFactorPaidValue(self, items, user):
        factorIds = []
        for item in items:
            factorIds.append(item['factor'])
        factors = Factor.objects.inFinancialYear(user).filter(pk__in=factorIds)
        for factor in factors:
            paidValue = FactorPayment.objects.inFinancialYear(user).filter(factor=factor).aggregate(Sum('value'))['value__sum']
            factor.paidValue = paidValue
            factor.save()


@api_view(['get'])
def newCodesForFactor(request):
    res = Factor.newCodes(request.user)
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

    qs = Factor.objects.inFinancialYear(request.user)\
        .exclude(sanad__bed=0)\
        .filter(filters)\
        .distinct() \
        .prefetch_related('items') \
        .prefetch_related('payments') \
        .prefetch_related('account') \
        .prefetch_related('floatAccount')
    res = Response(NotPaidFactorsSerializer(qs, many=True).data)
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
    queryset = Factor.objects.inFinancialYear(request.user).filter(type=type)

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


class FirstPeriodInventoryView(APIView):
    def get(self, request):
        factor = Factor.getFirstPeriodInventory(request.user)
        if not factor:
            return Response({'message': 'no first period inventory'}, status=status.HTTP_200_OK)
        serialized = FactorListRetrieveSerializer(factor)
        return Response(serialized.data)

    @transaction.atomic
    def post(self, request):

        if Factor.objects.inFinancialYear(request.user).filter(type__in=Factor.SALE_GROUP).count():
            return Response({'non_field_errors': ['لطفا ابتدا فاکتور های فروش و برگشت از خرید را حذف کنید']},
                            status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['factor']['type'] = Factor.FIRST_PERIOD_INVENTORY
        data['factor']['code'] = 0
        data['factor']['is_definite'] = 1
        data['factor']['account'] = Account.get_partners_account(request.user).id
        data['factor']['financial_year'] = request.user.active_financial_year.id

        factor = Factor.getFirstPeriodInventory(request.user)
        if factor:
            serialized = FactorSerializer(instance=factor, data=data['factor'])
        else:
            serialized = FactorSerializer(data=data['factor'])
        if not serialized.is_valid():
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        serialized.save()
        factor = Factor.getFirstPeriodInventory(request.user)

        items_to_create = []
        items_to_update = []

        SerializerClass = FactorItemSerializer

        for item in data.get('items', []):
            item['financial_year'] = request.user.active_financial_year.id
            if 'id' in item:
                items_to_update.append(item)
            else:
                items_to_create.append(item)

        for item in items_to_create:
            item['factor'] = factor.id

        serialized = SerializerClass(data=items_to_create, many=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        for item in items_to_update:
            instance = FactorItem.objects.inFinancialYear(request.user).get(id=item['id'])
            serialized = SerializerClass(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        ids_to_delete = data.get('ids_to_delete', [])
        if len(ids_to_delete):
            FactorItem.objects.inFinancialYear(request.user).filter(id__in=ids_to_delete).delete()

        for item in factor.items.all():
            item.total_input_count = item.count
            item.remain_value = item.value
            item.save()

        sanad = Sanad(code=newSanadCode(request.user), date=factor.date, explanation=factor.explanation,
                      createType=Sanad.AUTO, financial_year=request.user.active_financial_year)
        sanad.save()
        factor.sanad = sanad
        factor.save()

        if sanad.items.count():
            clearSanad(sanad)

        sanad.items.create(
            account=Account.get_inventory_account(request.user),
            value=factor.sum,
            valueType='bed',
            financial_year=request.user.active_financial_year
        )
        sanad.items.create(
            account=Account.get_partners_account(request.user),
            value=factor.sum,
            valueType='bes',
            financial_year=request.user.active_financial_year
        )

        res = Response(FactorSerializer(instance=factor).data, status=status.HTTP_200_OK)
        return res


# Check Inventory
def check_inventory(user, factor_items, consider_old_count):

    inventories = []
    for item in factor_items:
        if type(item) is FactorItem:
            ware = item.ware
            warehouse = item.warehouse
            old_count = item.count
        else:
            ware = Ware.objects.inFinancialYear(user).get(pk=item['ware'])
            warehouse = Warehouse.objects.inFinancialYear(user).get(pk=item['warehouse'])
            if 'id' in item:
                old_count = FactorItem.objects.inFinancialYear(user).get(pk=item['id']).count
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
            count = int(item.count)
        else:
            ware = Ware.objects.inFinancialYear(user).get(pk=item['ware'])
            warehouse = Warehouse.objects.inFinancialYear(user).get(pk=item['warehouse'])
            count = int(item['count'])

        for inventory in inventories:
            if inventory['ware'] == ware and inventory['warehouse'] == warehouse:
                inventory['remain'] -= count

            if inventory['remain'] < 0:
                raise ValidationError("موجودی انبار برای کالای {} کافی نیست.".format(inventory['ware']))


class DefiniteFactor(APIView):

    def post(self, request, pk):
        user = request.user
        factor = DefiniteFactor.definiteFactor(user, pk)
        return Response(FactorListRetrieveSerializer(factor).data)

    @staticmethod
    @transaction.atomic()
    def definiteFactor(user, pk, perform_inventory_check=True):
        factor = get_object_or_404(Factor.objects.inFinancialYear(user), pk=pk)

        # Check Inventory
        if perform_inventory_check:
            if factor.type in Factor.SALE_GROUP:
                check_inventory(user, factor.items.all(), consider_old_count=False)

        sanad = DefiniteFactor.getFactorSanad(user, factor)
        factor.sanad = sanad

        DefiniteFactor.setFactorItemsRemains(user, factor)

        if factor.type in Factor.SALE_GROUP:
            rowTypeOne = SanadItem.BED
            rowTypeTwo = SanadItem.BES
            if factor.type == Factor.SALE:
                account = 'sale'
            else:
                account = 'backFromBuy'
        else:
            rowTypeOne = SanadItem.BES
            rowTypeTwo = SanadItem.BED
            if factor.type == Factor.BUY:
                account = 'buy'
            else:
                account = 'backFromSale'

        code = Factor.newCodes(user, factor_type=factor.type)

        explanation = "فاکتور {} شماره {} به تاریخ {} {} مشتری".format(
            factor.type_label,
            code,
            str(factor.date),
            "از" if factor.type in Factor.BUY_GROUP else "به"
        )

        if factor.type != Factor.BACK_FROM_BUY:
            DefiniteFactor.submitSumSanadItems(user, factor, rowTypeOne, rowTypeTwo, account, explanation)

        if factor.type == Factor.SALE:
            DefiniteFactor.submitSaleSanadItems(user, factor, explanation)
        elif factor.type == Factor.BACK_FROM_SALE:
            DefiniteFactor.submitBackFromSaleSanadItems(user, factor, explanation)
        elif factor.type == Factor.BACK_FROM_BUY:
            DefiniteFactor.submitBackFromBuySanadItems(user, factor, explanation)

        DefiniteFactor.submitDiscountSanadItems(user, factor, rowTypeOne, rowTypeTwo, account, explanation)
        DefiniteFactor.submitTaxSanadItems(user, factor, rowTypeOne, rowTypeTwo, explanation)
        DefiniteFactor.submitExpenseSanadItems(factor, explanation)

        factor.is_definite = True
        factor.code = code
        factor.definition_date = now()
        factor.sanad = sanad
        factor.save()

        return factor

    @staticmethod
    def getFactorSanad(user, factor):
        if not factor.sanad:
            sanad = Sanad(
                code=newSanadCode(user),
                date=factor.date,
                createType=Sanad.AUTO,
                type=Sanad.TEMPORARY,
                explanation=factor.explanation,
                financial_year=user.active_financial_year
            )
        else:
            factor = DefiniteFactor.undoDefinition(user, factor)
            sanad = factor.sanad
            sanad.date = factor.date
            sanad.createType = Sanad.AUTO
            sanad.type = Sanad.TEMPORARY
            sanad.explanation = factor.explanation
        sanad.save()

        return sanad

    @staticmethod
    def undoDefinition(user, factor):
        sanad = factor.sanad
        clearSanad(sanad)

        factor.is_definite = False
        factor.definition_date = None
        factor.save()

        if factor.type in Factor.SALE_GROUP:
            for item in factor.items.all():
                if item.ware.pricingType == Ware.FIFO:
                    item.ware.revert_fifo(user, item.count)

        return factor

    @staticmethod
    def setFactorItemsRemains(user, factor):
        prev_items = {}
        for item in factor.items.order_by('id').all():

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
            else:
                calculated_output_value = item.ware.calculated_output_value(user, item.count, last_definite_factor)
                item.calculated_output_value = calculated_output_value

                item.remain_value -= calculated_output_value
                item.total_output_count += item.count

            item.save()

            prev_items[ware_id] = item

    @staticmethod
    def submitSumSanadItems(user, factor, rowTypeOne, rowTypeTwo, account, explanation):
        sanad = factor.sanad
        if factor.sum:
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                value=factor.sum,
                valueType=rowTypeOne,
                explanation=explanation,
                financial_year=sanad.financial_year
            )
            sanad.items.create(
                account=getDA(account, user).account,
                # floatAccount=factor.floatAccount,
                value=factor.sum,
                valueType=rowTypeTwo,
                explanation=explanation,
                financial_year=sanad.financial_year
            )

    @staticmethod
    def submitDiscountSanadItems(user, factor, rowTypeOne, rowTypeTwo, account, explanation):
        sanad = factor.sanad
        if factor.discountSum:
            sanad.items.create(
                account=getDA(account, user).account,
                # floatAccount=factor.floatAccount,
                value=factor.discountSum,
                valueType=rowTypeOne,
                explanation=explanation,
                financial_year=sanad.financial_year
            )
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                value=factor.discountSum,
                valueType=rowTypeTwo,
                explanation=explanation,
                financial_year=sanad.financial_year
            )

    @staticmethod
    def submitTaxSanadItems(user, factor, rowTypeOne, rowTypeTwo, explanation):
        sanad = factor.sanad
        # Factor Tax Sum
        if factor.taxSum:
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                value=factor.taxSum,
                valueType=rowTypeOne,
                explanation=explanation,
                financial_year=sanad.financial_year
            )
            sanad.items.create(
                account=getDA('tax', user).account,
                # floatAccount=factor.floatAccount,
                value=factor.taxSum,
                valueType=rowTypeTwo,
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
                    # floatAccount=factor.floatAccount,
                    value=e.value,
                    valueType='bed',
                    explanation=explanation,
                    financial_year=sanad.financial_year
                )
                sanad.items.create(
                    account=e.account,
                    floatAccount=e.floatAccount,
                    value=e.value,
                    valueType='bes',
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
            # floatAccount=factor.floatAccount,
            value=value,
            valueType=SanadItem.BED,
            explanation=explanation,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            account=Account.get_inventory_account(user),
            # floatAccount=factor.floatAccount,
            value=value,
            valueType=SanadItem.BES,
            explanation=explanation,
            financial_year=sanad.financial_year
        )

    @staticmethod
    def submitBackFromSaleSanadItems(user, factor, explanation):
        sanad = factor.sanad
        value = 0
        # for item in factor.items.all():
        #     value += item.calculated_output_value

        for item in factor.items.all():
            calculated_output_value = item.ware.calculated_output_value(user, item.count)
            value += calculated_output_value

        sanad.items.create(
            account=Account.get_inventory_account(user),
            # floatAccount=factor.floatAccount,
            value=value,
            valueType=SanadItem.BED,
            explanation=explanation,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            account=Account.get_cost_of_sold_wares_account(user),
            # floatAccount=factor.floatAccount,
            value=value,
            valueType=SanadItem.BES,
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
            value=factor.sum,
            valueType=SanadItem.BED,
            explanation=explanation,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            account=Account.get_inventory_account(user),
            # floatAccount=factor.floatAccount,
            value=value,
            valueType=SanadItem.BES,
            explanation=explanation,
            financial_year=sanad.financial_year
        )

        profit_and_loss_value = value - factor.sum
        if profit_and_loss_value:
            if profit_and_loss_value > 0:
                value_type = SanadItem.BED
            else:
                profit_and_loss_value = abs(profit_and_loss_value)
                value_type = SanadItem.BES
            sanad.items.create(
                account=getDA('profitAndLossFromBuying', user).account,
                # floatAccount=factor.floatAccount,
                value=profit_and_loss_value,
                valueType=value_type,
                explanation=explanation,
                financial_year=sanad.financial_year
            )


class TransferModelView(viewsets.ModelViewSet):
    serializer_class = TransferListRetrieveSerializer

    def get_queryset(self):
        return Transfer.objects.inFinancialYear(self.request.user)

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
            ware = Ware.objects.inFinancialYear(user).get(pk=item['ware'])
            warehouse = Warehouse.objects.inFinancialYear(user).get(pk=item['output_warehouse'])
            if 'id' in item:
                old_count = FactorItem.objects.inFinancialYear(user).get(pk=item['id']).count
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
    queryset = Transfer.objects.inFinancialYear(request.user)

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

