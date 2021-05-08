from rest_framework.exceptions import ValidationError
from accounts.accounts.models import Account
from companies.models import FinancialYear
from factors.models import Factor
from helpers.auto_sanad import AutoSanad
from helpers.functions import get_object_accounts
from helpers.models import BaseModel


class FactorSanad(AutoSanad):

    def get_sanad_rows(self, instance: BaseModel) -> list:
        if instance.type == Factor.SALE:
            items = [
                {**get_object_accounts(instance), 'bed': instance.sum, 'explanation': self.get_sanad_explanation()},
                {'account': 'sale', 'bes': instance.sum, 'explanation': self.get_sanad_explanation()},
            ]
            if instance.financial_year.warehouse_system == FinancialYear.DAEMI:
                items += [
                    {'account': Account.get_cost_of_sold_wares_account(instance.created_by),
                     'bed': instance.calculated_sum, 'explanation': self.get_sanad_explanation()},
                    {'account': Account.get_inventory_account(instance.created_by), 'bes': instance.calculated_sum,
                     'explanation': self.get_sanad_explanation()},
                ]
            items += [
                {'account': 'sale', 'bed': instance.discountSum, 'explanation': self.get_sanad_explanation()},
                {**get_object_accounts(instance), 'bes': instance.discountSum,
                 'explanation': self.get_sanad_explanation()},

                {**get_object_accounts(instance), 'bed': instance.taxSum, 'explanation': self.get_sanad_explanation()},
                {'account': 'tax', 'bes': instance.taxSum, 'explanation': self.get_sanad_explanation()}
            ]
        elif instance.type == Factor.BACK_FROM_BUY:
            if instance.financial_year.warehouse_system == FinancialYear.DAEMI:
                profit_and_loss_value = instance.calculated_sum - instance.sum
                bed = bes = 0
                if profit_and_loss_value > 0:
                    bed = profit_and_loss_value
                else:
                    bes = -profit_and_loss_value
                items = [
                    {**get_object_accounts(instance), 'bed': instance.sum, 'explanation': self.get_sanad_explanation()},
                    {'account': Account.get_inventory_account(instance.created_by), 'bes': instance.calculated_sum,
                     'explanation': self.get_sanad_explanation()},
                    {'account': 'profitAndLossFromBuying', 'bed': bed, 'bes': bes,
                     'explanation': self.get_sanad_explanation()},
                ]
            else:
                items = [
                    {**get_object_accounts(instance), 'bed': instance.sum, 'explanation': self.get_sanad_explanation()},
                    {'account': Account.get_inventory_account(instance.created_by), 'bes': instance.sum,
                     'explanation': self.get_sanad_explanation()},
                ]
            items += [

                {'account': 'backFromBuy', 'bed': instance.discountSum, 'explanation': self.get_sanad_explanation()},
                {**get_object_accounts(instance), 'bes': instance.discountSum,
                 'explanation': self.get_sanad_explanation()},

                {**get_object_accounts(instance), 'bed': instance.taxSum, 'explanation': self.get_sanad_explanation()},
                {'account': 'tax', 'bes': instance.taxSum, 'explanation': self.get_sanad_explanation()}
            ]
        elif instance.type in (Factor.BUY, Factor.PRODUCTION):
            items = [
                {**get_object_accounts(instance), 'bes': instance.sum, 'explanation': self.get_sanad_explanation()},
                {'account': 'buy', 'bed': instance.sum, 'explanation': self.get_sanad_explanation()},
                {'account': 'buy', 'bes': instance.discountSum, 'explanation': self.get_sanad_explanation()},
                {**get_object_accounts(instance), 'bed': instance.discountSum,
                 'explanation': self.get_sanad_explanation()},
                {**get_object_accounts(instance), 'bes': instance.taxSum, 'explanation': self.get_sanad_explanation()},
                {'account': 'tax', 'bed': instance.taxSum, 'explanation': self.get_sanad_explanation()}
            ]
        elif instance.type == Factor.BACK_FROM_SALE:
            items = [
                {**get_object_accounts(instance), 'bes': instance.sum, 'explanation': self.get_sanad_explanation()},
                {'account': 'backFromSale', 'bed': instance.sum, 'explanation': self.get_sanad_explanation()},
            ]

            if instance.financial_year.warehouse_system == FinancialYear.DAEMI:
                items += [
                    {'account': Account.get_inventory_account(instance.created_by), 'bed': instance.calculated_sum,
                     'explanation': self.get_sanad_explanation()},
                    {'account': Account.get_cost_of_sold_wares_account(instance.created_by),
                     'bes': instance.calculated_sum, 'explanation': self.get_sanad_explanation()},
                ]

            items += [
                {'account': 'backFromSale', 'bes': instance.discountSum, 'explanation': self.get_sanad_explanation()},
                {**get_object_accounts(instance), 'bed': instance.discountSum,
                 'explanation': self.get_sanad_explanation()},
                {**get_object_accounts(instance), 'bes': instance.taxSum, 'explanation': self.get_sanad_explanation()},
                {'account': 'tax', 'bed': instance.taxSum, 'explanation': self.get_sanad_explanation()}
            ]
        elif instance.type == Factor.CONSUMPTION_WARE:
            items = [
                {**get_object_accounts(instance), 'bed': instance.calculated_sum,
                 'explanation': self.get_sanad_explanation()},
                {'account': Account.get_inventory_account(instance.created_by), 'bes': instance.calculated_sum,
                 'explanation': self.get_sanad_explanation()},
            ]
        elif instance.type == Factor.FIRST_PERIOD_INVENTORY:
            items = [
                {'account': Account.get_inventory_account(instance.created_by), 'bed': instance.sum,
                 'explanation': self.get_sanad_explanation()},
                {**get_object_accounts(instance), 'bes': instance.sum, 'explanation': self.get_sanad_explanation()},
            ]
        else:
            raise ValidationError("نوع فاکتور صحیح نمی باشد")

        for factor_expense in instance.expenses.all():
            items += [
                {**get_object_accounts(factor_expense.expense), 'bed': factor_expense.value,
                 'explanation': self.get_sanad_explanation()},
                {**get_object_accounts(factor_expense), 'bes': factor_expense.value,
                 'explanation': self.get_sanad_explanation()}
            ]

        return items

    def get_sanad_explanation(self):
        return "فاکتور {} شماره {} به تاریخ {} {} مشتری".format(
            self.instance.type_label,
            self.instance.code,
            str(self.instance.date),
            "از" if self.instance.type in Factor.BUY_GROUP else "به",
            " - ",
            self.instance.explanation
        )
