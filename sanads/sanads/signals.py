from django.db.models import signals

from accounts.accounts.models import AccountBalance
from sanads.sanads.models import SanadItem


def updateAccountBalanceOnSave(sender, instance: SanadItem, **kwargs):
    account = instance.account
    bed = instance.bed
    bes = instance.bes

    if instance.id:
        sanadItem = SanadItem.objects.get(pk=instance.id)
        bed -= sanadItem.bed
        bes -= sanadItem.bes

    AccountBalance.update_balance(
        account=account,
        bed_change=bed,
        bes_change=bes,
        floatAccount=instance.floatAccount,
        costCenter=instance.costCenter
    )
    account.save()


def updateAccountBalanceOnDelete(sender, instance: SanadItem, **kwargs):
    account = instance.account
    bed = instance.bed
    bes = instance.bes

    AccountBalance.update_balance(
        account=account,
        bed_change=-bed,
        bes_change=-bes,
        floatAccount=instance.floatAccount,
        costCenter=instance.costCenter
    )
    account.save()


signals.pre_save.connect(receiver=updateAccountBalanceOnSave, sender=SanadItem)
signals.pre_delete.connect(receiver=updateAccountBalanceOnDelete, sender=SanadItem)
