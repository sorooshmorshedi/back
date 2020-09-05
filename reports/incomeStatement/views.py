from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import AccountType, Account
from accounts.accounts.serializers import TypeReportAccountSerializer
from helpers.auth import BasicCRUDPermission
from helpers.exports import get_xlsx_response
from reports.filters import get_account_sanad_items_filter


def getType(pName):
    return list(filter(lambda at: at.codename == pName, getType.accountTypes))[0]


def getAccounts(accountType, allAccounts):
    return filter(lambda acc: acc.type_id == accountType.id, allAccounts)


def getRemain(accountType, allAccounts):
    accounts = getAccounts(accountType, allAccounts)
    remain = 0
    for acc in accounts:
        if accountType.nature == 'bed':
            remain += acc.remain
        else:
            remain -= acc.remain
    return remain


def getSerialized(pName, allAccounts):
    account_type = getType(pName)
    remain = getRemain(account_type, allAccounts)

    subPrefix = (
        'backFromSaleAndDiscounts',
        'soldProductValue',
        'operatingCosts',
        'nonOperatingCosts',
    )

    addPrefix = (
        'nonOperatingIncomes',
    )

    hasPrefix = False
    prefix = ''
    prefixColor = None

    if account_type.codename in subPrefix:
        hasPrefix = True
        prefix = 'کسر می شود:'
        prefixColor = 'red'

    if account_type.codename in addPrefix:
        hasPrefix = True
        prefix = 'اضافه می شود:'
        prefixColor = 'blue'

    return {
        'type': {
            'name': account_type.name,
            'hasPrefix': hasPrefix,
            'pName': account_type.codename,
            'prefix': prefix,
            'prefixColor': prefixColor
        },
        'remain': remain,
        'accounts': TypeReportAccountSerializer(getAccounts(account_type, allAccounts), many=True).data
    }


class IncomeStatementView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.incomeStatementReport'

    def generate_report(self, request):
        getType.accountTypes = AccountType.objects.all()

        rows = []
        dateFilter = get_account_sanad_items_filter(request)

        allAccounts = list(Account.objects.inFinancialYear() \
                           .annotate(remain=
                                     Coalesce(Sum('sanadItems__bed', filter=dateFilter), 0) -
                                     Coalesce(Sum('sanadItems__bes', filter=dateFilter), 0)
                                     ).filter(level=3).order_by('code'))

        t = getSerialized('sale', allAccounts)
        rows.append(t)
        sale = t['remain']

        t = getSerialized('backFromSaleAndDiscounts', allAccounts)
        rows.append(t)
        backFromSaleAndDiscounts = t['remain']

        netSales = sale - backFromSaleAndDiscounts
        t = ({
            'type': {
                'name': 'فروش خالص',
                'prefix': '',
                'pName': None
            },
            'remain': netSales,
        })
        rows.append(t)

        t = getSerialized('soldProductValue', allAccounts)
        soldProductValue = t['remain']
        rows.append(t)

        grossIncome = netSales - soldProductValue
        t = ({
            'type': {
                'name': 'سود (زیان) ناخالص',
                'prefix': '',
                'pName': None
            },
            'remain': grossIncome,
        })
        rows.append(t)

        t = getSerialized('operatingCosts', allAccounts)
        operatingCosts = t['remain']
        rows.append(t)

        operatingIncome = grossIncome - operatingCosts
        t = ({
            'type': {
                'name': 'سود (زیان) عملیاتی',
                'prefix': '',
                'pName': None
            },
            'remain': operatingIncome
        })
        rows.append(t)

        t = getSerialized('nonOperatingIncomes', allAccounts)
        nonOperatingIncomes = t['remain']
        rows.append(t)

        t = getSerialized('nonOperatingCosts', allAccounts)
        nonOperatingCosts = t['remain']
        rows.append(t)

        specialIncome = operatingIncome \
                        + nonOperatingIncomes \
                        - nonOperatingCosts
        t = ({
            'type': {
                'name': 'سود (زیان) ویژه',
                'prefix': '',
                'pName': None
            },
            'remain': specialIncome
        })
        rows.append(t)

        return rows

    def get(self, request):
        res = self.generate_report(request)
        res = Response(res)
        return res


class IncomeStatementExportView(IncomeStatementView):
    def get(self, request, **kwargs):
        rows = [[
            "#",
            "شرح",
            "مبلغ",
        ]]

        i = 0
        data = self.generate_report(request)
        get_detailed = request.GET.get('detailed') == 'true'

        if get_detailed:
            rows[0].append("")

        for row in data:
            i += 1
            rows.append([
                i,
                "{} {}".format(row['type']['prefix'], row['type']['name']),
                row['remain']
            ])

            if get_detailed and 'accounts' in row:
                j = 0
                for account in row['accounts']:
                    j += 1
                    rows.append([
                        "",
                        j,
                        account['title'],
                        account['remain']
                    ])

        return get_xlsx_response("Income Statement", rows)
