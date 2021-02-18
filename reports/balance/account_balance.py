from typing import List

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account
from helpers.auth import BasicCRUDPermission
from helpers.db import select_raw_sql
from helpers.exports import get_xlsx_response
from helpers.functions import to_gregorian
from reports.balance.serializers import BalanceAccountSerializer
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

    _rows = None

    @staticmethod
    def get_rows(filters, financial_year):

        if AccountBalanceView._rows:
            return AccountBalanceView._rows

        where_filters = "true and "
        if filters.get('from_date'):
            where_filters += "sanad.date >= '{}' and ".format(to_gregorian(filters['from_date']))
        if filters.get('to_date'):
            where_filters += "sanad.date <= '{}' and ".format(to_gregorian(filters['to_date']))
        if filters.get('from_code'):
            where_filters += "sanad.code >= {} and ".format(filters['from_code'])
        if filters.get('to_code'):
            where_filters += "sanad.code <= {} and ".format(filters['to_code'])
        if filters.get('skip_closing_sanad', False) == 'true':
            closing_sanad_names = [
                'temporaryClosingSanad',
                'currentEarningsClosingSanad',
                'permanentsClosingSanad',
            ]
            for closing_sanad_name in closing_sanad_names:
                closing_sanad = getattr(financial_year, closing_sanad_name)
                if closing_sanad:
                    where_filters += "sanad.id != {} and ".format(closing_sanad.id)

        where_filters += "true"

        sql = """
            select 
                account_id, 
                \"floatAccount_id\",
                \"costCenter_id\", 
                sum(sanadItem.bed) as bed_sum, sum(sanadItem.bes) as bes_sum
            from sanads_sanaditem as sanadItem join sanads_sanad as sanad on sanadItem.sanad_id = sanad.id
            where {}
            group by account_id, \"floatAccount_id\", \"costCenter_id\"
            order by account_id
        """.format(where_filters)

        AccountBalanceView._rows = select_raw_sql(sql)
        return AccountBalanceView._rows

    def set_remain(self, account: Account, accounts: List[Account]):

        if hasattr(account, 'bed_sum'):
            return

        account.bed_sum = 0
        account.bes_sum = 0
        account.bed_remain = 0
        account.bes_remain = 0

        if account.level == Account.TAFSILI:
            rows = self.get_rows(self.request.GET, self.request.user.active_financial_year)
            for row in rows:
                if row['account_id'] == account.id:
                    account.bed_sum += row['bed_sum']
                    account.bes_sum += row['bes_sum']
        else:
            for sub_account in accounts:
                if sub_account.parent_id == account.id:
                    self.set_remain(sub_account, accounts)
                    account.bed_sum += sub_account.bed_sum
                    account.bes_sum += sub_account.bes_sum

        remain = account.bed_sum - account.bes_sum
        if remain > 0:
            account.bed_remain = remain
        else:
            account.bes_remain = -remain

    def get_accounts(self, request):

        account_code_starts_with = request.GET.get('account_code_starts_with')
        level = request.GET.get('level')
        account_type = request.GET.get('account_type')
        account_code_gte = request.GET.get('account__code__gte')
        account_code_lte = request.GET.get('account__code__lte')
        balance_status = request.GET.get('balance_status')
        show_float_accounts = request.GET.get('show_float_accounts')
        show_cost_centers = request.GET.get('show_cost_centers')
        show_differences = request.GET.get('show_differences')

        qs = Account.objects.inFinancialYear()

        accounts = qs.prefetch_related(
            'type',
            'floatAccountGroup',
            'costCenterGroup',
            'floatAccountGroup__floatAccounts',
            'costCenterGroup__floatAccounts',
        ).order_by('code').all()

        for account in accounts:

            self.set_remain(account, accounts)

            if account.type:
                account.type_data = {
                    'nature': account.type.nature
                }

            account.floatAccounts_data = []
            account.costCenters_data = []

            rows = self.get_rows(self.request.GET, self.request.user.active_financial_year)

            if show_float_accounts == 'true' and account.floatAccountGroup:
                for floatAccount in account.floatAccountGroup.floatAccounts.all():
                    floatAccount.bed_sum = 0
                    floatAccount.bes_sum = 0
                    for row in rows:
                        if row['account_id'] == account.id and row['floatAccount_id'] == floatAccount.id:
                            floatAccount.bed_sum += row['bed_sum']
                            floatAccount.bes_sum += row['bes_sum']

                    remain = floatAccount.bed_sum - floatAccount.bes_sum
                    if remain > 0:
                        floatAccount.bed_remain = remain
                        floatAccount.bes_remain = 0
                    else:
                        floatAccount.bes_remain = -remain
                        floatAccount.bed_remain = 0
                    account.floatAccounts_data.append({
                        'id': floatAccount.id,
                        'name': floatAccount.name,
                        'bed_sum': floatAccount.bed_sum,
                        'bes_sum': floatAccount.bes_sum,
                        'bed_remain': floatAccount.bed_remain,
                        'bes_remain': floatAccount.bes_remain,
                    })

            if show_cost_centers == 'true' and account.costCenterGroup:
                for floatAccount in account.costCenterGroup.floatAccounts.all():
                    floatAccount.bed_sum = 0
                    floatAccount.bes_sum = 0
                    for row in rows:
                        if row['account_id'] == account.id and row['costCenter_id'] == floatAccount.id:
                            floatAccount.bed_sum += row['bed_sum']
                            floatAccount.bes_sum += row['bes_sum']

                    remain = floatAccount.bed_sum - floatAccount.bes_sum
                    if remain > 0:
                        floatAccount.bed_remain = remain
                        floatAccount.bes_remain = 0
                    else:
                        floatAccount.bes_remain = -remain
                        floatAccount.bed_remain = 0
                    account.costCenters_data.append({
                        'id': floatAccount.id,
                        'name': floatAccount.name,
                        'bed_sum': floatAccount.bed_sum,
                        'bes_sum': floatAccount.bes_sum,
                        'bed_remain': floatAccount.bed_remain,
                        'bes_remain': floatAccount.bes_remain,
                    })

        accounts = list(accounts)
        for account in accounts:
            if show_differences == 'true':
                nature = account.type.nature
                if (
                        account.bed_remain == account.bes_remain == 0
                ) or (
                        nature == 'bed' and account.bes_remain != 0
                ) or (
                        nature == 'bes' and account.bed_remain != 0
                ):
                    accounts.remove(account)

        def filter_account(acc: Account):
            result = True

            if account_code_starts_with:
                result = result and acc.code.startswith(account_code_starts_with)

            if account_type == 'buyer':
                result = result and acc.account_type == Account.PERSON and acc.buyer_or_seller == Account.BUYER
            elif account_type == 'seller':
                result = result and acc.account_type == Account.PERSON and acc.buyer_or_seller == Account.SELLER
            elif account_type == 'bank':
                result = result and acc.account_type == Account.BANK

            if level is not None:
                result = result and acc.level == int(level)

            if balance_status == 'with_remain':
                result = result and acc.bed_sum != acc.bes_sum
            elif balance_status == 'without_remain':
                result = result and acc.bed_sum == acc.bes_sum
            elif balance_status == 'bed_remain':
                result = result and acc.bed_sum > acc.bes_sum
            elif balance_status == 'bes_remain':
                result = result and acc.bed_sum < acc.bes_sum
            elif balance_status == 'with_transaction':
                result = result and (acc.bed_sum != 0 or acc.bes_sum != 0)
            elif balance_status == 'without_transaction':
                result = result and acc.bed_sum == 0 and acc.bes_sum == 0

            if account_code_gte:
                result = result and acc.code >= account_code_gte
            if account_code_lte:
                result = result and acc.code < account_code_lte

            return result

        accounts = list(filter(filter_account, accounts))

        return accounts

    def get(self, request):
        accounts = self.get_accounts(request)
        res = Response(BalanceAccountSerializer(accounts, many=True).data)
        return res


class AccountBalanceExportView(AccountBalanceView, BaseExportView):
    filename = 'account-balance.pdf'
    template_name = 'export/simple_export.html'

    def get_context_data(self, user, **kwargs):
        data = self.request.GET.copy()
        accounts = self.get_accounts(self.request)

        context = {
            'title': "تراز حساب ها",
            'content_template': 'reports/balance_report.html',
            'company': self.request.user.active_company,
            'user': self.request.user,
            'items': BalanceAccountSerializer(accounts, many=True).data,
            'show_float_accounts': data.get('show_float_accounts') == 'true',
            'show_cost_centers': data.get('show_cost_centers') == 'true',
            'four_cols': data.get('cols_count') == '4',
            'sum': get_common_columns_sum(accounts)
        }

        return context

    def xlsx_response(self, request, *args, **kwargs):
        accounts = self.get_accounts(request)

        context = self.get_context_data(request.user, **kwargs)
        show_float_accounts = context['show_float_accounts']
        show_cost_centers = context['show_cost_centers']

        data = [[
            '#',
            'کد حساب',
            'نام حساب',
            *common_headers
        ]]
        for account in accounts:
            data.append([
                accounts.index(account),
                account.code,
                account.name,
                *get_common_columns(account)
            ])

            sub_items = []
            if show_float_accounts:
                sub_items += account.floatAccounts_data
            if show_cost_centers:
                sub_items += account.costCenters_data

            for item in sub_items:
                data.append([
                    '', '',
                    item['name'],
                    *get_common_columns(item, True)
                ])

        data.append([
            '', '',
            'جمع',
            *get_common_columns_sum(accounts)
        ])

        return get_xlsx_response('account-balance', data)

    def get(self, *args, **kwargs):
        return self.export(*args, **kwargs)
