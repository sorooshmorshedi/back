from django.db.models import signals

from sanads.sanads.models import SanadItem


def updateAccountBalanceOnSave(sender, instance: SanadItem, **kwargs):
    account = instance.account
    bed = instance.bed
    bes = instance.bes

    if instance.id:
        sanadItem = SanadItem.objects.get(pk=instance.id)
        bed -= sanadItem.bed
        bes -= sanadItem.bes

    account.bed += bed
    account.bes += bes
    account.save()


def updateAccountBalanceOnDelete(sender, instance: SanadItem, **kwargs):
    account = instance.account
    bed = instance.bed
    bes = instance.bes

    account.bed -= bed
    account.bes -= bes
    account.save()


signals.pre_save.connect(receiver=updateAccountBalanceOnSave(), sender=SanadItem)
signals.pre_delete.connect(receiver=updateAccountBalanceOnDelete(), sender=SanadItem)
