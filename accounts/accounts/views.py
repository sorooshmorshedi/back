from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.accounts.serializers import *
from helpers.auth import BasicCRUDPermission


@method_decorator(csrf_exempt, name='dispatch')
class FloatAccountListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountSerializer

    def get_queryset(self):
        return FloatAccount.objects.inFinancialYear(self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class FloatAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountSerializer

    def get_queryset(self):
        return FloatAccount.objects.inFinancialYear(self.request.user)


class FloatAccountGroupListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountGroupSerializer

    def get_queryset(self):
        return FloatAccountGroup.objects.inFinancialYear(self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class FloatAccountGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountGroupSerializer

    def get_queryset(self):
        return FloatAccountGroup.objects.inFinancialYear(self.request.user)


class IndependentAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = IndependentAccountSerializer

    def get_queryset(self):
        return IndependentAccount.objects.inFinancialYear(self.request.user)


class IndependentAccountListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = IndependentAccountSerializer

    def get_queryset(self):
        return IndependentAccount.objects.inFinancialYear(self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class AccountTypeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


class AccountListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super(AccountListCreate, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Account.objects.inFinancialYear(self.request.user)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        queryset = AccountListRetrieveSerializer.setup_eager_loading(queryset)
        serializer = AccountListRetrieveSerializer(queryset, many=True)
        res = Response(serializer.data)
        return res


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = AccountSerializer

    def retrieve(self, request, pk=None):
        queryset = Account.objects.inFinancialYear(request.user)
        account = get_object_or_404(queryset, pk=pk)
        serializer = AccountListRetrieveSerializer(account)
        return Response(serializer.data)

    def destroy(self, request, pk, *args, **kwargs):
        account = get_object_or_404(Account.objects.inFinancialYear(request.user), pk=pk)
        if account.can_delete():
            return super().destroy(self, request, *args, **kwargs)

        return Response(['حساب های دارای گردش در سال مالی جاری غیر قابل حذف می باشند'],
                        status=status.HTTP_400_BAD_REQUEST)


class PersonListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = PersonSerializer

    def get_queryset(self):
        return Person.objects.inFinancialYear(self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = PersonSerializer

    def get_queryset(self):
        return Person.objects.inFinancialYear(self.request.user)


class BankListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = BankSerializer

    def get_queryset(self):
        return Bank.objects.inFinancialYear(self.request.user)


class BankDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = BankSerializer

    def get_queryset(self):
        return Bank.objects.inFinancialYear(self.request.user)


@api_view(['get'])
def getAccountRemain(request, pk):
    account = get_object_or_404(Account.objects.inFinancialYear(request.user), pk=pk)
    return Response(account.get_remain(), status=status.HTTP_200_OK)

