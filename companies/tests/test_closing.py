import jdatetime
from accounts.accounts.models import Account, FloatAccount, AccountBalance
from companies.tests.test_financial_years import FinancialYearTest
from companies.views.financialYear import CloseFinancialYearView
from sanads.sanads.models import newSanadCode, Sanad, SanadItem
from sanads.tests.test_sanads import SanadTest
from users.models import User

from helpers.test import MTestCase


class ClosingTest(MTestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.first()
        cls.user = user

        cls.bank_account = Account.objects.get(code='101010001')
        cls.ware_inventory_account = Account.objects.get(code='106040001')
        cls.person_account = Account.objects.get(code='103010002')
        cls.ware_sale_account = Account.objects.get(code='601020001')
        cls.ware_cost_account = Account.objects.get(code='701010001')
        cls.income_account = Account.objects.get(code='601020002')
        cls.receivable_account = Account.objects.get(code='103010005')
        cls.fund_account = Account.objects.get(code='501010001')
        cls.current_earnings_account = Account.objects.get(code='505020001')
        cls.retained_earnings_account = Account.objects.get(code='505010002')

    def test_closing(self):
        self.client.force_authenticate(self.user)

        sanad = SanadTest.create_sanad(self.user.active_financial_year)

        SanadTest.create_sanad_item(sanad, self.ware_inventory_account, bed=2000)
        SanadTest.create_sanad_item(sanad, self.bank_account, bes=2000)

        SanadTest.create_sanad_item(sanad, self.person_account, bed=1200)
        SanadTest.create_sanad_item(sanad, self.ware_cost_account, bed=1000)
        SanadTest.create_sanad_item(sanad, self.ware_sale_account, bes=1200)
        SanadTest.create_sanad_item(sanad, self.ware_inventory_account, bes=1000)

        SanadTest.create_sanad_item(sanad, self.receivable_account, bed=500)
        SanadTest.create_sanad_item(sanad, self.income_account, bes=500)

        SanadTest.create_sanad_item(sanad, self.bank_account, bed=5000)
        SanadTest.create_sanad_item(sanad, self.fund_account, bes=5000)

        # for balance in AccountBalance.objects.all():
        #     print(balance.account.title)
        #     print(' - ', balance.bed, balance.bes)
        # print("---------------------")

        target_financial_year = FinancialYearTest.create_financial_year(self.user.active_company)
        CloseFinancialYearView.close_financial_year(self.user, target_financial_year)

        current_financial_year = self.user.active_financial_year

        sanad = current_financial_year.temporaryClosingSanad
        for sanad_item in sanad.items.all():
            print(sanad_item.account.title)
            print(' - ', sanad_item.bed, sanad_item.bes)

        print('-----------')
        sanad = current_financial_year.currentEarningsClosingSanad
        for sanad_item in sanad.items.all():
            print(sanad_item.account.title)
            print(' - ', sanad_item.bed, sanad_item.bes)

        print('-----------')
        sanad = current_financial_year.permanentsClosingSanad
        for sanad_item in sanad.items.all():
            print(sanad_item.account.title)
            print(' - ', sanad_item.bed, sanad_item.bes)

        # target_financial_year.currentEarningsClosingSanad
        # target_financial_year.permanentsClosingSanad
