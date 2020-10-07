from helpers.auto_sanad import AutoSanad
from helpers.functions import get_object_accounts
from imprests.models import ImprestSettlement


class ImprestSettlementSanad(AutoSanad):
    def perform_update(self, instance: ImprestSettlement, sanad):
        sanad_items = []
        for item in instance.items.all():
            sanad_items.append({
                'bed': item.value,
                **get_object_accounts(item)
            })

        sanad_items.append({
            'bes': instance.settled_value,
            **get_object_accounts(instance.transaction)
        })

        self.create_sanad_items(sanad, sanad_items)
