from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
    permission_basename = 'floatAccount'

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
    permission_basename = 'floatAccount'

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
    permission_basename = 'floatAccountGroup'


class FloatAccountGroupDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountGroupSerializer
    permission_basename = 'floatAccountGroup'


class AccountTypeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


def get_account_permission_basename(view):
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
        account = Account.objects.get(**view.kwargs)
        return "account{}".format(account.level)


class AccountListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = AccountCreateSerializer

    @property
    def permission_basename(self):
        return get_account_permission_basename(self)

    def get_queryset(self):
        return Account.objects.hasAccess(
            self.request.method,
            get_account_permission_basename(self)
        )

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
                if person_type == Account.REAL:
                    person_type = 'real'
                elif person_type == Account.LEGAL:
                    person_type = 'legal'
                elif person_type == Account.CONTRACTOR:
                    person_type = 'contractor'
                elif person_type == Account.OTHER:
                    person_type = 'other'

                buyer_or_seller = serializer.validated_data.get('buyer_or_seller')
                if buyer_or_seller == Account.BUYER:
                    buyer_or_seller = 'Buyer'
                elif buyer_or_seller == Account.SELLER:
                    buyer_or_seller = 'Seller'

                parent = DefaultAccount.get("{}{}Parent".format(person_type, buyer_or_seller)).account

            if parent:
                code = parent.get_new_child_code()
                level = 3
            else:
                code = Account.get_new_group_code()
                level = 0

        type = serializer.initial_data.get('type')
        if type:
            type = AccountType.objects.get(pk=type)
        else:
            type = parent.type

        serializer.save(
            financial_year=self.request.user.active_financial_year,
            parent=parent,
            code=code,
            level=level,
            type=type
        )

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        queryset = AccountListSerializer.setup_eager_loading(queryset)
        serializer = AccountListSerializer(queryset, many=True)
        res = Response(serializer.data)
        return res


class AccountDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_basename(self):
        return get_account_permission_basename(self)

    def get_serializer_class(self):
        method = self.request.method.lower()
        if method == 'put':
            return AccountUpdateSerializer
        else:
            return AccountRetrieveSerializer

    def get_queryset(self):
        return Account.objects.hasAccess(
            self.request.method,
            get_account_permission_basename(self)
        )

    def perform_update(self, serializer: AccountUpdateSerializer) -> None:

        instance = self.get_object()
        old_type = instance.type
        new_type = self.request.data.get('type')

        if new_type:
            new_type = AccountType.objects.get(pk=new_type)
        else:
            new_type = old_type

        if old_type != new_type and SanadItem.objects.filter(
                account__code__startswith=instance.code
        ).count() != 0:
            raise serializers.ValidationError("نوع حساب های دارای گردش غیر قابل ویرایش می باشد")

        serializer.save(
            type=new_type
        )

        instance = serializer.instance

        if instance.level != 0:
            # update children when account's type changes
            Account.objects.filter(
                code__startswith=instance.code,
                type=new_type
            ).update(type=instance.type)

    def destroy(self, request, *args, **kwargs):
        account = self.get_object()
        if account.can_delete():
            return super().destroy(request, *args, **kwargs)
        raise ValidationError({
            'non_field_errors': ['حساب های دارای گردش در سال مالی جاری غیر قابل حذف می باشند'],
            'sanad_ids': [item.sanad.id for item in account.sanadItems.all()[:10]],
            'item_ids': [item.id for item in account.sanadItems.all()[:10]],
        })
