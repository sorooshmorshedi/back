from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import FloatAccount, FloatAccountGroup
from helpers.auth import BasicCRUDPermission
from reports.balance.account_balance import get_common_columns_sum
from reports.filters import get_account_sanad_items_filter
from reports.lists.export_views import BaseListExportView


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
