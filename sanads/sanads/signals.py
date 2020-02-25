from django.db.models import signals
from cheques.models.StatusChangeModel import StatusChange
from sanads.sanads.models import SanadItem


# def updateAccountBalance(sender, instance: SanadItem, created, **kwargs):
#     account = instance.account
#
#
#
#
# signals.post_save.connect(receiver=updateAccountBalance, sender=SanadItem)
