from django.db.models import Q
from django.db.models import Sum
from django.db.models.expressions import F
from django.db.models.functions import Coalesce
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from wkhtmltopdf.views import PDFTemplateView

from accounts.accounts.models import Account, FloatAccount, FloatAccountGroup
from accounts.accounts.serializers import AccountTypeSerializer
from helpers.auth import BasicCRUDPermission
from helpers.exports import get_xlsx_response, MPDFTemplateView
from reports.balance.serializers import BalanceAccountSerializer, BalanceFloatAccountSerializer, \
    BalanceFloatAccountGroupSerializer
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

    def get_accounts(self, request):
        filters = get_account_sanad_items_filter(request)
        account_code_starts_with = request.GET.get('account_code_starts_with', '')
        level = request.GET.get('level', None)
        account_type = request.GET.get('account_type')
        balance_status = request.GET.get('balance_status')

        show_differences = request.GET.get('show_differences')

        qs = Account.objects.inFinancialYear().annotate(
            bed_sum=Coalesce(Sum('sanadItems__bed', filter=filters), 0),
            bes_sum=Coalesce(Sum('sanadItems__bes', filter=filters), 0)
        )

        qs = qs.filter(code__startswith=account_code_starts_with, )

        if level:
            qs = qs.filter(level=level)

        if balance_status == 'with_remain':
            qs = qs.filter(~Q(bed_sum=F('bes_sum')))
        elif balance_status == 'without_remain':
            qs = qs.filter(bed_sum=F('bes_sum'))
        elif balance_status == 'bed_remain':
            qs = qs.filter(bed_sum__gt=F('bes_sum'))
        elif balance_status == 'bes_remain':
            qs = qs.filter(bes_sum__gt=F('bed_sum'))
        elif balance_status == 'with_transaction':
            qs = qs.filter(~Q(bes_sum=0, bed_sum=0))
        elif balance_status == 'without_transaction':
            qs = qs.filter(bes_sum=0, bed_sum=0)

        if account_type == Account.BUYER:
            qs = qs.filter(account_type=Account.PERSON, buyer_or_seller=Account.BUYER)
        elif account_type == Account.SELLER:
            qs = qs.filter(account_type=Account.PERSON, buyer_or_seller=Account.SELLER)
        elif account_type == Account.BANK:
            qs = qs.filter(account_type=Account.BANK)

        accounts = qs.prefetch_related(
            'floatAccountGroup', 'costCenterGroup', 'type'
        ).order_by('code')

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
                account.type_data = AccountTypeSerializer(account.type).data
            if account.floatAccountGroup:
                account.floatAccountGroup_data = BalanceFloatAccountGroupSerializer(account.floatAccountGroup).data
            if account.costCenterGroup:
                account.costCenterGroup_data = BalanceFloatAccountGroupSerializer(account.costCenterGroup).data

            account.floatAccounts_data = []
            account.costCenters_data = []
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
                    account.floatAccounts_data.append(BalanceFloatAccountSerializer(floatAccount).data)

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
                    account.costCenters_data.append(BalanceFloatAccountSerializer(floatAccount).data)

        accounts = list(accounts)
        for account in accounts:
            if show_differences:
                nature = account.type.nature
                if (
                        account.bed_remain == account.bes_remain == 0
                ) or (
                        nature == 'bed' and account.bes_remain != 0
                ) or (
                        nature == 'bes' and account.bed_remain != 0
                ):
                    accounts.remove(account)

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
