from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account, FloatAccount, FloatAccountGroup
from accounts.accounts.serializers import AccountTypeSerializer
from helpers.auth import BasicCRUDPermission
from helpers.exports import get_xlsx_response, MPDFTemplateView
from reports.balance.serializers import BalanceAccountSerializer, BalanceFloatAccountSerializer, \
    BalanceFloatAccountGroupSerializer
from reports.filters import get_account_sanad_items_filter
from reports.lists.export_views import BaseExportView

common_headers = [
    'گردش بدهکار',
    'گردش بستانکار',
    'مانده بدهکار',
    'مانده بستانکار'
]


def get_common_columns(obj, is_dict=False):
    if is_dict:
        return [
            obj['bed_sum'],
            obj['bes_sum'],
            obj['bed_remain'],
            obj['bes_remain'],
        ]
    return [
        obj.bed_sum,
        obj.bes_sum,
        obj.bed_remain,
        obj.bes_remain,
    ]


def get_common_columns_sum(objs, is_dict=False):
    bed_sum = bes_sum = bed_remain = bes_remain = 0
    for obj in objs:

        if is_dict:
            bed_sum += obj['bed_sum']
            bes_sum += obj['bes_sum']
            bed_remain += obj['bed_remain']
            bes_remain += obj['bes_remain']
        else:
            bed_sum += obj.bed_sum
            bes_sum += obj.bes_sum
            bed_remain += obj.bed_remain
            bes_remain += obj.bes_remain
    return [
        bed_sum,
        bes_sum,
        bed_remain,
        bes_remain,
    ]


class AccountBalanceView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.accountBalanceReport'

    def get_accounts(self, request):
        filters = get_account_sanad_items_filter(request)
        account_code_starts_with = request.GET.get('account_code_starts_with', '')

        accounts = Account.objects.inFinancialYear() \
            .filter(code__startswith=account_code_starts_with) \
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
                floatAccounts = FloatAccount.objects.inFinancialYear() \
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
                floatAccounts = FloatAccount.objects.inFinancialYear() \
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

        return accounts

    def get(self, request):
        accounts = self.get_accounts(request)
        res = Response(BalanceAccountSerializer(accounts, many=True).data)
        return res


class AccountBalanceExportView(AccountBalanceView, MPDFTemplateView):
    filename = 'balance.pdf'
    template_name = 'reports/balance_report.html'

    def get(self, request, *args, **kwargs):
        export_type = kwargs.get('export_type')
        if export_type == 'xlsx':
            return self.get_xlsx(request)
        elif export_type == 'pdf':
            return super().get(request, user=request.user, *args, **kwargs)
        else:
            return self.render(request)

    def get_context_data(self, request, **kwargs):
        return self.get_accounts(request)

    def get_xlsx(self, request):
        accounts = self.get_accounts(request)

        data = [[
            '#',
            'کد حساب',
            'نام حساب',
            *common_headers
        ]]
        for account in accounts:
            data.append([
                account.code,
                account.name,
                *get_common_columns(account)
            ])

        data.append([
            '', '',
            'جمع',
            *get_common_columns_sum(accounts)
        ])

        return get_xlsx_response('account balance', data)


class FloatAccountBalanceByGroupView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.floatAccountBalanceByGroupReport'

    def get_accounts_data(self, request):

        filters = get_account_sanad_items_filter(request)

        is_cost_center = request.GET.get('is_cost_center') == 'true'

        floatAccounts = FloatAccount.objects.inFinancialYear().filter(is_cost_center=is_cost_center)
        floatAccountGroups = FloatAccountGroup.objects.inFinancialYear().prefetch_related(
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
                if floatAccountGroup.id in [o.id for o in floatAccount.floatAccountGroups.all()]:
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

        return res

    def get(self, request):
        data = self.get_accounts_data(request)
        res = Response(data)
        return res


class FloatAccountBalanceByGroupExportView(FloatAccountBalanceByGroupView):

    def get(self, request, **kwargs):
        accounts_data = self.get_accounts_data(request)
        is_cost_center = request.GET.get('is_cost_center') == 'true'

        if is_cost_center:
            column_label = "مرکز هزینه و درآمد"
            file_name = "Cost & Income Center By Group Balance"
        else:
            column_label = "شناور"
            file_name = "Float By Group Balance"

        data = [[
            '#',
            'گروه',
            column_label,
            *common_headers
        ]]
        for account in accounts_data:
            data.append([
                accounts_data.index(account),
                account['group_name'],
                account['float_account_name'],
                *get_common_columns(account, True)
            ])

        data.append([
            '', '',
            'جمع',
            *get_common_columns_sum(accounts_data, True)
        ])

        return get_xlsx_response(file_name, data)


class FloatAccountBalanceView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.floatAccountBalanceReport'

    def get_accounts_data(self, request):
        filters = get_account_sanad_items_filter(request)

        is_cost_center = request.GET.get('is_cost_center') == 'true'

        if is_cost_center:
            sanad_item_key = "sanadItemsAsCostCenter"
        else:
            sanad_item_key = "sanadItems"

        floatAccounts = FloatAccount.objects.inFinancialYear().annotate(
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

        return res

    def get(self, request):
        res = self.get_accounts_data(request)

        res = Response(res)
        return res


class FloatAccountBalanceExportView(FloatAccountBalanceView):

    def get(self, request, **kwargs):
        accounts_data = self.get_accounts_data(request)

        is_cost_center = request.GET.get('is_cost_center') == 'true'

        if is_cost_center:
            column_label = "مرکز هزینه و درآمد"
            file_name = "Cost & Income Center Balance"
        else:
            column_label = "شناور"
            file_name = "Float Balance"

        data = [[
            '#',
            column_label,
            *common_headers
        ]]
        for account in accounts_data:
            data.append([
                account['float_account_name'],
                *get_common_columns(account, True)
            ])

        data.append([
            '',
            'جمع',
            *get_common_columns_sum(accounts_data, True)
        ])

        return get_xlsx_response(file_name, data)
