from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import AccountType, Account
from accounts.accounts.serializers import TypeReportAccountSerializer
from helpers.auth import BasicCRUDPermission
from reports.filters import get_account_sanad_items_filter


def getType(pName):
    return list(filter(lambda at: at.programingName == pName, getType.accountTypes))[0]


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
    at = getType(pName)
    remain = getRemain(at, allAccounts)

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
    prefix = None
    prefixColor = None

    if at.programingName in subPrefix:
        hasPrefix = True
        prefix = 'کسر می شود:'
        prefixColor = 'red'

    if at.programingName in addPrefix:
        hasPrefix = True
        prefix = 'اضافه می شود:'
        prefixColor = 'blue'

    return {
        'type': {
            'name': at.name,
            'hasPrefix': hasPrefix,
            'pName': at.programingName,
            'prefix': prefix,
            'prefixColor': prefixColor
        },
        'remain': remain,
        'accounts': TypeReportAccountSerializer(getAccounts(at, allAccounts), many=True).data
    }


class IncomeStatementView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.incomeStatementReport'

    def get(self, request):
        getType.accountTypes = AccountType.objects.all()

        res = []
        dateFilter = get_account_sanad_items_filter(request)

        allAccounts = list(Account.objects.inFinancialYear() \
                           .annotate(remain=
                                     Coalesce(Sum('sanadItems__bed', filter=dateFilter), 0) -
                                     Coalesce(Sum('sanadItems__bes', filter=dateFilter), 0)
                                     ).filter(level=3).order_by('code'))

        usingTypes = (
            'sale',
            'backFromSaleAndDiscounts',
            'soldProductValue',
            'operatingCosts',
            'nonOperatingIncomes',
            'nonOperatingCosts',
        )

        t = getSerialized('sale', allAccounts)
        res.append(t)
        sale = t['remain']

        t = getSerialized('backFromSaleAndDiscounts', allAccounts)
        res.append(t)
        backFromSaleAndDiscounts = t['remain']

        netSales = sale - backFromSaleAndDiscounts
        t = ({
            'type': {
                'name': 'فروش خالص',
                'pName': None
            },
            'remain': netSales,
        })
        res.append(t)

        t = getSerialized('soldProductValue', allAccounts)
        soldProductValue = t['remain']
        res.append(t)

        grossIncome = netSales - soldProductValue
        t = ({
            'type': {
                'name': 'سود (زیان) ناخالص',
                'pName': None
            },
            'remain': grossIncome,
        })
        res.append(t)

        t = getSerialized('operatingCosts', allAccounts)
        operatingCosts = t['remain']
        res.append(t)

        operatingIncome = grossIncome - operatingCosts
        t = ({
            'type': {
                'name': 'سود (زیان) عملیاتی',
                'pName': None
            },
            'remain': operatingIncome
        })
        res.append(t)

        t = getSerialized('nonOperatingIncomes', allAccounts)
        nonOperatingIncomes = t['remain']
        res.append(t)

        t = getSerialized('nonOperatingCosts', allAccounts)
        nonOperatingCosts = t['remain']
        res.append(t)

        specialIncome = operatingIncome \
                        + nonOperatingIncomes \
                        - nonOperatingCosts
        t = ({
            'type': {
                'name': 'سود (زیان) ویژه',
                'pName': None
            },
            'remain': specialIncome
        })
        res.append(t)

        res = Response(res)
        return res
