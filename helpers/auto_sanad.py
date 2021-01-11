from accounts.defaultAccounts.models import DefaultAccount
from helpers.functions import get_object_accounts
from helpers.models import BaseModel
from sanads.models import Sanad, newSanadCode, clearSanad


class AutoSanad:
    """
        How to use:
         1. Inherit from this class
         2. Implement

        IMPORTANT NOTE: Don't call update method in `Model.save` method
    """

    def __init__(self, instance):
        self.instance = instance

    def get_sanad_date(self):
        return self.instance.date

    def get_sanad_explanation(self):
        return self.instance.explanation

    def get_sanad_rows(self, instance: BaseModel) -> list:
        raise NotImplementedError()

    def update(self, is_confirmed=True):
        sanad = self._get_sanad()
        rows = self.get_sanad_rows(self.instance)
        self._create_sanad_items(sanad, rows)
        sanad.update_values()

        if not is_confirmed:
            sanad.check_account_balance_confirmations()

        self.instance.sanad = sanad
        self.instance.save()

    def _get_sanad(self):
        sanad = self.instance.sanad
        if not sanad:
            sanad = Sanad.objects.create(
                code=newSanadCode(),
                financial_year=self.instance.financial_year,
                date=self.get_sanad_date(),
                explanation=self.get_sanad_explanation(),
                is_auto_created=True,
            )
            self.instance.sanad = sanad
            self.instance.save()
        else:
            clearSanad(sanad)
            sanad.is_auto_created = True
            sanad.date = self.get_sanad_date()
            sanad.explanation = self.get_sanad_explanation()
            sanad.save()
        return sanad

    def _create_sanad_items(self, sanad: Sanad, sanad_items: list):
        """
        :param sanad: Sanad
        :param sanad_items: array[{any field of SanadItem}, ...]
        # You can pass default accounts as string!
        :return: None
        """

        for sanad_item in sanad_items:
            if isinstance(sanad_item['account'], str):
                sanad_item.update(get_object_accounts(DefaultAccount.get(sanad_item['account'])))
            sanad_item['bed'] = sanad_item.get('bed', 0)
            sanad_item['bes'] = sanad_item.get('bes', 0)

        for sanad_item in sanad_items:
            if sanad_item['bed'] == sanad_item['bes'] == 0:
                continue

            sanad.items.create(
                **sanad_item
            )
