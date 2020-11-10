from django.core.exceptions import ValidationError
from django.db.models.query import Prefetch

from rest_framework import generics, serializers
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.auth import BasicCRUDPermission
from helpers.functions import get_object_by_code
from helpers.views.confirm_view import ConfirmView
from sanads.models import clearSanad, Sanad
from transactions.models import Transaction, TransactionItem
from transactions.serializers import TransactionCreateUpdateSerializer, TransactionListRetrieveSerializer


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
        transaction = serializer.instance
        transaction.sync(user, data)
        transaction.updateSanad(user)

        return Response(TransactionListRetrieveSerializer(instance=transaction).data, status=status.HTTP_201_CREATED)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
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

        transaction.sync(user, data)
        transaction.updateSanad(user)

        return Response(TransactionListRetrieveSerializer(instance=transaction).data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset().prefetch_related(
            Prefetch('items', TransactionItem.objects.order_by('pk'))
        )
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
            ).prefetch_related(
                Prefetch('items', TransactionItem.objects.order_by('pk'))
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
