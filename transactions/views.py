from django.core.exceptions import ValidationError
from django.db.models import Q, F

from rest_framework import generics, serializers
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.defaultAccounts.models import DefaultAccount
from factors.models import Factor
from factors.serializers import FactorListRetrieveSerializer
from helpers.auth import BasicCRUDPermission, DefinedItemUDPermission
from helpers.functions import get_object_by_code, get_object_accounts
from helpers.views.confirm_view import ConfirmView
from sanads.models import clearSanad, Sanad
from transactions.models import Transaction, TransactionItem
from transactions.serializers import TransactionCreateUpdateSerializer, TransactionListRetrieveSerializer, \
    TransactionFactorListSerializer, Sum


def get_transaction_permission_basename(transaction_type):
    if transaction_type == Transaction.RECEIVE:
        return "receiveTransaction"
    else:
        return "paymentTransaction"


class TransactionCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    serializer_class = TransactionCreateUpdateSerializer

    @property
    def permission_basename(self):
        return get_transaction_permission_basename(self.request.data.get('type'))

    def get_queryset(self):
        return Transaction.objects.hasAccess(self.request.method, self.permission_basename)

    def create(self, request, *args, **kwargs):
        user = request.user

        data = request.data
        transaction_data = data.get('item')

        sanad = Sanad.objects.inFinancialYear().filter(code=transaction_data.get('sanad_code')).first()

        if sanad and not sanad.isEmpty:
            raise ValidationError("سند باید خالی باشد")

        serializer = TransactionCreateUpdateSerializer(data=transaction_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            code=Transaction.newCodes(transaction_data.get('type')),
            sanad=sanad
        )

        serializer.instance.sync(user, data)

        return Response(
            TransactionListRetrieveSerializer(instance=serializer.instance).data,
            status=status.HTTP_201_CREATED
        )


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission, DefinedItemUDPermission)
    serializer_class = TransactionCreateUpdateSerializer

    @property
    def permission_basename(self):
        return get_transaction_permission_basename(get_object_or_404(Transaction, pk=self.kwargs['pk']).type)

    def get_queryset(self):
        return Transaction.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):

        transaction = self.get_object()
        user = request.user

        data = request.data
        transaction_data = data.get('item')

        serializer = TransactionCreateUpdateSerializer(instance=transaction, data=transaction_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        instance = serializer.instance
        instance.sync(user, data)

        if instance.is_defined:
            instance.updateSanad(user)

        return Response(TransactionListRetrieveSerializer(instance=transaction).data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        transaction = get_object_or_404(queryset, pk=pk)
        serializer = TransactionListRetrieveSerializer(transaction)
        return Response(serializer.data)

    def delete(self, request, **kwargs):
        transaction = self.get_object()
        for item in transaction.items.all():
            if item.cheque:
                raise serializers.ValidationError("ابتدا چک ها را حذف کنید")
        transaction.delete()
        clearSanad(transaction.sanad)
        return Response()


class TransactionByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)

    @property
    def permission_basename(self):
        return get_transaction_permission_basename(self.request.GET.get('type'))

    def get(self, request):
        item = get_object_by_code(
            Transaction.objects.hasAccess(request.method, self.permission_basename).filter(
                type=request.GET.get('type')
            ),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(TransactionListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class ConfirmTransaction(ConfirmView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    model = Transaction

    @property
    def permission_codename(self):
        instance = self.get_object()
        return get_transaction_permission_basename(instance.type)


class TransactionFactorsListView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_basename(self):

        transaction_type = self.request.GET.get('transaction_type')
        if transaction_type == Transaction.RECEIVE:
            return 'notReceivedFactor'
        else:
            return 'notPaidFactor'

    def get(self, request):
        data = request.GET

        account_id = data.get('account_id')
        floatAccount_id = data.get('floatAccount_id')
        costCenter_id = data.get('costCenter_id')
        transaction_type = data.get('transaction_type')
        transaction_id = data.get('transaction_id')  # optional, others are required

        qs = Factor.objects.filter(
            account_id=account_id,
            floatAccount_id=floatAccount_id,
            costCenter_id=costCenter_id
        )

        if transaction_type == Transaction.PAYMENT:
            qs = qs.filter(type__in=Factor.BUY_GROUP)
        else:
            qs = qs.filter(type__in=Factor.SALE_GROUP)

        if transaction_id:
            qs = qs.filter(
                Q(
                    Q(payments=None) | Q(payments__transaction_id=transaction_id)
                )
            )
        else:
            qs = qs.filter(~Q(paidValue=F('total_sum')))

        return Response(
            TransactionFactorListSerializer(
                qs,
                many=True,
                context={'transaction_id': transaction_id}
            ).data
        )


class QuickFactorTransaction(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        factor = get_object_or_404(Factor, pk=data.get('factor_id'))
        value = factor.total_sum - factor.paidValue

        if factor.type in Factor.BUY_GROUP:
            transaction_type = Transaction.PAYMENT
        else:
            transaction_type = Transaction.RECEIVE

        codename = data.get('default_account_codename')

        default_account = DefaultAccount.get(codename)

        transaction = Transaction.objects.create(
            financial_year=user.active_financial_year,
            type=transaction_type,
            code=Transaction.newCodes(transaction_type),
            date=factor.date,
            **get_object_accounts(factor)
        )
        transaction.items.create(
            financial_year=transaction.financial_year,
            type=default_account,
            **get_object_accounts(default_account),
            date=factor.date,
            value=value
        )
        transaction.factorPayments.create(
            financial_year=transaction.financial_year,
            factor=factor,
            value=value
        )
        transaction.updateSanad(user)

        factor.paidValue += value
        factor.save()

        return Response(FactorListRetrieveSerializer(instance=factor).data, status=status.HTTP_200_OK)


class DefineTransactionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    serializer_class = TransactionListRetrieveSerializer

    @property
    def permission_codename(self):
        return 'define.{}'.format(get_transaction_permission_basename(self.item.type))

    @property
    def item(self):
        data = self.request.data
        return get_object_or_404(
            self.serializer_class.Meta.model,
            pk=data.get('item')
        )

    def post(self, request):
        user = request.user

        if not self.item.is_defined:
            self.item.updateSanad(user)
            self.item.define()

        return Response(self.serializer_class(instance=self.item).data)
