import jdatetime
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account, AccountType, AccountBalance
from accounts.defaultAccounts.models import getDefaultAccount
from companies.models import FinancialYear
from factors.models import Factor
from factors.views.firstPeriodInventoryViews import FirstPeriodInventoryView
from sanads.sanads.models import SanadItem, clearSanad
from users.serializers import UserSerializer
from wares.models import WareInventory


class ClosingHelpers:
    @staticmethod
    def create_sanad_items_with_balance(sanad, accounts=None, reverse=False):
        sanad_items = []

        qs = AccountBalance.objects.inFinancialYear()
        if accounts:
            qs = qs.filter(account__in=accounts)

        balances = qs.all()

        for balance in balances:
            remain = balance.bed - balance.bes
            bed = bes = 0
            if remain > 0:
                bed = remain
            else:
                bes = remain

            if reverse:
                bed, bes = bes, bed

            if bed == bes == 0:
                continue

            item = SanadItem(
                financial_year=sanad.financial_year,
                sanad=sanad,
                account=balance.account,
                floatAccount=balance.floatAccount,
                costCenter=balance.costCenter,
                bed=bed,
                bes=bes
            )

            item.save()
            sanad_items.append(item)

        return sanad_items

    @staticmethod
    def balance_sanad(sanad, defaultAccount):

        sanad_remain = sanad.bed - sanad.bes
        bed = bes = 0
        if sanad_remain > 0:
            bed = sanad_remain
        elif sanad_remain < 0:
            bes = sanad_remain

        current_earnings_default_account = getDefaultAccount(defaultAccount)

        item = SanadItem(
            financial_year=sanad.financial_year,
            sanad=sanad,
            account=current_earnings_default_account.account,
            floatAccount=current_earnings_default_account.floatAccount,
            costCenter=current_earnings_default_account.costCenter,
            bed=bed,
            bes=bes
        )

        item.save()

        return item

    @staticmethod
    def create_first_period_inventory(target_financial_year):

        first_period_inventory = Factor.get_first_period_inventory(target_financial_year)
        if first_period_inventory:
            first_period_inventory.delete()

        data = {
            'factor': {
                'date': jdatetime.date.today(),
                'time': jdatetime.datetime.now(),
            },
            'factor_items': {
                'items': [],
                'ids_to_delete': []
            }
        }

        items = []

        WareInventory.objects.inFinancialYear(target_financial_year).delete()
        for inventory in WareInventory.objects.inFinancialYear().all():
            items.append({
                'fee': inventory.fee,
                'ware': inventory.ware.id,
                'warehouse': inventory.warehouse.id,
                'count': inventory.count,
            })

        data['factor_items']['items'] = items

        FirstPeriodInventoryView.set_first_period_inventory(data, target_financial_year)


class CloseFinancialYearView(APIView):
    sanad = None

    def post(self, request):
        data = request.data
        user = request.user

        current_financial_year = user.active_financial_year
        # target_financial_year = get_object_or_404(FinancialYear, pk=data.get('target_financial_year'))
        target_financial_year = FinancialYear.objects.get(pk=189)

        if Factor.objects.inFinancialYear(target_financial_year).filter(code__gte=1, is_definite=True).exists():
            raise ValidationError("ابتدا فاکتور های قطعی سال مالی جدید را پاک نمایید")

        self.sanad = current_financial_year.get_closing_sanad()
        clearSanad(self.sanad)

        self.add_temporaries_sanad_items()

        self.add_current_earnings_sanad_item()

        self.add_retained_earnings_sanad_item()

        self.add_permanents_sanad_items()

        self.add_closing_sanad_item()

        self.create_opening_sanad(target_financial_year)

        ClosingHelpers.create_first_period_inventory(target_financial_year)

        return Response(UserSerializer(request.user).data)

    def add_temporaries_sanad_items(self):
        accounts = Account.objects \
            .filter(type__usage=AccountType.INCOME_STATEMENT) \
            .all()

        sanad_items = ClosingHelpers.create_sanad_items_with_balance(self.sanad, accounts, reverse=True)

        return sanad_items

    def add_current_earnings_sanad_item(self):
        sanad_item = ClosingHelpers.balance_sanad(self.sanad, 'currentEarnings')
        return [sanad_item]

    def add_retained_earnings_sanad_item(self):
        sanad_item = ClosingHelpers.balance_sanad(self.sanad, 'retainedEarnings')
        return [sanad_item]

    def add_permanents_sanad_items(self):
        accounts = Account.objects \
            .filter(type__usage__in=[AccountType.BALANCE_SHEET, None, AccountType.NONE]) \
            .all()

        sanad_items = ClosingHelpers.create_sanad_items_with_balance(self.sanad, accounts, reverse=True)
        return sanad_items

    def add_closing_sanad_item(self):
        sanad_item = ClosingHelpers.balance_sanad(self.sanad, 'closing')
        return [sanad_item]

    def create_opening_sanad(self, target_financial_year):
        accounts = Account.objects \
            .filter(type__usage__in=[AccountType.BALANCE_SHEET, None, AccountType.NONE]) \
            .all()

        sanad = target_financial_year.get_opening_sanad()
        clearSanad(sanad)
        sanad_items = ClosingHelpers.create_sanad_items_with_balance(sanad, accounts, reverse=False)

        return sanad_items


class CancelFinancialYearClosingView(APIView):

    def post(self, request):
        financial_year = request.user.active_financial_year
        closing_sanad = financial_year.closingSanad
        if closing_sanad:
            closing_sanad.delete()

        return Response(UserSerializer(request.user).data)


class MoveFinancialYearView(APIView):
    sanad = None

    def post(self, request):
        # target_financial_year = get_object_or_404(FinancialYear, pk=data.get('target_financial_year'))
        target_financial_year = FinancialYear.objects.get(pk=189)

        self.sanad = target_financial_year.get_opening_sanad()

        self.move_accounts()

        ClosingHelpers.create_first_period_inventory(target_financial_year)

        return Response(UserSerializer(request.user).data)

    def move_accounts(self):
        sanad_items = ClosingHelpers.create_sanad_items_with_balance(self.sanad)
        return sanad_items
