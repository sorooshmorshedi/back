from django.db.models import signals

from accounts.accounts.models import AccountBalance
from helpers.functions import get_object_accounts
from sanads.models import SanadItem


def updateAccountBalanceOnSave(sender, instance: SanadItem, **kwargs):
    if instance.sanad.is_defined:
        if instance.id:
            sanadItem = SanadItem.objects.get(pk=instance.id)
            AccountBalance.update_balance(
                financial_year=instance.financial_year,
                **get_object_accounts(sanadItem),
                bed_change=-sanadItem.bed,
                bes_change=-sanadItem.bes,
            )

        AccountBalance.update_balance(
            financial_year=instance.financial_year,
            **get_object_accounts(instance),
            bed_change=instance.bed,
            bes_change=instance.bes
        )


def updateAccountBalanceOnDelete(sender, instance: SanadItem, **kwargs):
    account = instance.account
    bed = instance.bed
    bes = instance.bes

    AccountBalance.update_balance(
        financial_year=instance.financial_year,
        account=account,
        bed_change=-bed,
        bes_change=-bes,
        floatAccount=instance.floatAccount,
        costCenter=instance.costCenter
    )
    account.save()


signals.pre_save.connect(receiver=updateAccountBalanceOnSave, sender=SanadItem)
signals.pre_delete.connect(receiver=updateAccountBalanceOnDelete, sender=SanadItem)
