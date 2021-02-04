import jdatetime
from django.db import connection
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.views import APIView

from _dashtbashi.models import Lading
from _dashtbashi.sanads import LadingSanad
from accounts.accounts.models import Account, FloatAccountRelation, FloatAccountGroup, FloatAccount
from accounts.accounts.views import AccountListCreate, SanadItem
from companies.models import FinancialYear
# from helpers.db import select_raw_sql
from sanads.models import Sanad, newSanadCode
from users.models import User


class TestApiView(APIView):

    def get(self, request):

        for lading in Lading.objects.all():
            LadingSanad(lading).update()

        return Response([])
        # self.add_floatAccounts()
        # self.update_sanad_items()

        rows = select_raw_sql("""
            select account_id, \"floatAccount_id\", \"costCenter_id\", sum(bed)
            from sanads_sanaditem
            group by account_id, \"floatAccount_id\", \"costCenter_id\"
        """)
        print(len(rows))
        for i in rows[:10]:
            print(i)
        return Response([])

    def update_sanad_items(self):
        financial_year = FinancialYear.objects.get(pk=2)
        sanad_items = SanadItem.objects.inFinancialYear(financial_year).filter(floatAccount=None).all()[:1000]
        count = sanad_items.count()
        print(count)
        for sanad_item in sanad_items:
            print('sanad item ', sanad_item.id)
            if sanad_item.account.floatAccountGroup:
                sanad_item.floatAccount = sanad_item.account.floatAccountGroup.floatAccounts.first()
            sanad_item.save()

    def add_floatAccounts(self):
        financial_year = FinancialYear.objects.get(pk=2)
        accounts = Account.objects.inFinancialYear(financial_year).filter(level=3).all()
        float_accounts = FloatAccount.objects.inFinancialYear(financial_year).all()
        for account in accounts:
            print('account', account.id)
            float_account_group = FloatAccountGroup.objects.create(
                financial_year=financial_year,
                is_cost_center=False,
                name="گروه شناور {}"
            )
            for float_account in float_accounts:
                FloatAccountRelation.objects.create(
                    financial_year=financial_year,
                    floatAccountGroup=float_account_group,
                    floatAccount=float_account
                )
            account.floatAccountGroup = float_account_group
            account.save()

    def create_accounts(self):
        financial_year = FinancialYear.objects.get(pk=2)
        accounts = Account.objects.inFinancialYear(financial_year).filter(level=2).all()
        accounts_count = len(accounts)
        for i in range(500):
            print(i)
            factory = APIRequestFactory()
            request = factory.post('/accounts/accounts', {
                'account_type': 'o',
                'parent': accounts[i % accounts_count].id,
                'name': 'حساب تست #{}'.format(i)
            })
            force_authenticate(request, user=User.objects.get(pk=1))
            view = AccountListCreate.as_view()
            view(request)

    def create_sanads(self):
        financial_year = FinancialYear.objects.get(pk=2)
        accounts = Account.objects.inFinancialYear(financial_year).filter(level=3).all()[:100]
        accounts_count = len(accounts)

        for i in range(10000):
            sanad = Sanad.objects.create(
                financial_year=financial_year,
                code=newSanadCode(),
                date=jdatetime.date.today()
            )
            for j in range(10):
                if i % 2 == 0:
                    bed = 1000
                    bes = 0
                else:
                    bed = 0
                    bes = 1000
                sanad.items.create(
                    financial_year=financial_year,
                    account=accounts[i * j % accounts_count],
                    bed=bed,
                    bes=bes
                )
