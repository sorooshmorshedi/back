from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.accounts.models import AccountType, Account
from accounts.accounts.serializers import TypeReportAccountSerializer


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


@api_view(['get'])
def incomeStatementView(request):

    getType.accountTypes = AccountType.objects.all()

    res = []
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

    allAccounts = list(Account.objects.inFinancialYear(request.user) \
        .annotate(remain=
            Coalesce(Sum('sanadItems__value', filter=Q(sanadItems__valueType='bed') & dateFilter), 0) -
            Coalesce(Sum('sanadItems__value', filter=Q(sanadItems__valueType='bes') & dateFilter), 0)
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

    operatingIncome = operatingCosts - grossIncome
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


