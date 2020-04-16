import jdatetime
from accounts.accounts.models import Account, FloatAccount
from sanads.sanads.models import newSanadCode, Sanad, SanadItem
from users.models import User

from helpers.test import MTestCase


class SanadTest(MTestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.first()

    @staticmethod
    def create_sanad(financial_year):
        sanad = Sanad.objects.create(
            code=newSanadCode(financial_year),
            financial_year=financial_year,
            date=jdatetime.date.today(),
        )
        return sanad

    @staticmethod
    def create_sanad_item(
            sanad: Sanad,
            account: Account,
            floatAccount: FloatAccount = None,
            costCenter: FloatAccount = None,
            bed=0,
            bes=0
    ):

        if account.floatAccountGroup and not floatAccount:
            floatAccount = account.floatAccountGroup.floatAccounts.first()
        if account.costCenterGroup and not costCenter:
            costCenter = account.costCenterGroup.floatAccounts.first()

        sanad_item = SanadItem.objects.create(
            sanad=sanad,
            financial_year=sanad.financial_year,
            account=account,
            floatAccount=floatAccount,
            costCenter=costCenter,
            bed=bed,
            bes=bes
        )
        return sanad_item
