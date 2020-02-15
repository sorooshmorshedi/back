from django.db.models import Prefetch
from django.db.models.aggregates import Max
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
from helpers.views import ListCreateAPIViewWithAutoFinancialYear, RetrieveUpdateDestroyAPIViewWithAutoFinancialYear


@method_decorator(csrf_exempt, name='dispatch')
class FloatAccountListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountSerializer

    def created(self, instance, request):
        syncFloatAccountGroups = request.data.get('syncFloatAccountGroups', [])
        financial_year = request.user.active_financial_year
        for floatAccountGroup in syncFloatAccountGroups:
            relation = FloatAccountRelation.create(
                floatAccount=instance,
                floatAccountGroup=floatAccountGroup
            )
            financial_year.add(relation)
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
                     queryset=FloatAccountGroup.objects.inFinancialYear(user)
                     .filter(relation__financial_year=financial_year)
                     .distinct()
                     )
        )
        return queryset

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        syncFloatAccountGroups = request.data.get('syncFloatAccountGroups', [])
        instance = self.get_object()
        FloatAccountRelation.objects.inFinancialYear(request.user).filter(
            floatAccount=instance,
            floatAccountGroup__in=syncFloatAccountGroups
        ).delete()
        financial_year = request.user.active_financial_year
        for floatAccountGroup in syncFloatAccountGroups:
            relation = FloatAccountRelation.create(
                floatAccount=instance,
                floatAccountGroup=floatAccountGroup
            )
            financial_year.add(relation)
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
                     queryset=FloatAccount.objects.inFinancialYear(user)
                     .filter(relation__financial_year=financial_year)
                     .distinct()
                     )
        )
        return queryset


class FloatAccountGroupDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = FloatAccountGroupSerializer


class IndependentAccountDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = IndependentAccountSerializer


class IndependentAccountListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = IndependentAccountSerializer


class AccountTypeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


class AccountListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = AccountCreateUpdateSerializer

    def perform_create(self, serializer):
        parent = serializer.validated_data['parent']
        if parent:
            code = parent.get_new_child_code()
            level = parent.level - 1
        else:
            code = Account.objects.inFinancialYear(self.request.user).filter(level=Account.GROUP).annotate(Max('code'))[
                       'code_max'] + 1
            level = 0
        serializer.save(
            code=code,
            level=level
        )

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        queryset = AccountListRetrieveCreateUpdateSerializer.setup_eager_loading(queryset)
        serializer = AccountListRetrieveCreateUpdateSerializer(queryset, many=True)
        res = Response(serializer.data)
        return res


class AccountDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = AccountListRetrieveCreateUpdateSerializer

    def retrieve(self, request, **kwargs):
        account = self.get_object()
        serializer = AccountListRetrieveCreateUpdateSerializer(account)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        account = self.get_object()
        if account.can_delete():
            return super().destroy(request, *args, **kwargs)
        return Response(['حساب های دارای گردش در سال مالی جاری غیر قابل حذف می باشند'],
                        status=status.HTTP_400_BAD_REQUEST)


class PersonListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = PersonSerializer


class PersonDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = PersonSerializer


class BankListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = BankSerializer


class BankDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = BankSerializer


@api_view(['get'])
def getAccountRemain(request, pk):
    account = get_object_or_404(Account.objects.inFinancialYear(request.user), pk=pk)
    return Response(account.get_remain(), status=status.HTTP_200_OK)
