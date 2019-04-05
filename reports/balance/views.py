from django.db import connection
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.accounts.models import Account, FloatAccount, FloatAccountGroup
from accounts.accounts.serializers import BankSerializer, PersonSerializer, AccountTypeSerializer
from reports.balance.serializers import BalanceAccountSerializer, BalanceFloatAccountSerializer, \
    BalanceFloatAccountGroupSerializer, FloatBalanceSerializer


@api_view(['get'])
def accountBalanceView(request):

    data = request.GET

    dateFilter = Q()
    if 'from_date' in data:
        dateFilter &= Q(sanadItems__sanad__date__gte=data['from_date'])
    if 'to_date' in data:
        dateFilter &= Q(sanadItems__sanad__date__lte=data['to_date'])
    if 'from_code' in data:
        dateFilter &= Q(sanadItems__sanad__code__gte=data['from_code'])
    if 'to_code' in data:
        dateFilter &= Q(sanadItems__sanad__code__lte=data['to_code'])
    if 'codes' in data:
        dateFilter &= Q(sanadItems__sanad__code__in=data['codes'])

    accounts = Account.objects.inFinancialYear(request.user)\
        .annotate(bed_sum=Coalesce(Sum('sanadItems__value', filter=Q(sanadItems__valueType='bed') & dateFilter), 0))\
        .annotate(bes_sum=Coalesce(Sum('sanadItems__value', filter=Q(sanadItems__valueType='bes') & dateFilter), 0))\
        .prefetch_related('bank').prefetch_related('person').prefetch_related('floatAccountGroup')\
        .prefetch_related('type')\
        .order_by('code')

    for account in accounts:
        if account.level != 3:
            for acc in accounts:
                if acc == account or acc.level != 3:
                    continue
                if acc.code.find(account.code) == 0:
                    account.bed_sum += acc.bed_sum
                    account.bes_sum += acc.bes_sum

        remain = account.bed_sum - account.bes_sum
        if remain > 0:
            account.bed_remain = remain
            account.bes_remain = 0
        else:
            account.bes_remain = -remain
            account.bed_remain = 0

        if account.type:
            account._type = AccountTypeSerializer(account.type).data
        if hasattr(account, 'bank'):
            account._bank = BankSerializer(account.bank).data
        if hasattr(account, 'person'):
            account._person = PersonSerializer(account.person).data
        if account.floatAccountGroup:
            account._floatAccountGroup = BalanceFloatAccountGroupSerializer(account.floatAccountGroup).data

        account._floatAccounts = []
        if account.floatAccountGroup:
            floatAccounts = FloatAccount.objects.inFinancialYear(request.user) \
                .filter(floatAccountGroups__in=[account.floatAccountGroup])\
                .annotate(bed_sum=Coalesce(Sum('sanadItems__value',
                                               filter=Q(sanadItems__valueType='bed') &
                                                      Q(sanadItems__account=account) &
                                                      dateFilter), 0)) \
                .annotate(bes_sum=Coalesce(Sum('sanadItems__value',
                                               filter=Q(sanadItems__valueType='bes') &
                                                      Q(sanadItems__account=account) &
                                                      dateFilter), 0)) \
                .prefetch_related('floatAccountGroups')

            for floatAccount in floatAccounts:
                remain = floatAccount.bed_sum - floatAccount.bes_sum
                if remain > 0:
                    floatAccount.bed_remain = remain
                    floatAccount.bes_remain = 0
                else:
                    floatAccount.bes_remain = -remain
                    floatAccount.bed_remain = 0
                account._floatAccounts.append(BalanceFloatAccountSerializer(floatAccount).data)

    res = Response(BalanceAccountSerializer(accounts, many=True).data)
    # print(len(connection.queries))
    return res


@api_view(['get'])
def floatAccountBalanceView(request):

    data = request.GET

    dateFilter = Q()
    if 'from_date' in data:
        dateFilter &= Q(sanadItems__sanad__date__gte=data['from_date'])
    if 'to_date' in data:
        dateFilter &= Q(sanadItems__sanad__date__lte=data['to_date'])
    if 'from_code' in data:
        dateFilter &= Q(sanadItems__sanad__code__gte=data['from_code'])
    if 'to_code' in data:
        dateFilter &= Q(sanadItems__sanad__code__lte=data['to_code'])
    if 'codes' in data:
        dateFilter &= Q(sanadItems__sanad__code__in=data['codes'])

    floatAccounts = FloatAccount.objects.inFinancialYear(request.user) \
        .annotate(bed_sum=Coalesce(Sum('sanadItems__value', filter=Q(sanadItems__valueType='bed') & dateFilter), 0)) \
        .annotate(bes_sum=Coalesce(Sum('sanadItems__value', filter=Q(sanadItems__valueType='bes') & dateFilter), 0)) \
        .prefetch_related('floatAccountGroups')

    floatAccountGroups = FloatAccountGroup.objects.inFinancialYear(request.user).prefetch_related('floatAccounts').all()

    res = []

    for floatAccountGroup in floatAccountGroups:
        floatAccountGroup.group_name = floatAccountGroup.name
        floatAccountGroup.float_account_name = ''
        floatAccountGroup.bed_sum = 0
        floatAccountGroup.bes_sum = 0
        res.append(floatAccountGroup)
        for floatAccount in floatAccounts:
            floatAccount.float_account_name = floatAccount.name
            floatAccount.group_name = ''
            if floatAccountGroup in floatAccount.floatAccountGroups.all():
                floatAccountGroup.bed_sum += floatAccount.bed_sum
                floatAccountGroup.bes_sum += floatAccount.bes_sum
                res.append(floatAccount)

    for account in res:
        remain = account.bed_sum - account.bes_sum
        if remain > 0:
            account.bed_remain = remain
            account.bes_remain = 0
        else:
            account.bes_remain = -remain
            account.bed_remain = 0

    res = Response(FloatBalanceSerializer(res, many=True).data)
    # print(len(connection.queries))
    return res
