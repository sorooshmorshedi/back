from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from sanads.sanads.models import clearSanad, Sanad
from sanads.transactions.models import Transaction
from sanads.transactions.serializers import TransactionCreateUpdateSerializer, TransactionListRetrieveSerializer


@method_decorator(csrf_exempt, name='dispatch')
class TransactionListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    serializer_class = TransactionCreateUpdateSerializer

    def get_queryset(self):
        return Transaction.objects.inFinancialYear(self.request.user)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = TransactionListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user

        data = request.data
        transaction_data = data.get('transaction')

        sanad = Sanad.objects.inFinancialYear(user).filter(code=transaction_data.get('sanad_code')).first()

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

        # raise serializers.ValidationError("haa")

        return Response(TransactionListRetrieveSerializer(instance=transaction).data, status=status.HTTP_201_CREATED)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    serializer_class = TransactionCreateUpdateSerializer

    def get_queryset(self):
        return Transaction.objects.inFinancialYear(self.request.user)

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


@api_view(['get'])
def getTransactionByCode(request):
    if 'code' not in request.GET:
        return Response(['کد وارد نشده است'], status.HTTP_400_BAD_REQUEST)
    if 'type' not in request.GET:
        return Response(['نوع وارد نشده است'], status.HTTP_400_BAD_REQUEST)

    code = request.GET['code']
    type = request.GET['type']
    queryset = Transaction.objects.inFinancialYear(request.user).all()
    transaction = get_object_or_404(queryset, code=code, type=type)
    serializer = TransactionListRetrieveSerializer(transaction)
    return Response(serializer.data)
