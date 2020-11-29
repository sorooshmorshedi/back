from helpers.models import BaseModel
from sanads.models import Sanad, newSanadCode, clearSanad


class AutoSanad:
    """
        IMPORTANT NOTE: Shouldn't call in `Model.save` method
    """

    def __init__(self, instance):
        self.instance = instance

    def get_sanad(self, date=None):
        sanad = self.instance.sanad
        if not sanad:
            sanad = Sanad.objects.create(
                code=newSanadCode(),
                financial_year=self.instance.financial_year,
                date=date or self.instance.date
            )
            self.instance.sanad = sanad
            self.instance.save()
        else:
            clearSanad(sanad)
            sanad.is_auto_created = True
            sanad.save()
        return sanad

    def update(self, **kwargs):
        sanad = self.get_sanad(**kwargs)
        self.perform_update(self.instance, sanad)
        sanad.update_values()

    def perform_update(self, instance: BaseModel, sanad):
        raise NotImplementedError()

    @staticmethod
    def create_sanad_items(sanad, sanad_items):
        """
        :param sanad: Sanad
        :param sanad_items: array[{any field of SanadItem}, ...]
        :return: None
        """

        for sanad_item in sanad_items:
            if sanad_item.get('bed', 0) == sanad_item.get('bes', 0) == 0:
                continue

            sanad.items.create(
                **sanad_item
            )
