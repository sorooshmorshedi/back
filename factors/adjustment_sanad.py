from accounts.accounts.models import Account
from companies.models import FinancialYear
from factors.models import Factor
from helpers.auto_sanad import AutoSanad
from helpers.models import BaseModel


class AdjustmentSanad(AutoSanad):

    def get_sanad_rows(self, instance: BaseModel) -> list:

        user = instance.created_by
        adjustment_type = instance.type
        factor = instance.factor

        items = []
        for item in factor.items.all():
            if adjustment_type == Factor.INPUT_ADJUSTMENT:
                items += [
                    {'account': Account.get_inventory_account(user), 'bed': item.calculated_value},
                ]
                if instance.financial_year.warehouse_system == FinancialYear.DAEMI:
                    items += [
                        {'account': Account.get_cost_of_sold_wares_account(user), 'bes': item.calculated_value},
                    ]
                else:
                    items += [
                        {'account': 'warehouseDeductionAndAddition', 'bes': item.calculated_value},
                    ]
            elif adjustment_type == Factor.OUTPUT_ADJUSTMENT:
                items += [
                    {'account': Account.get_inventory_account(user), 'bes': item.calculated_value},
                ]

                if instance.financial_year.warehouse_system == FinancialYear.DAEMI:
                    items += [
                        {'account': Account.get_cost_of_sold_wares_account(user), 'bed': item.calculated_value},
                    ]
                else:
                    items += [
                        {'account': 'warehouseDeductionAndAddition', 'bed': item.calculated_value},
                    ]

        return items
