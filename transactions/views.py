from django.core.exceptions import ValidationError

from rest_framework import generics, serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.auth import BasicCRUDPermission
from sanads.models import clearSanad, Sanad
from transactions.models import Transaction
from transactions.serializers import TransactionCreateUpdateSerializer, TransactionListRetrieveSerializer


def get_transaction_permission_base_codename(transaction_type):
    if transaction_type == Transaction.RECEIVE:
        return "receiveTransaction"
    else:
        return "paymentTransaction"


class TransactionCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    serializer_class = TransactionCreateUpdateSerializer

    @property
    def permission_base_codename(self):
        return get_transaction_permission_base_codename(self.request.data.get('type'))

    def get_queryset(self):
        return Transaction.objects.inFinancialYear()

    def create(self, request, *args, **kwargs):
        user = request.user

        data = request.data
        transaction_data = data.get('transaction')

        sanad = Sanad.objects.inFinancialYear().filter(code=transaction_data.get('sanad_code')).first()

        if sanad and not sanad.isEmpty:
            raise ValidationError("سند باید خالی باشد")

        serializer = TransactionCreateUpdateSerializer(data=transaction_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            code=Transaction.newCodes(request.user, transaction_data.get('type')),
            sanad=sanad
        )
        transaction = serializer.instance
        transaction.sync(user, data)
        transaction.updateSanad(user)

        return Response(TransactionListRetrieveSerializer(instance=transaction).data, status=status.HTTP_201_CREATED)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    serializer_class = TransactionCreateUpdateSerializer

    @property
    def permission_base_codename(self):
        return get_transaction_permission_base_codename(self.get_object().type)

    def get_queryset(self):
        return Transaction.objects.inFinancialYear()

    def update(self, request, *args, **kwargs):

        transaction = self.get_object()
        user = request.user

        data = request.data
        transaction_data = data.get('transaction')

        serializer = TransactionCreateUpdateSerializer(instance=transaction, data=transaction_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        transaction.sync(user, data)
        transaction.updateSanad(user)

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


@api_view(['get'])
def newCodeForTransaction(request):
    codes = Transaction.newCodes(request.user)
    return Response(codes)


class GetTransactionByCodeView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    serializer_class = TransactionCreateUpdateSerializer

    @property
    def permission_base_codename(self):
        return get_transaction_permission_base_codename(self.request.GET.get('type'))

    def get(self, request):
        if 'code' not in request.GET:
            return Response(['کد وارد نشده است'], status.HTTP_400_BAD_REQUEST)
        if 'type' not in request.GET:
            return Response(['نوع وارد نشده است'], status.HTTP_400_BAD_REQUEST)

        code = request.GET['code']
        type = request.GET['type']
        queryset = Transaction.objects.inFinancialYear().all()
        transaction = get_object_or_404(queryset, code=code, type=type)
        serializer = TransactionListRetrieveSerializer(transaction)
        return Response(serializer.data)
