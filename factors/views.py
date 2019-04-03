from django.db import connection
from django.db import transaction
from django.db.models import F
from django.db.models import Q, Sum
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.defaultAccounts.models import getDA
from sanads.sanads.models import clearSanad
from .serializers import *


class ExpenseModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = Expense.objects.all()
        serialized = ExpenseListRetrieveSerializer(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = Expense.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serialized = ExpenseListRetrieveSerializer(instance)
        return Response(serialized.data)


class FactorModelView(viewsets.ModelViewSet):
    queryset = Factor.objects.all()
    serializer_class = FactorSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = Factor.objects.all()
        serialized = FactorListRetrieveSerializer(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = Factor.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serialized = FactorListRetrieveSerializer(instance)
        return Response(serialized.data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        factor = get_object_or_404(Factor, pk=pk)
        clearSanad(factor.sanad)
        res = super().destroy(request, *args, **kwargs)
        return res


class FactorItemMass(APIView):
    serializer_class = FactorItemSerializer

    def post(self, request):
        serialized = self.serializer_class(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        for item in request.data:
            instance = FactorItem.objects.get(id=item['id'])
            serialized = FactorItemSerializer(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request):
        for itemId in request.data:
            instance = FactorItem.objects.get(id=itemId)
            instance.delete()
        return Response([], status=status.HTTP_200_OK)


class FactorExpenseMass(APIView):
    serializer_class = FactorExpenseListRetrieveSerializer
    model = FactorExpense

    def post(self, request):
        serialized = FactorExpenseSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        for item in request.data:
            instance = self.model.objects.get(id=item['id'])
            serialized = self.serializer_class(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request):
        for itemId in request.data:
            instance = self.model.objects.get(id=itemId)
            instance.delete()
        return Response([], status=status.HTTP_200_OK)


class FactorSanadAndReceiptUpdate(APIView):
    def put(self, request, pk):
        queryset = Factor.objects.all()
        factor = get_object_or_404(queryset, pk=pk)
        sanad = factor.sanad
        clearSanad(sanad)

        sanad.explanation = factor.explanation
        sanad.date = factor.date
        sanad.type = 'temporary'
        sanad.createType = 'auto'
        sanad.save()

        if factor.type in ('sale', 'backFromBuy'):
            rowTypeOne = 'bed'
            rowTypeTwo = 'bes'
            if factor.type == 'sale':
                account = 'sale'
            else:
                account = 'backFromBuy'
        else:
            rowTypeOne = 'bes'
            rowTypeTwo = 'bed'
            if factor.type == 'buy':
                account = 'buy'
            else:
                account = 'backFromSale'

        explanation = "شماره فاکتور: {} تاریخ فاکتور: {} {}".format(factor.code, str(factor.date), factor.explanation)

        # Factor Sum
        if factor.sum:
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                value=factor.sum,
                valueType=rowTypeOne,
                explanation=explanation
            )
            sanad.items.create(
                account=getDA(account).account,
                # floatAccount=factor.floatAccount,
                value=factor.sum,
                valueType=rowTypeTwo,
                explanation=explanation
            )

        # Factor Discount Sum
        if factor.discountSum:
            sanad.items.create(
                account=getDA(account).account,
                # floatAccount=factor.floatAccount,
                value=factor.discountSum,
                valueType=rowTypeOne,
                explanation=explanation
            )
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                value=factor.discountSum,
                valueType=rowTypeTwo,
                explanation=explanation
            )

        # Factor Tax Sum
        if factor.taxSum:
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                value=factor.taxSum,
                valueType=rowTypeOne,
                explanation=explanation
            )
            sanad.items.create(
                account=getDA('tax').account,
                # floatAccount=factor.floatAccount,
                value=factor.taxSum,
                valueType=rowTypeTwo,
                explanation=explanation
            )

        # Factor Expenses
        for e in factor.expenses.all():
            if e.value:
                sanad.items.create(
                    account=e.expense.account,
                    # floatAccount=factor.floatAccount,
                    value=e.value,
                    valueType='bed',
                    explanation=explanation
                )
                sanad.items.create(
                    account=e.account,
                    floatAccount=e.floatAccount,
                    value=e.value,
                    valueType='bes',
                    explanation=explanation
                )

        # Receipt
        # receipt = factor.receipt
        # clearReceipt(receipt)
        #
        # for item in factor.items.all():
        #     receipt.items.create(
        #         ware=item.ware,
        #         warehouse=item.warehouse,
        #         count=item.count

        return Response([])


class ReceiptModelView(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = Receipt.objects.all()
        serialized = ReceiptListRetrieveSerializer(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = Receipt.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serialized = ReceiptListRetrieveSerializer(instance)
        return Response(serialized.data)


class ReceiptItemMass(APIView):
    serializer_class = ReceiptItemSerializer

    def post(self, request):
        serialized = self.serializer_class(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        for item in request.data:
            instance = ReceiptItem.objects.get(id=item['id'])
            serialized = ReceiptItemSerializer(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request):
        for itemId in request.data:
            instance = ReceiptItem.objects.get(id=itemId)
            instance.delete()
        return Response([], status=status.HTTP_200_OK)


class FactorPaymentMass(APIView):
    serializer_class = FactorPaymentSerializer

    def post(self, request):
        serialized = self.serializer_class(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            self.updateFactorPaidValue(request.data)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        for item in request.data:
            instance = FactorPayment.objects.get(id=item['id'])
            if int(item['value']) == 0:
                instance.delete()
                continue
            serialized = self.serializer_class(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        self.updateFactorPaidValue(request.data)
        return Response([], status=status.HTTP_200_OK)

    def updateFactorPaidValue(self, items):
        factorIds = []
        for item in items:
            factorIds.append(item['factor'])
        factors = Factor.objects.filter(pk__in=factorIds)
        for factor in factors:
            paidValue = FactorPayment.objects.filter(factor=factor).aggregate(Sum('value'))['value__sum']
            factor.paidValue = paidValue
            factor.save()


@api_view(['get'])
def newCodesForFactor(request):
    res = {}
    types = ['buy', 'sale', 'backFromBuy', 'backFromSale']
    for t in types:
        try:
            res[t] = Factor.objects.filter(type=t).latest('code').code + 1
        except:
            res[t] = 1
    return Response(res)


@api_view(['get'])
def newCodesForReceipt(request):
    res = {}
    types = ['receipt', 'remittance']
    for t in types:
        try:
            res[t] = Receipt.objects.filter(type=t).latest('code').code + 1
        except:
            res[t] = 1
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

    qs = Factor.objects\
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
def getFactorByCode(request):
    if 'code' not in request.GET:
        return Response(['کد وارد نشده است'], status.HTTP_400_BAD_REQUEST)
    if 'type' not in request.GET:
        return Response(['نوع وارد نشده است'], status.HTTP_400_BAD_REQUEST)

    code = request.GET['code']
    type = request.GET['type']
    queryset = Factor.objects.all()
    factor = get_object_or_404(queryset, code=code, type=type)
    serializer = FactorListRetrieveSerializer(factor)
    return Response(serializer.data)


class FirstPeriodInventoryView(APIView):
    def get(self, request):
        factor = Factor.getFirstPeriodInventory()
        if not factor:
            return Response({'message': 'no first period inventory'}, status=status.HTTP_200_OK)
        serialized = FactorListRetrieveSerializer(factor)
        return Response(serialized.data)

    @transaction.atomic
    def post(self, request):
        data = request.data
        data['factor']['type'] = Factor.FIRST_PERIOD_INVENTORY
        data['factor']['code'] = 0
        data['factor']['account'] = Account.get_partners_account().id

        factor = Factor.getFirstPeriodInventory()
        if factor:
            serialized = FactorSerializer(instance=factor, data=data['factor'])
        else:
            serialized = FactorSerializer(data=data['factor'])
        if not serialized.is_valid():
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        serialized.save()
        factor = serialized.instance

        items_to_create = []
        items_to_update = []

        SerializerClass = FactorItemSerializer

        for item in data.get('items', []):
            if 'id' in item:
                items_to_update.append(item)
            else:
                items_to_create.append(item)

        for item in items_to_create:
            item['factor'] = factor.id

        serialized = SerializerClass(data=items_to_create, many=True)
        if serialized.is_valid():
            serialized.save()
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        for item in items_to_update:
            instance = FactorItem.objects.get(id=item['id'])
            serialized = SerializerClass(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        ids_to_delete = data.get('ids_to_delete', [])
        if len(ids_to_delete):
            FactorItem.objects.filter(id__in=ids_to_delete).delete()

        sanad = factor.sanad
        sanad.explanation = factor.explanation
        sanad.date = factor.date
        sanad.type = 'temporary'
        sanad.createType = 'auto'
        sanad.save()

        if sanad.items.count():
            clearSanad(sanad)

        sanad.items.create(
            account=Account.get_inventory_account(),
            value=factor.sum,
            valueType='bed',
        )
        sanad.items.create(
            account=Account.get_partners_account(),
            value=factor.sum,
            valueType='bes',
        )

        res = Response(FactorSerializer(instance=factor).data, status=status.HTTP_200_OK)
        return res




