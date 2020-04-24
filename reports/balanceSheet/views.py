from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import AccountType, Account
from accounts.accounts.serializers import TypeReportAccountSerializer
from helpers.auth import BasicCRUDPermission

from reports.filters import get_account_sanad_items_filter


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


class BalanceSheetView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.balanceSheetReport'

    def get(self, request):
        # print(len(connection.queries))
        res = {}
        dateFilter = get_account_sanad_items_filter(request)

        allAccounts = Account.objects.inFinancialYear() \
            .annotate(remain=
                      Coalesce(Sum('sanadItems__bed', filter=dateFilter), 0) -
                      Coalesce(Sum('sanadItems__bes', filter=dateFilter), 0)
                      ).filter(level=3).order_by('code')

        accountTypes = AccountType.objects.filter(usage='balanceSheet')

        for at in accountTypes:
            remain = getRemain(at, allAccounts)
            res[at.programingName] = {
                'name': at.name,
                'remain': remain,
                'accounts': TypeReportAccountSerializer(getAccounts(at, allAccounts), many=True).data
            }

        remain = res['cacheAndBank']['remain'] \
                 + res['shortTimeInvestments']['remain'] \
                 + res['commercialAccountsAndReceivables']['remain'] \
                 + res['otherAccountsAndReceivables']['remain'] \
                 + res['inventories']['remain'] \
                 + res['ordersAndPrepayments']['remain']
        res['totalCurrentAssets'] = {
            'name': 'جمع دارایی های جاری',
            'remain': remain
        }

        remain = res['evidentFixedAssets']['remain'] \
                 + res['notEvidentAssets']['remain'] \
                 + res['longTimeInvestments']['remain'] \
                 + res['otherAssets']['remain']
        res['totalNotCurrentAssets'] = {
            'name': 'جمع دارایی های غیر جاری',
            'remain': remain
        }

        remain = res['totalCurrentAssets']['remain'] \
                 + res['totalNotCurrentAssets']['remain']
        res['totalAssets'] = {
            'name': 'جمع دارایی ها',
            'remain': remain
        }

        remain = res['businessAccountsAndPayableDocuments']['remain'] \
                 + res['otherAccountsAndPayableDocuments']['remain'] \
                 + res['prepayments']['remain'] \
                 + res['saveTypes']['remain'] \
                 + res['paidDividends']['remain'] \
                 + res['receivableFunds']['remain']
        res['totalCurrentDebt'] = {
            'name': 'جمع بدهی های جاری',
            'remain': remain
        }

        remain = res['longtermAccountsAndPayableDocuments']['remain'] \
                 + res['longtermReceivableFunds']['remain'] \
                 + res['savedEndingServiceBenefits']['remain']
        res['totalNotCurrentDebt'] = {
            'name': 'جمع بدهی های غیر جاری',
            'remain': remain
        }

        remain = res['totalCurrentDebt']['remain'] \
                 + res['totalNotCurrentDebt']['remain']
        res['totalDebt'] = {
            'name': 'جمع بدهی ها',
            'remain': remain
        }

        remain = res['fund']['remain'] \
                 + res['savings']['remain'] \
                 + res['accumulatedProfit']['remain']
        res['equitiesSum'] = {
            'name': 'جمع حقوق صاحبان سهام',
            'remain': remain
        }

        remain = res['equitiesSum']['remain'] \
                 + res['totalDebt']['remain']
        res['totalDebtsAndEquities'] = {
            'name': 'جمع بدهی ها و حقوق صاحبان سهام',
            'remain': remain
        }
        # print(len(connection.queries))

        return Response(res)
