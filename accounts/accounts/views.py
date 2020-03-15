from django.db.models import Prefetch
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.accounts.models import FloatAccountRelation
from accounts.accounts.serializers import *
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_current_user
from helpers.views.RetrieveUpdateDestroyAPIViewWithAutoFinancialYear import \
    RetrieveUpdateDestroyAPIViewWithAutoFinancialYear
from helpers.views.ListCreateAPIViewWithAutoFinancialYear import ListCreateAPIViewWithAutoFinancialYear


class FloatAccountListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountSerializer

    def created(self, instance, request):
        syncFloatAccountGroups = request.data.pop('syncFloatAccountGroups', [])
        financial_year = request.user.active_financial_year
        for floatAccountGroup in syncFloatAccountGroups:
            relation = FloatAccountRelation.objects.create(
                floatAccount=instance,
                floatAccountGroup=FloatAccountGroup.objects.get(pk=floatAccountGroup)
            )
            financial_year.floatAccountRelations.add(relation)
        return instance


class FloatAccountDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountSerializer

    def get_queryset(self):
        user = self.request.user
        financial_year = user.active_financial_year
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch('floatAccountGroups',
                     queryset=FloatAccountGroup.objects.inFinancialYear()
                     .filter(relation__financial_year=financial_year)
                     .distinct()
                     )
        )
        return queryset

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        syncFloatAccountGroups = request.data.get('syncFloatAccountGroups', [])
        instance = self.get_object()
        FloatAccountRelation.objects.inFinancialYear().filter(floatAccount=instance).delete()
        financial_year = request.user.active_financial_year
        for floatAccountGroup in syncFloatAccountGroups:
            relation = FloatAccountRelation.objects.create(
                floatAccount=instance,
                floatAccountGroup=FloatAccountGroup.objects.get(pk=floatAccountGroup)
            )
            financial_year.floatAccountRelations.add(relation)
        return res


class FloatAccountGroupListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountGroupSerializer

    def get_queryset(self):
        user = self.request.user
        financial_year = user.active_financial_year
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch('floatAccounts',
                     queryset=FloatAccount.objects.inFinancialYear()
                     .filter(relation__financial_year=financial_year)
                     .distinct()
                     )
        )
        return queryset


class FloatAccountGroupDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountGroupSerializer


class AccountTypeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


class AccountListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = AccountCreateUpdateSerializer

    def perform_create(self, serializer):

        parent = serializer.validated_data.get('parent')
        account_type = serializer.validated_data.get('account_type')
        if parent:
            code = parent.get_new_child_code()
            level = parent.level + 1
        else:
            parent_code = None
            if account_type == Account.BANK:
                parent_code = "10101"
            elif account_type == Account.PERSON:
                person_type = serializer.validated_data.get('person_type')
                is_real = serializer.validated_data.get('is_real')
                if person_type == Account.BUYER_PERSON:
                    if is_real:
                        parent_code = '10301'
                    else:
                        parent_code = '10302'
                else:
                    if is_real:
                        parent_code = '30101'
                    else:
                        parent_code = '30102'

            if parent_code:
                parent = Account.objects.get(code=parent_code)
                code = parent.get_new_child_code()
                level = 3
            else:
                code = Account.get_new_group_code()
                level = 0

        serializer.save(
            financial_year=self.request.user.active_financial_year,
            parent=parent,
            code=code,
            level=level
        )

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        queryset = AccountListRetrieveSerializer.setup_eager_loading(queryset)
        serializer = AccountListRetrieveSerializer(queryset, many=True)
        res = Response(serializer.data)
        return res


class AccountDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        method = self.request.method.lower()
        if method == 'put':
            return AccountCreateUpdateSerializer
        else:
            return AccountListRetrieveSerializer

    def retrieve(self, request, **kwargs):
        account = self.get_object()
        serializer = AccountListRetrieveSerializer(account)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        account = self.get_object()
        if account.can_delete():
            return super().destroy(request, *args, **kwargs)
        return Response(['حساب های دارای گردش در سال مالی جاری غیر قابل حذف می باشند'],
                        status=status.HTTP_400_BAD_REQUEST)
