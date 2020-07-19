from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.accounts.models import FloatAccountRelation
from accounts.accounts.serializers import *
from accounts.defaultAccounts.models import DefaultAccount
from helpers.auth import BasicCRUDPermission
from helpers.views.RetrieveUpdateDestroyAPIViewWithAutoFinancialYear import \
    RetrieveUpdateDestroyAPIViewWithAutoFinancialYear
from helpers.views.ListCreateAPIViewWithAutoFinancialYear import ListCreateAPIViewWithAutoFinancialYear


class FloatAccountListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountSerializer
    permission_base_codename = 'floatAccount'

    def created(self, instance, request):
        syncFloatAccountGroups = request.data.pop('syncFloatAccountGroups', [])
        financial_year = request.user.active_financial_year
        for floatAccountGroup in syncFloatAccountGroups:
            relation = FloatAccountRelation.objects.create(
                financial_year=request.user.active_financial_year,
                floatAccount=instance,
                floatAccountGroup=FloatAccountGroup.objects.get(pk=floatAccountGroup)
            )
            financial_year.floatAccountRelations.add(relation)
        return instance


class FloatAccountDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountSerializer
    permission_base_codename = 'floatAccount'

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
                financial_year=request.user.active_financial_year,
                floatAccount=instance,
                floatAccountGroup=FloatAccountGroup.objects.get(pk=floatAccountGroup)
            )
            financial_year.floatAccountRelations.add(relation)
        return res


class FloatAccountGroupListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountGroupSerializer
    permission_base_codename = 'floatAccountGroup'

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
    permission_base_codename = 'floatAccountGroup'


class AccountTypeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


def get_account_permission_base_codename(view):
    method = view.request.method.lower()

    if method == 'get':
        return 'account'
    elif method == 'post':
        parent_id = view.request.data.get('parent', None)
        if parent_id:
            parent = get_object_or_404(Account, pk=parent_id)
            return "account{}".format(parent.level + 1)
        else:
            return "account0"
    else:
        account = view.get_object()
        return "account{}".format(account.level)


class AccountListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = AccountCreateUpdateSerializer

    @property
    def permission_base_codename(self):
        return get_account_permission_base_codename(self)

    def perform_create(self, serializer):

        parent = serializer.validated_data.get('parent')
        account_type = serializer.validated_data.get('account_type')
        if parent:
            code = parent.get_new_child_code()
            level = parent.level + 1
        else:
            parent = None
            if account_type == Account.BANK:
                parent = DefaultAccount.get("bankParent").account
            elif account_type == Account.PERSON:
                person_type = serializer.validated_data.get('person_type')
                is_real = serializer.validated_data.get('is_real')
                if person_type == Account.BUYER_PERSON:
                    if is_real:
                        parent = DefaultAccount.get("realBuyerParent").account
                    else:
                        parent = DefaultAccount.get("notRealBuyerParent").account
                else:
                    if is_real:
                        parent = DefaultAccount.get("realSellerParent").account
                    else:
                        parent = DefaultAccount.get("notRealSellerParent").account

            if parent:
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
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_base_codename(self):
        return get_account_permission_base_codename(self)

    def get_serializer_class(self):
        method = self.request.method.lower()
        if method == 'put':
            return AccountCreateUpdateSerializer
        else:
            return AccountListRetrieveSerializer

    def destroy(self, request, *args, **kwargs):
        account = self.get_object()
        if account.can_delete():
            return super().destroy(request, *args, **kwargs)
        return Response(['حساب های دارای گردش در سال مالی جاری غیر قابل حذف می باشند'],
                        status=status.HTTP_400_BAD_REQUEST)
