import jdatetime
from django.db.models import QuerySet, Q
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account, AccountType, AccountBalance
from accounts.defaultAccounts.models import DefaultAccount
from companies.models import FinancialYear, CompanyUser, FinancialYearOperation
from companies.serializers import FinancialYearSerializer
from factors.management.commands.refresh_inventory import Command
from factors.models import Factor
from factors.views.firstPeriodInventoryViews import FirstPeriodInventoryView
from helpers.auth import BasicCRUDPermission
from home.models import DefaultText
from sanads.models import SanadItem, clearSanad, Sanad
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

        account = DefaultAccount.get(defaultAccount)

        item = SanadItem(
            financial_year=sanad.financial_year,
            sanad=sanad,
            account=account.account,
            floatAccount=account.floatAccount,
            costCenter=account.costCenter,
            bed=bed,
            bes=bes
        )

        item.save()

        return item

    @staticmethod
    def create_first_period_inventory(user, target_financial_year):

        first_period_inventory = Factor.get_first_period_inventory(target_financial_year)
        if first_period_inventory:
            first_period_inventory.delete()

        opening_default_account = DefaultAccount.get('opening')
        account = opening_default_account.account.id
        if opening_default_account.floatAccount:
            float_account = opening_default_account.floatAccount.id
        else:
            float_account = None
        if opening_default_account.costCenter:
            cost_center = opening_default_account.costCenter.id
        else:
            cost_center = None

        data = {
            'item': {
                'type': Factor.FIRST_PERIOD_INVENTORY,
                'account': account,
                'floatAccount': float_account,
                'costCenter': cost_center,
                'date': target_financial_year.start,
                'time': '00:00',
            },
            'items': {
                'items': [],
                'ids_to_delete': []
            }
        }

        items = []

        # WareInventory.objects.inFinancialYear(target_financial_year).delete()
        for inventory in WareInventory.objects.inFinancialYear().all():
            has_similar = False
            for item in items:
                if (
                        item['fee'] == inventory.fee
                        and item['ware'] == inventory.ware.id
                        and item['warehouse'] == inventory.warehouse.id
                ):
                    item['count'] += inventory.count
                    item['unit_count'] += inventory.count
                    has_similar = True

            if not has_similar:
                items.append({
                    'fee': inventory.fee,
                    'ware': inventory.ware.id,
                    'unit': inventory.ware.main_unit.id,
                    'warehouse': inventory.warehouse.id,
                    'count': inventory.count,
                    'unit_count': inventory.count,
                })

        data['items']['items'] = items

        FirstPeriodInventoryView.set_first_period_inventory(
            data,
            target_financial_year,
            engage_inventory=False,
            submit_sanad=False,
            is_auto_created=True
        )
        Command.refresh_inventory(user, target_financial_year)

    @staticmethod
    def verify_password(user: User, password):
        is_valid = user.check_password(password)
        if not is_valid:
            raise ValidationError(["کلمه عبور غیر قابل قبول می باشد"])


class CloseFinancialYearView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'close.financialYear'

    sanad = None

    def post(self, request):
        data = request.data
        user = request.user

        ClosingHelpers.verify_password(user, data.get('password'))

        target_financial_year = get_object_or_404(FinancialYear, pk=data.get('target_financial_year'))

        user.has_object_perm(user.active_financial_year, self.permission_codename, raise_exception=True)

        if Factor.objects.inFinancialYear(target_financial_year).filter(code__gte=1, is_defined=True).exists():
            raise ValidationError("ابتدا فاکتور های قطعی سال مالی جدید را پاک نمایید")

        CloseFinancialYearView.close_financial_year(user, target_financial_year)

        return Response(UserListRetrieveSerializer(request.user).data)

    @staticmethod
    def close_financial_year(user: User, target_financial_year: FinancialYear):
        current_financial_year = user.active_financial_year

        current_financial_year.check_closing_sanads()

        sanad = current_financial_year.temporaryClosingSanad
        clearSanad(sanad)
        sanad.is_auto_created = True
        sanad.type = Sanad.CLOSING
        sanad.explanation = "سند اختتامیه"
        CloseFinancialYearView.add_temporaries_sanad_items(sanad)
        sanad.update_values()
        CloseFinancialYearView.add_current_earnings_sanad_item(sanad)
        sanad.define()
        sanad.save()
        sanad.update_values()

        sanad = current_financial_year.currentEarningsClosingSanad
        clearSanad(sanad)
        sanad.is_auto_created = True
        sanad.type = Sanad.CLOSING
        sanad.explanation = "سند اختتامیه"
        CloseFinancialYearView.add_retained_earnings_sanad_item(sanad)
        sanad.define()
        sanad.save()
        sanad.update_values()

        sanad = current_financial_year.permanentsClosingSanad
        clearSanad(sanad)
        sanad.is_auto_created = True
        sanad.type = Sanad.CLOSING
        sanad.explanation = "سند اختتامیه"
        CloseFinancialYearView.add_permanents_sanad_items(sanad)
        sanad.update_values()
        CloseFinancialYearView.add_closing_sanad_item(sanad)
        sanad.define()
        sanad.save()
        sanad.update_values()

        CloseFinancialYearView.create_opening_sanad(current_financial_year, target_financial_year)

        ClosingHelpers.create_first_period_inventory(user, target_financial_year)

        FinancialYearOperation.objects.create(
            fromFinancialYear=current_financial_year,
            toFinancialYear=target_financial_year,
            operation=FinancialYearOperation.CLOSE_AND_MOVE
        )

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
        current_earnings_default_account = DefaultAccount.get('currentEarnings').account
        sanad_items = ClosingHelpers.create_sanad_items_with_balance(
            sanad,
            [current_earnings_default_account],
            reverse=True
        )
        sanad.update_values()
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
        closing_account_default_account = DefaultAccount.get('closing')

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
        sanad.is_auto_created = True
        sanad.type = Sanad.OPENING
        sanad.explanation = "سند افتتاحیه"
        sanad.date = target_financial_year.start
        sanad.save()

        opening_default_account = DefaultAccount.get('opening')
        closing_default_account = DefaultAccount.get('closing')

        sanad_items = []
        for sanad_item in current_financial_year.permanentsClosingSanad.items.all():
            sanad_item.id = None
            sanad_item.sanad = sanad
            sanad_item.bed, sanad_item.bes = sanad_item.bes, sanad_item.bed
            sanad_item.explanation = "سند افتتاحیه"

            if sanad_item.account == closing_default_account.account:
                sanad_item.account = opening_default_account.account
                sanad_item.floatAccount = opening_default_account.floatAccount
                sanad_item.costCenter = opening_default_account.costCenter

            sanad_item.save()

            sanad_items.append(sanad_item)

        sanad.define()
        sanad.update_values()

        return sanad_items


class CancelFinancialYearClosingView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'cancelClosing.financialYear'

    def post(self, request):
        financial_year = request.user.active_financial_year

        user = request.user
        data = request.data

        ClosingHelpers.verify_password(user, data.get('password'))

        user.has_object_perm(financial_year, self.permission_codename, raise_exception=True)

        if financial_year.is_closed():
            financial_year.delete_closing_sanads()
            financial_year.refresh_from_db()

        FinancialYearOperation.objects.create(
            fromFinancialYear=financial_year,
            toFinancialYear=None,
            operation=FinancialYearOperation.CANCEL_CLOSE
        )

        target_financial_year = FinancialYearOperation.objects.filter(
            fromFinancialYear=financial_year,
            operation=FinancialYearOperation.CLOSE_AND_MOVE
        ).latest().toFinancialYear
        sanad = target_financial_year.get_opening_sanad()
        clearSanad(sanad)
        sanad.is_auto_created = True
        sanad.save()

        return Response(UserListRetrieveSerializer(user).data)


class MoveFinancialYearView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'move.financialYear'
    sanad = None

    def post(self, request):
        user = request.user
        data = request.data

        ClosingHelpers.verify_password(user, data.get('password'))

        current_financial_year = user.active_financial_year
        target_financial_year = get_object_or_404(FinancialYear, pk=data.get('target_financial_year'))

        request.user.has_object_perm(current_financial_year, self.permission_codename, raise_exception=True)

        self.move_accounts(target_financial_year)

        ClosingHelpers.create_first_period_inventory(user, target_financial_year)

        FinancialYearOperation.objects.create(
            fromFinancialYear=current_financial_year,
            toFinancialYear=target_financial_year,
            operation=FinancialYearOperation.MOVE
        )

        return Response(UserListRetrieveSerializer(request.user).data)

    def move_accounts(self, target_financial_year):
        sanad = target_financial_year.get_opening_sanad()
        clearSanad(sanad)
        sanad_items = ClosingHelpers.create_sanad_items_with_balance(sanad)
        return sanad_items


class FinancialYearModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'financialYear'
    serializer_class = FinancialYearSerializer

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        company = user.active_company

        if user == company.superuser:
            return company.financial_years.all()
        else:
            company_user = CompanyUser.objects.get(company=company, user=user)
            qs = company_user.financialYears.all()
            return qs

    def perform_create(self, serializer: FinancialYearSerializer) -> None:
        serializer.save(
            company=self.request.user.active_company
        )
        self.copy_data(serializer.instance)

    def copy_data(self, new_financial_year: FinancialYear):

        try:
            if new_financial_year.is_advari:
                base_financial_year = FinancialYear.objects.get(pk=116)
            else:
                base_financial_year = FinancialYear.objects.get(pk=117)
        except FinancialYear.DoesNotExist:
            if new_financial_year.is_advari:
                base_financial_year = FinancialYear.objects.get(pk=2)
            else:
                base_financial_year = FinancialYear.objects.get(pk=3)

        """
            Be careful about models with relationships
        """

        """
            Copying accounts
        """
        accounts_map = {}
        if Account.objects.inFinancialYear(new_financial_year).count() == 0:
            base_accounts = Account.objects.inFinancialYear(base_financial_year).order_by('level').all()
            for account in base_accounts:
                key = account.pk

                account.pk = None
                account.financial_year = new_financial_year
                if account.parent:
                    account.parent_id = accounts_map[account.parent_id]

                account.save()

                accounts_map[key] = account.pk

        """
            Copying default accounts
        """
        if DefaultAccount.objects.inFinancialYear(new_financial_year).count() == 0:
            for item in DefaultAccount.objects.inFinancialYear(base_financial_year).all():
                item.pk = None
                item.financial_year = new_financial_year
                if item.account_id in accounts_map:
                    item.account_id = accounts_map[item.account_id]
                item.save()

        """
            Copying default texts
        """

        if DefaultText.objects.inFinancialYear(new_financial_year).count() == 0:
            for item in DefaultText.objects.inFinancialYear(base_financial_year).all():
                item.pk = None
                item.financial_year = new_financial_year
                item.save()
