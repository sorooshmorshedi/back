import jdatetime
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account, AccountType, AccountBalance
from accounts.defaultAccounts.models import getDefaultAccount
from companies.models import FinancialYear
from companies.serializers import FinancialYearSerializer
from factors.models import Factor
from factors.views.firstPeriodInventoryViews import FirstPeriodInventoryView
from helpers.auth import BasicCRUDPermission
from sanads.models import SanadItem, clearSanad
from users.models import User
from users.serializers import UserListRetrieveSerializer
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
                bes = -remain

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
        if sanad_remain < 0:
            bed = -sanad_remain
        elif sanad_remain > 0:
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
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'close.financialYear'

    sanad = None

    def post(self, request):
        data = request.data
        user = request.user

        target_financial_year = get_object_or_404(FinancialYear, pk=data.get('target_financial_year'))

        if Factor.objects.inFinancialYear(target_financial_year).filter(code__gte=1, is_definite=True).exists():
            raise ValidationError("ابتدا فاکتور های قطعی سال مالی جدید را پاک نمایید")

        CloseFinancialYearView.close_financial_year(user, target_financial_year)

        return Response(UserListRetrieveSerializer(request.user).data)

    @staticmethod
    def close_financial_year(user: User, target_financial_year: FinancialYear):
        current_financial_year = user.active_financial_year

        current_financial_year.check_closing_sanads()

        sanad = current_financial_year.temporaryClosingSanad
        clearSanad(sanad)
        CloseFinancialYearView.add_temporaries_sanad_items(sanad)
        CloseFinancialYearView.add_current_earnings_sanad_item(sanad)
        sanad.save()

        sanad = current_financial_year.currentEarningsClosingSanad
        clearSanad(sanad)
        CloseFinancialYearView.add_retained_earnings_sanad_item(sanad)
        sanad.save()

        sanad = current_financial_year.permanentsClosingSanad
        clearSanad(sanad)
        CloseFinancialYearView.add_permanents_sanad_items(sanad)
        CloseFinancialYearView.add_closing_sanad_item(sanad)
        sanad.save()

        CloseFinancialYearView.create_opening_sanad(current_financial_year, target_financial_year)

        ClosingHelpers.create_first_period_inventory(target_financial_year)

    @staticmethod
    def add_temporaries_sanad_items(sanad):
        accounts = Account.objects \
            .filter(type__usage=AccountType.INCOME_STATEMENT) \
            .all()

        sanad_items = ClosingHelpers.create_sanad_items_with_balance(sanad, accounts, reverse=True)

        return sanad_items

    @staticmethod
    def add_current_earnings_sanad_item(sanad):
        sanad_item = ClosingHelpers.balance_sanad(sanad, 'currentEarnings')
        return [sanad_item]

    @staticmethod
    def add_retained_earnings_sanad_item(sanad):
        current_earnings_default_account = getDefaultAccount('currentEarnings').account
        sanad_items = ClosingHelpers.create_sanad_items_with_balance(
            sanad,
            [current_earnings_default_account],
            reverse=True
        )
        sanad_items.append(ClosingHelpers.balance_sanad(sanad, 'retainedEarnings'))
        return sanad_items

    @staticmethod
    def add_permanents_sanad_items(sanad):
        accounts = Account.objects \
            .filter(type__usage__in=[AccountType.BALANCE_SHEET, None, AccountType.NONE]) \
            .all()

        sanad_items = ClosingHelpers.create_sanad_items_with_balance(sanad, accounts, reverse=True)
        return sanad_items

    @staticmethod
    def add_closing_sanad_item(sanad):
        closing_account_default_account = getDefaultAccount('closing')

        sanad_items = []

        bed = sanad.bed
        bes = sanad.bes

        item = SanadItem(
            financial_year=sanad.financial_year,
            sanad=sanad,
            account=closing_account_default_account.account,
            floatAccount=closing_account_default_account.floatAccount,
            costCenter=closing_account_default_account.costCenter,
            bed=bes,
            bes=0
        )
        item.save()
        sanad_items.append(item)

        item = SanadItem(
            financial_year=sanad.financial_year,
            sanad=sanad,
            account=closing_account_default_account.account,
            floatAccount=closing_account_default_account.floatAccount,
            costCenter=closing_account_default_account.costCenter,
            bed=0,
            bes=bed
        )
        item.save()
        sanad_items.append(item)

        return sanad_items

    @staticmethod
    def create_opening_sanad(current_financial_year, target_financial_year):

        sanad = target_financial_year.get_opening_sanad()
        clearSanad(sanad)

        opening_default_account = getDefaultAccount('opening')
        closing_default_account = getDefaultAccount('closing')

        sanad_items = []
        for sanad_item in current_financial_year.permanentsClosingSanad.items.all():
            sanad_item.id = None
            sanad_item.sanad = sanad
            sanad_item.bed, sanad_item.bes = sanad_item.bes, sanad_item.bed

            if sanad_item.account == closing_default_account.account:
                sanad_item.account = opening_default_account.account
                sanad_item.floatAccount = opening_default_account.floatAccount
                sanad_item.costCenter = opening_default_account.costCenter

            sanad_item.save()

            sanad_items.append(sanad_item)

        return sanad_items


class CancelFinancialYearClosingView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'cancelClosing.financialYear'

    def post(self, request):
        financial_year = request.user.active_financial_year
        if financial_year.is_closed:
            financial_year.delete_closing_sanads()

        return Response(UserListRetrieveSerializer(request.user).data)


class MoveFinancialYearView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'move.financialYear'
    sanad = None

    def post(self, request):
        target_financial_year = get_object_or_404(FinancialYear, pk=data.get('target_financial_year'))

        self.sanad = target_financial_year.get_opening_sanad()

        self.move_accounts()

        ClosingHelpers.create_first_period_inventory(target_financial_year)

        return Response(UserListRetrieveSerializer(request.user).data)

    def move_accounts(self):
        sanad_items = ClosingHelpers.create_sanad_items_with_balance(self.sanad)
        return sanad_items


class FinancialYearModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'financialYear'
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer