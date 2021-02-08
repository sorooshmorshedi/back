from typing import List
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account, FloatAccount, FloatAccountGroup
from helpers.auth import BasicCRUDPermission
from helpers.db import select_raw_sql
from helpers.exports import get_xlsx_response
from helpers.functions import to_gregorian
from reports.balance.serializers import BalanceAccountSerializer
from reports.filters import get_account_sanad_items_filter
from reports.lists.export_views import BaseExportView, BaseListExportView

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

    def get_rows(self):

        if self._rows:
            return self._rows

        request = self.request
        data = request.GET

        where_filters = "true and "
        if data.get('from_date'):
            where_filters += "sanad.date >= '{}' and ".format(to_gregorian(data['from_date']))
        if data.get('to_date'):
            where_filters += "sanad.date <= '{}' and ".format(to_gregorian(data['to_date']))
        if data.get('from_code'):
            where_filters += "sanad.code >= {} and ".format(data['from_code'])
        if data.get('to_code'):
            where_filters += "sanad.code <= {} and ".format(data['to_code'])
        if data.get('skip_closing_sanad', False) == 'true':
            financial_year = request.user.active_financial_year
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

        self._rows = select_raw_sql(sql)
        return self._rows

    def set_remain(self, account: Account, accounts: List[Account]):

        if hasattr(account, 'bed_sum'):
            return

        account.bed_sum = 0
        account.bes_sum = 0
        account.bed_remain = 0
        account.bes_remain = 0

        if account.level == Account.TAFSILI:
            rows = self.get_rows()
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
        show_differences = False

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

            rows = self.get_rows()

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


class FloatAccountBalanceByGroupView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.floatAccountBalanceByGroupReport'

    @property
    def is_cost_center(self):
        return self.request.GET.get('is_cost_center') == 'true'

    def get_accounts_data(self, request):

        filters = get_account_sanad_items_filter(request)

        floatAccounts = FloatAccount.objects.inFinancialYear().filter(is_cost_center=self.is_cost_center)
        floatAccountGroups = FloatAccountGroup.objects.inFinancialYear().prefetch_related(
            'floatAccounts').filter(is_cost_center=self.is_cost_center)

        if self.is_cost_center:
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


class FloatAccountBalanceByGroupExportView(FloatAccountBalanceByGroupView, BaseListExportView):
    filename = None

    @property
    def title(self):
        if self.is_cost_center:
            return "تراز مراکز هزینه بر اساس گروه"
        else:
            return "تراز حساب های شناور بر اساس گروه"

    def get_headers(self):
        if self.is_cost_center:
            text = "مرکز هزینه و درآمد"
        else:
            text = "حساب شناو"
        headers = [
            {
                "text": "گروه " + text,
                "value": "group_name",
            },
            {
                "text": text,
                "value": "float_account_name",
            },
            {
                "text": "گردش بدهکار",
                "value": "bed_sum",
                "type": "numeric",
            },
            {
                "text": "گردش بستانکار",
                "value": "bes_sum",
                "type": "numeric",
            },
            {
                "text": "مانده بدهکار",
                "value": "bed_remain",
                "type": "numeric",
            },
            {
                "text": "مانده بستانکار",
                "value": "bes_remain",
                "type": "numeric",
            },
        ]
        return headers

    def get_rows(self):
        accounts_data = list(self.get_accounts_data(self.request))

        rows_sum = get_common_columns_sum(accounts_data, True)
        accounts_data.append({
            'group_name': '',
            'float_account_name': 'جمع',
            'bed_sum': rows_sum[0],
            'bes_sum': rows_sum[1],
            'bed_remain': rows_sum[2],
            'bes_remain': rows_sum[3],
        })
        return accounts_data

    def get(self, request, *args, **kwargs):

        if self.is_cost_center:
            self.filename = "Cost & Income Center By Group Balance"
        else:
            self.filename = "Float By Group Balance"

        return self.get_response(request, *args, **kwargs)


class FloatAccountBalanceView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.floatAccountBalanceReport'

    @property
    def is_cost_center(self):
        return self.request.GET.get('is_cost_center') == 'true'

    def get_accounts_data(self, request):
        filters = get_account_sanad_items_filter(request)

        if self.is_cost_center:
            sanad_item_key = "sanadItemsAsCostCenter"
        else:
            sanad_item_key = "sanadItems"

        floatAccounts = FloatAccount.objects.inFinancialYear().annotate(
            bed_sum=Coalesce(Sum('{}__bed'.format(sanad_item_key), filter=filters), 0),
            bes_sum=Coalesce(Sum('{}__bes'.format(sanad_item_key), filter=filters), 0),
        ).filter(is_cost_center=self.is_cost_center)

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


class FloatAccountBalanceExportView(FloatAccountBalanceView, BaseListExportView):
    filename = None

    @property
    def title(self):
        if self.is_cost_center:
            return "تراز مراکز هزینه"
        else:
            return "تراز حساب های شناور"

    def get_headers(self):
        if self.is_cost_center:
            text = "مرکز هزینه و درآمد"
        else:
            text = "حساب شناور"
        headers = [
            {
                "text": text,
                "value": "float_account_name",
            },
            {
                "text": "گردش بدهکار",
                "value": "bed_sum",
                "type": "numeric",
            },
            {
                "text": "گردش بستانکار",
                "value": "bes_sum",
                "type": "numeric",
            },
            {
                "text": "مانده بدهکار",
                "value": "bed_remain",
                "type": "numeric",
            },
            {
                "text": "مانده بستانکار",
                "value": "bes_remain",
                "type": "numeric",
            },
        ]
        return headers

    def get_rows(self):
        accounts_data = list(self.get_accounts_data(self.request))

        rows_sum = get_common_columns_sum(accounts_data, True)
        accounts_data.append({
            'float_account_name': 'جمع',
            'bed_sum': rows_sum[0],
            'bes_sum': rows_sum[1],
            'bed_remain': rows_sum[2],
            'bes_remain': rows_sum[3],
        })
        return accounts_data

    def get(self, request, *args, **kwargs):

        if self.is_cost_center:
            self.filename = "Cost & Income Center Balance"
        else:
            self.filename = "Float Balance"

        return self.get_response(request, *args, **kwargs)
