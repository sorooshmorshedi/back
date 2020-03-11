from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.accounts.models import Account, FloatAccount, FloatAccountGroup
from accounts.accounts.serializers import AccountTypeSerializer
from reports.balance.serializers import BalanceAccountSerializer, BalanceFloatAccountSerializer, \
    BalanceFloatAccountGroupSerializer, FloatBalanceSerializer
from reports.filters import get_account_sanad_items_filter


@api_view(['get'])
def accountBalanceView(request):
    filters = get_account_sanad_items_filter(request)

    accounts = Account.objects.inFinancialYear(request.user) \
        .annotate(bed_sum=Coalesce(Sum('sanadItems__bed', filter=filters), 0)) \
        .annotate(bes_sum=Coalesce(Sum('sanadItems__bes', filter=filters), 0)) \
        .prefetch_related('floatAccountGroup').prefetch_related('costCenterGroup').prefetch_related('type') \
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
            account.bed_remain = 0
            account.bes_remain = -remain

        if account.type:
            account._type = AccountTypeSerializer(account.type).data
        if account.floatAccountGroup:
            account._floatAccountGroup = BalanceFloatAccountGroupSerializer(account.floatAccountGroup).data
        if account.costCenterGroup:
            account._costCenterGroup = BalanceFloatAccountGroupSerializer(account.costCenterGroup).data

        account._floatAccounts = []
        account._costCenters = []
        if account.floatAccountGroup:
            floatAccounts = FloatAccount.objects.inFinancialYear(request.user) \
                .filter(floatAccountGroups__in=[account.floatAccountGroup]) \
                .annotate(bed_sum=Coalesce(Sum('sanadItems__bed',
                                               filter=Q(sanadItems__account=account) & filters), 0)) \
                .annotate(bes_sum=Coalesce(Sum('sanadItems__bes',
                                               filter=Q(sanadItems__account=account) & filters), 0)) \
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

        if account.costCenterGroup:
            floatAccounts = FloatAccount.objects.inFinancialYear(request.user) \
                .filter(floatAccountGroups__in=[account.costCenterGroup]) \
                .annotate(bed_sum=Coalesce(Sum('sanadItemsAsCostCenter__bed',
                                               filter=Q(sanadItemsAsCostCenter__account=account) & filters), 0)) \
                .annotate(bes_sum=Coalesce(Sum('sanadItemsAsCostCenter__bes',
                                               filter=Q(sanadItemsAsCostCenter__account=account) & filters), 0)) \
                .prefetch_related('floatAccountGroups')

            for floatAccount in floatAccounts:
                remain = floatAccount.bed_sum - floatAccount.bes_sum
                if remain > 0:
                    floatAccount.bed_remain = remain
                    floatAccount.bes_remain = 0
                else:
                    floatAccount.bes_remain = -remain
                    floatAccount.bed_remain = 0
                account._costCenters.append(BalanceFloatAccountSerializer(floatAccount).data)

    res = Response(BalanceAccountSerializer(accounts, many=True).data)
    return res


@api_view(['get'])
def floatAccountBalanceByGroupView(request):
    filters = get_account_sanad_items_filter(request)

    is_cost_center = request.GET.get('is_cost_center') == 'true'

    floatAccounts = FloatAccount.objects.inFinancialYear(request.user).filter(is_cost_center=is_cost_center)
    floatAccountGroups = FloatAccountGroup.objects.inFinancialYear(request.user).prefetch_related(
        'floatAccounts').filter(is_cost_center=is_cost_center)

    if is_cost_center:
        sanad_item_key = "sanadItemsAsCostCenter"
        float_account_group_key = "costCenterGroup"
    else:
        sanad_item_key = "sanadItems"
        float_account_group_key = "floatAccountGroup"

    for floatAccountGroup in floatAccountGroups.all():
        annotates = {
            "bed_sum_{}".format(floatAccountGroup.id): Coalesce(
                Sum(
                    '{}__bed'.format(sanad_item_key),
                    filter=(filters & Q(**{
                        '{}__account__{}'.format(sanad_item_key, float_account_group_key): floatAccountGroup
                    }))
                ),
                0
            ),
            "bes_sum_{}".format(floatAccountGroup.id): Coalesce(
                Sum(
                    '{}__bes'.format(sanad_item_key),
                    filter=(filters & Q(**{
                        '{}__account__{}'.format(sanad_item_key, float_account_group_key): floatAccountGroup
                    }))
                ),
                0
            ),
        }

        floatAccounts = floatAccounts.annotate(**annotates)

    res = []

    for floatAccountGroup in floatAccountGroups:

        bed_sum = bes_sum = 0
        for floatAccount in floatAccounts:
            if floatAccountGroup in floatAccount.floatAccountGroups.all():
                bed_sum += getattr(floatAccount, "bed_sum_{}".format(floatAccountGroup.id))
                bes_sum += getattr(floatAccount, "bes_sum_{}".format(floatAccountGroup.id))

        res.append({
            'bed_sum': bed_sum,
            'bes_sum': bes_sum,
            'bed_remain': 0,
            'bes_remain': 0,
            'group_name': floatAccountGroup.name,
            'float_account_name': '',
        })

        for floatAccount in floatAccounts:
            if floatAccountGroup in floatAccount.floatAccountGroups.all():
                bed_sum = getattr(floatAccount, "bed_sum_{}".format(floatAccountGroup.id))
                bes_sum = getattr(floatAccount, "bes_sum_{}".format(floatAccountGroup.id))

                res.append({
                    'bed_sum': bed_sum,
                    'bes_sum': bes_sum,
                    'bed_remain': 0,
                    'bes_remain': 0,
                    'group_name': '',
                    'float_account_name': floatAccount.name,
                })

    for account in res:
        remain = account['bed_sum'] - account['bes_sum']
        if remain > 0:
            account['bed_remain'] = remain
            account['bes_remain'] = 0
        else:
            account['bes_remain'] = -remain
            account['bed_remain'] = 0

    res = Response(res)
    return res


@api_view(['get'])
def floatAccountBalanceView(request):
    filters = get_account_sanad_items_filter(request)

    is_cost_center = request.GET.get('is_cost_center') == 'true'

    if is_cost_center:
        sanad_item_key = "sanadItemsAsCostCenter"
    else:
        sanad_item_key = "sanadItems"

    floatAccounts = FloatAccount.objects.inFinancialYear(request.user).annotate(
        bed_sum=Coalesce(Sum('{}__bed'.format(sanad_item_key), filter=filters), 0),
        bes_sum=Coalesce(Sum('{}__bes'.format(sanad_item_key), filter=filters), 0),
    ).filter(is_cost_center=is_cost_center)

    res = []
    for floatAccount in floatAccounts:
        res.append({
            'bed_sum': floatAccount.bed_sum,
            'bes_sum': floatAccount.bes_sum,
            'bed_remain': 0,
            'bes_remain': 0,
            'float_account_name': floatAccount.name,
        })

    for account in res:
        remain = account['bed_sum'] - account['bes_sum']
        if remain > 0:
            account['bed_remain'] = remain
            account['bes_remain'] = 0
        else:
            account['bes_remain'] = -remain
            account['bed_remain'] = 0

    res = Response(res)
    return res
