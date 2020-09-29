from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account
from accounts.defaultAccounts.models import DefaultAccount
from factors.models import Factor, FactorItem
from helpers.auth import BasicCRUDPermission
from sanads.models import clearSanad, Sanad, newSanadCode
from wares.models import WareInventory


class DefiniteFactor(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_codename(self):
        if self.request.method.lower() == 'post' and 'item' in self.request.data:
            factor_data = self.request.data['item']
            factor_type = factor_data.get('type')
        else:
            factor_type = Factor.objects.get(pk=self.kwargs['pk']).type
        from factors.views.factorViews import get_factor_permission_basename

        return "definite.".format(get_factor_permission_basename(factor_type))

    def post(self, request, pk):
        user = request.user
        factor = DefiniteFactor.definiteFactor(user, pk, is_confirmed=request.data.get('_confirmed'))
        from factors.serializers import FactorListRetrieveSerializer
        return Response(FactorListRetrieveSerializer(factor).data)

    @staticmethod
    def undoDefinition(user, factor: Factor):
        sanad = DefiniteFactor.getFactorSanad(user, factor)
        clearSanad(sanad)

        sanad.is_auto_created = True
        factor.code = None
        factor.is_definite = False
        factor.save()

        for factor_item in factor.items.all():

            ware = factor_item.ware

            if ware.is_service:
                continue

            DefiniteFactor.updateInventory(factor_item, True)

            factor_item.fees = []
            factor_item.remain_fees = []
            factor_item.save()

    @staticmethod
    def definiteFactor(user, pk, is_confirmed=False):
        factor = get_object_or_404(Factor.objects.inFinancialYear(), pk=pk)
        from factors.views.factorViews import get_factor_permission_basename
        permission_codename = "definite.".format(get_factor_permission_basename(factor.type))
        user.has_object_perm(factor, permission_codename, raise_exception=True)

        sanad = DefiniteFactor.getFactorSanad(user, factor)
        factor.sanad = sanad
        factor.code = Factor.new_code(factor_type=factor.type)

        factor.is_definite = True
        if not factor.definition_date:
            factor.definition_date = now()

        factor.save()

        DefiniteFactor.updateFactorInventory(factor)

        first_row_bed = 0
        first_row_bes = 0

        second_row_bed = 0
        second_row_bes = 0

        if factor.type in Factor.SALE_GROUP:
            first_row_bed = factor.sum
            second_row_bes = factor.sum
            if factor.type == Factor.SALE:
                account = 'sale'
            else:
                account = 'backFromBuy'
        else:
            first_row_bes = factor.sum
            second_row_bed = factor.sum
            if factor.type == Factor.BUY:
                account = 'buy'
            else:
                account = 'backFromSale'

        explanation = "فاکتور {} شماره {} به تاریخ {} {} مشتری".format(
            factor.type_label,
            factor.code,
            str(factor.date),
            "از" if factor.type in Factor.BUY_GROUP else "به"
        )

        if factor.type != Factor.BACK_FROM_BUY:
            DefiniteFactor.submitSumSanadItems(
                user,
                factor,
                first_row_bed,
                first_row_bes,
                second_row_bed,
                second_row_bes,
                account,
                explanation
            )

        if factor.type == Factor.SALE:
            DefiniteFactor.submitSaleSanadItems(user, factor, explanation)
        elif factor.type == Factor.BACK_FROM_SALE:
            DefiniteFactor.submitBackFromSaleSanadItems(user, factor, explanation)
        elif factor.type == Factor.BACK_FROM_BUY:
            DefiniteFactor.submitBackFromBuySanadItems(user, factor, explanation)

        DefiniteFactor.submitDiscountSanadItems(
            user,
            factor,
            factor.discountSum if first_row_bed != 0 else 0,
            factor.discountSum if first_row_bes != 0 else 0,
            factor.discountSum if second_row_bed != 0 else 0,
            factor.discountSum if second_row_bes != 0 else 0,
            account,
            explanation
        )
        DefiniteFactor.submitTaxSanadItems(
            user,
            factor,
            factor.taxSum if first_row_bed != 0 else 0,
            factor.taxSum if first_row_bes != 0 else 0,
            factor.taxSum if second_row_bed != 0 else 0,
            factor.taxSum if second_row_bes != 0 else 0,
            account,
            explanation
        )
        DefiniteFactor.submitExpenseSanadItems(factor, explanation)

        if not is_confirmed:
            sanad.check_account_balance_confirmations()

        return factor

    @staticmethod
    def getFactorSanad(user, factor):
        if not factor.sanad:
            sanad = Sanad(
                code=newSanadCode(),
                date=factor.date,
                explanation=factor.explanation,
                financial_year=user.active_financial_year
            )
        else:
            sanad = factor.sanad
            clearSanad(sanad)
            sanad.date = factor.date
            sanad.is_auto_created = True
            sanad.explanation = factor.explanation
        sanad.save()

        return sanad

    @staticmethod
    def updateFactorInventory(factor: Factor, revert=False):
        for item in factor.items.order_by('id').all():
            DefiniteFactor.updateInventory(item, revert)

    @staticmethod
    def updateInventory(item: FactorItem, revert=False):

        factor = item.factor
        ware = item.ware
        warehouse = item.warehouse

        if item.ware.is_service:
            return

        is_used_in_next_years = FactorItem.objects.filter(
            factor__financial_year__start__gt=factor.financial_year.end,
            factor__type__in=Factor.OUTPUT_GROUP,
            ware=ware
        ).exists()

        if is_used_in_next_years:
            raise ValidationError("ابتدا فاکتور های سال مالی بعدی را پاک نمایید")

        if not revert:
            if factor.type in Factor.OUTPUT_GROUP:
                item.fees = WareInventory.decrease_inventory(ware, warehouse, item.count, factor.financial_year)
                item.save()

            elif factor.type in Factor.INPUT_GROUP:
                fee = item.fee
                if factor.type == Factor.BACK_FROM_SALE:
                    fee = float(WareInventory.get_remain_fees(ware)[-1]['fee'])
                item.fees = [{
                    'fee': float(fee),
                    'count': float(item.count)
                }]
                item.save()
                WareInventory.increase_inventory(ware, warehouse, item.count, fee, factor.financial_year)

        else:
            if item.factor.type in Factor.INPUT_GROUP:
                WareInventory.decrease_inventory(ware, warehouse, item.count, factor.financial_year, revert=True)
            else:
                fees = item.fees.copy()
                fees.reverse()
                for fee in fees:
                    WareInventory.increase_inventory(ware, warehouse, fee['count'], fee['fee'], factor.financial_year,
                                                     revert=True)

        item.remain_fees = WareInventory.get_remain_fees(item.ware)
        item.save()

    @staticmethod
    def submitSumSanadItems(user, factor, first_row_bed, first_row_bes, second_row_bed, second_row_bes, account,
                            explanation):
        sanad = factor.sanad
        if factor.sum:
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                costCenter=factor.costCenter,
                bed=first_row_bed,
                bes=first_row_bes,
                explanation=explanation,
            )

            sanad.items.create(
                account=DefaultAccount.get(account).account,
                floatAccount=DefaultAccount.get(account).floatAccount,
                costCenter=DefaultAccount.get(account).costCenter,
                bed=second_row_bed,
                bes=second_row_bes,
                explanation=explanation,
            )

    @staticmethod
    def submitDiscountSanadItems(user, factor, first_row_bed, first_row_bes, second_row_bed, second_row_bes, account,
                                 explanation):
        sanad = factor.sanad
        if factor.discountSum:
            sanad.items.create(
                account=DefaultAccount.get(account).account,
                floatAccount=DefaultAccount.get(account).floatAccount,
                costCenter=DefaultAccount.get(account).costCenter,
                bed=first_row_bed,
                bes=first_row_bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                costCenter=factor.costCenter,
                bed=second_row_bed,
                bes=second_row_bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )

    @staticmethod
    def submitTaxSanadItems(user, factor, first_row_bed, first_row_bes, second_row_bed, second_row_bes, account,
                            explanation):
        sanad = factor.sanad
        # Factor Tax Sum
        if factor.taxSum:
            sanad.items.create(
                account=factor.account,
                floatAccount=factor.floatAccount,
                costCenter=factor.costCenter,
                bed=first_row_bed,
                bes=first_row_bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )
            sanad.items.create(
                account=DefaultAccount.get('tax').account,
                floatAccount=DefaultAccount.get('tax').floatAccount,
                costCenter=DefaultAccount.get('tax').costCenter,
                bed=second_row_bed,
                bes=second_row_bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )

    @staticmethod
    def submitExpenseSanadItems(factor, explanation):
        sanad = factor.sanad
        for e in factor.expenses.all():
            if e.value:
                sanad.items.create(
                    account=e.expense.account,
                    floatAccount=e.expense.floatAccount,
                    costCenter=e.expense.costCenter,
                    bed=e.value,
                    explanation=explanation,
                    financial_year=sanad.financial_year
                )
                sanad.items.create(
                    account=e.account,
                    floatAccount=e.floatAccount,
                    costCenter=e.costCenter,
                    bes=e.value,
                    explanation=explanation,
                    financial_year=sanad.financial_year
                )

    @staticmethod
    def submitSaleSanadItems(user, factor, explanation):
        sanad = factor.sanad
        value = 0
        for item in factor.items.all():
            value += item.calculated_value

        sanad.items.create(
            account=Account.get_cost_of_sold_wares_account(user),
            bed=value,
            explanation=explanation,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            account=Account.get_inventory_account(user),
            bes=value,
            explanation=explanation,
            financial_year=sanad.financial_year
        )

    @staticmethod
    def submitBackFromSaleSanadItems(user, factor, explanation):
        sanad = factor.sanad
        value = 0

        for item in factor.items.all():
            value += item.calculated_value

        sanad.items.create(
            account=Account.get_inventory_account(user),
            bed=value,
            explanation=explanation,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            account=Account.get_cost_of_sold_wares_account(user),
            bes=value,
            explanation=explanation,
            financial_year=sanad.financial_year
        )

    @staticmethod
    def submitBackFromBuySanadItems(user, factor, explanation):
        sanad = factor.sanad
        value = 0
        for item in factor.items.all():
            value += item.calculated_value

        sanad.items.create(
            account=factor.account,
            floatAccount=factor.floatAccount,
            costCenter=factor.costCenter,
            bed=factor.sum,
            explanation=explanation,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            account=Account.get_inventory_account(user),
            bes=value,
            explanation=explanation,
            financial_year=sanad.financial_year
        )

        profit_and_loss_value = value - factor.sum
        if profit_and_loss_value:
            bed = 0
            bes = 0
            if profit_and_loss_value > 0:
                bed = profit_and_loss_value
            else:
                profit_and_loss_value = abs(profit_and_loss_value)
                bes = profit_and_loss_value

            sanad.items.create(
                account=DefaultAccount.get('profitAndLossFromBuying').account,
                floatAccount=DefaultAccount.get('profitAndLossFromBuying').floatAccount,
                costCenter=DefaultAccount.get('profitAndLossFromBuying').costCenter,
                bed=bed,
                bes=bes,
                explanation=explanation,
                financial_year=sanad.financial_year
            )
