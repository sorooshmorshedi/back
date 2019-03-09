from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from accounts.accounts.models import *
from accounts.accounts.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class FloatAccountListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, AccountListCreate,)
    queryset = FloatAccount.objects.all()
    serializer_class = FloatAccountSerializer


class FloatAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, AccountListDetail,)
    queryset = FloatAccount.objects.all()
    serializer_class = FloatAccountSerializer


class FloatAccountGroupListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, AccountListCreate,)
    queryset = FloatAccountGroup.objects.all()
    serializer_class = FloatAccountGroupSerializer


class FloatAccountGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, AccountListDetail,)
    queryset = FloatAccountGroup.objects.all()
    serializer_class = FloatAccountGroupSerializer


class IndependentAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, AccountListDetail,)
    queryset = IndependentAccount.objects.all()
    serializer_class = IndependentAccountSerializer


class IndependentAccountListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, AccountListCreate,)
    queryset = IndependentAccount.objects.all()
    serializer_class = IndependentAccountSerializer


# ChangeIt to list
class AccountTypeListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, AccountListCreate,)
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


class AccountListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, AccountListCreate,)
    queryset = Account.objects.order_by('code')
    serializer_class = AccountSerializer

    def list(self, request, *ergs, **kwargs):
        # queryset = Account.objects.filter(level=0)
        queryset = Account.objects.filter()
        serializer = AccountListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, AccountListDetail,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def retrieve(self, request, pk=None):
        queryset = Account.objects.all()
        account = get_object_or_404(queryset, pk=pk)
        serializer = AccountListRetrieveSerializer(account)
        return Response(serializer.data)

    def destroy(self, request, pk, *args, **kwargs):
        account = get_object_or_404(Account, pk=pk)
        if account.can_delete():
            return super().destroy(self, request, *args, **kwargs)

        return Response(['حساب های دارای گردش در سال مالی جاری غیر قابل حذف می باشند'],
                        status=status.HTTP_400_BAD_REQUEST)


class PersonListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, AccountListCreate,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, AccountListDetail,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class BankListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, AccountListCreate,)
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class BankDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, AccountListDetail,)
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
