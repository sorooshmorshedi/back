from helpers.auto_sanad import AutoSanad
from helpers.functions import get_object_accounts, sanad_exp
from imprests.models import ImprestSettlement


class ImprestSettlementSanad(AutoSanad):
    def perform_update(self, instance: ImprestSettlement, sanad):
        sanad.explanation = sanad_exp(
            'بابت تسویه',
            instance.explanation,
            'از محل تنخواه شماره',
            instance.transaction.code,
            'مورخ',
            instance.transaction.date
        )

        sanad_items = []
        for item in instance.items.all():
            sanad_items.append({
                'bed': item.value,
                **get_object_accounts(item),
                'explanation': sanad_exp(
                    'بابت',
                    instance.explanation,
                    'مورخ',
                    instance.transaction.date,
                    'از محل تنخواه شماره',
                    instance.transaction.code,
                )
            })

        sanad_items.append({
            'bes': instance.settled_value,
            **get_object_accounts(instance.transaction),
            'explanation': sanad_exp(
                'بابت تسویه',
                instance.explanation,
                'از محل تنخواه شماره',
                instance.transaction.code,
            )
        })

        self.create_sanad_items(sanad, sanad_items)
