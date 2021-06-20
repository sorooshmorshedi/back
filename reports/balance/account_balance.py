from typing import List

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account
from helpers.auth import BasicCRUDPermission
from helpers.db import select_raw_sql
from helpers.functions import to_gregorian
from reports.balance.serializers import BalanceAccountSerializer
from reports.lists.export_views import BaseListExportView
from sanads.models import Sanad

common_headers = [
    'گردش بدهکار',
    'گردش بستانکار',
    'مانده بدهکار',
    'مانده بستانکار'
]


def get_common_columns(obj, is_dict=False) -> dict:
    if is_dict:
        return {
            'opening_bed_sum': obj['bed_sum'],
            'opening_bes_sum': obj['bes_sum'],
            'previous_bed_sum': obj['bed_sum'],
            'previous_bes_sum': obj['bes_sum'],
            'bed_sum': obj['bed_sum'],
            'bes_sum': obj['bes_sum'],
            'bed_remain': obj['bed_remain'],
            'bes_remain': obj['bes_remain'],
        }
    return {
        'opening_bed_sum': obj.bed_sum,
        'opening_bes_sum': obj.bes_sum,
        'previous_bed_sum': obj.bed_sum,
        'previous_bes_sum': obj.bes_sum,
        'bed_sum': obj.bed_sum,
        'bes_sum': obj.bes_sum,
        'bed_remain': obj.bed_remain,
        'bes_remain': obj.bes_remain,
    }


def get_common_columns_sum(objs, is_dict=False) -> dict:
    sums = {}
    for obj in objs:
        obj = get_common_columns(obj, is_dict)
        for key in obj.keys():
            sums[key] = sums.get(key, 0) + obj[key]

    return sums


class AccountBalanceView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.accountBalanceReport'

    _rows = None

    @staticmethod
    def get_db_rows(filters, financial_year):

        if AccountBalanceView._rows:
            return AccountBalanceView._rows

        where_filters = "sanad.financial_year_id = {} and ".format(financial_year.id)
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

        base_query = """
            select 
                account_id, 
                \"floatAccount_id\",
                \"costCenter_id\", 
                sum(sanadItem.bed) as bed_sum,
                sum(sanadItem.bes) as bes_sum
            from sanads_sanaditem as sanadItem join sanads_sanad as sanad on sanadItem.sanad_id = sanad.id
            where {}
            group by account_id, \"floatAccount_id\", \"costCenter_id\"
            order by account_id
        """

        sql = base_query.format(where_filters)
        rows = select_raw_sql(sql)

        opening_sql = base_query.format(where_filters + " and sanad.type = '{}'".format(Sanad.OPENING))
        opening_rows = select_raw_sql(opening_sql)

        previous_rows = []

        def are_equal(r1, r2):
            return r1['account_id'] == r2['account_id'] and \
                   r1['floatAccount_id'] == r2['floatAccount_id'] and \
                   r1['costCenter_id'] == r2['costCenter_id']

        for row in rows:
            row['opening_bed_sum'] = row['opening_bes_sum'] = row['previous_bed_sum'] = row['previous_bes_sum'] = 0

        for row in rows:
            for opening_row in opening_rows:
                if are_equal(row, opening_row):
                    row['opening_bed_sum'] = opening_row['bed_sum']
                    row['opening_bes_sum'] = opening_row['bes_sum']
                    continue

        # for previous_row in previous_rows:
        #     if are_equal(row, previous_row):
        #         row['previous_bed_sum'] = previous_row['bed_sum']
        #         row['previous_bes_sum'] = previous_row['bes_sum']

        AccountBalanceView._rows = rows

        return rows

    def set_remain(self, account: Account, accounts: List[Account]):

        if hasattr(account, 'bed_sum'):
            return

        account.bed_sum = 0
        account.bes_sum = 0
        account.bed_remain = 0
        account.bes_remain = 0

        account.opening_bed_sum = 0
        account.opening_bes_sum = 0

        account.previous_bed_sum = 0
        account.previous_bes_sum = 0

        if account.level == Account.TAFSILI:
            rows = self.get_db_rows(self.request.GET, self.request.user.active_financial_year)
            for row in rows:
                if row['account_id'] == account.id:
                    account.bed_sum += row['bed_sum']
                    account.bes_sum += row['bes_sum']
                    account.opening_bed_sum += row['opening_bed_sum']
                    account.opening_bes_sum += row['opening_bes_sum']
                    account.previous_bed_sum += row['previous_bed_sum']
                    account.previous_bes_sum += row['previous_bes_sum']
        else:
            for sub_account in accounts:
                if sub_account.parent_id == account.id:
                    self.set_remain(sub_account, accounts)
                    account.bed_sum += sub_account.bed_sum
                    account.bes_sum += sub_account.bes_sum
                    account.opening_bed_sum += sub_account.opening_bed_sum
                    account.opening_bes_sum += sub_account.opening_bes_sum
                    account.previous_bed_sum += sub_account.previous_bed_sum
                    account.previous_bes_sum += sub_account.previous_bes_sum

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

            rows = self.get_db_rows(self.request.GET, self.request.user.active_financial_year)

            if show_float_accounts == 'true' and account.floatAccountGroup:
                for floatAccount in account.floatAccountGroup.floatAccounts.all():
                    floatAccount.bed_sum = 0
                    floatAccount.bes_sum = 0
                    floatAccount.opening_bed_sum = 0
                    floatAccount.opening_bes_sum = 0
                    floatAccount.previous_bed_sum = 0
                    floatAccount.previous_bes_sum = 0
                    for row in rows:
                        if row['account_id'] == account.id and row['floatAccount_id'] == floatAccount.id:
                            floatAccount.bed_sum += row['bed_sum']
                            floatAccount.bes_sum += row['bes_sum']
                            floatAccount.opening_bed_sum += row['opening_bed_sum']
                            floatAccount.opening_bes_sum += row['opening_bes_sum']
                            floatAccount.previous_bed_sum += row['previous_bed_sum']
                            floatAccount.previous_bes_sum += row['previous_bes_sum']

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
                        'opening_bed_sum': floatAccount.opening_bed_sum,
                        'opening_bes_sum': floatAccount.opening_bes_sum,
                        'previous_bed_sum': floatAccount.previous_bed_sum,
                        'previous_bes_sum': floatAccount.previous_bes_sum,
                    })

            if show_cost_centers == 'true' and account.costCenterGroup:
                for floatAccount in account.costCenterGroup.floatAccounts.all():
                    floatAccount.bed_sum = 0
                    floatAccount.bes_sum = 0
                    floatAccount.opening_bed_sum = 0
                    floatAccount.opening_bes_sum = 0
                    floatAccount.previous_bed_sum = 0
                    floatAccount.previous_bes_sum = 0
                    for row in rows:
                        if row['account_id'] == account.id and row['costCenter_id'] == floatAccount.id:
                            floatAccount.bed_sum += row['bed_sum']
                            floatAccount.bes_sum += row['bes_sum']
                            floatAccount.opening_bed_sum = +row['opening_bed_sum']
                            floatAccount.opening_bes_sum = +row['opening_bes_sum']
                            floatAccount.previous_bed_sum = +row['previous_bed_sum']
                            floatAccount.previous_bes_sum = +row['previous_bes_sum']

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
                        'opening_bed_sum': floatAccount.opening_bed_sum,
                        'opening_bes_sum': floatAccount.opening_bes_sum,
                        'previous_bed_sum': floatAccount.previous_bed_sum,
                        'previous_bes_sum': floatAccount.previous_bes_sum,
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

            if level:
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
        AccountBalanceView._rows = None
        accounts = self.get_accounts(request)
        res = Response(BalanceAccountSerializer(accounts, many=True).data)
        return res


class AccountBalanceExportView(AccountBalanceView, BaseListExportView):
    filename = 'account-balance.pdf'
    template_name = 'export/simple_export.html'
    right_header_template = 'reports/balance_report_right_header.html'

    @property
    def title(self):
        cols_count = self.request.GET.get('cols_count')
        return "تراز {} ستونی حساب ها".format(cols_count)

    def get_rows(self):
        accounts = self.get_accounts(self.request)

        data = self.request.data
        show_float_accounts = data.get('show_float_accounts') == 'true',
        show_cost_centers = data.get('show_cost_centers') == 'true',

        rows = []
        for account in accounts:
            rows.append({
                'code': account.code,
                'name': account.name,
                **get_common_columns(account)
            })

            sub_items = []
            if show_float_accounts:
                sub_items += account.floatAccounts_data
            if show_cost_centers:
                sub_items += account.costCenters_data

            for item in sub_items:
                rows.append({
                    'code': '',
                    'name': item['name'],
                    **get_common_columns(item, True)
                })

        rows.append({
            'code': '',
            'name': 'جمع',
            **get_common_columns_sum(accounts)
        })

        return rows

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)
