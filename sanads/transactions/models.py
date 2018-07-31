from datetime import datetime
from django.db import models
from django.db.models import signals
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account, FloatAccount
from sanads.RPTypes.models import RPType
from sanads.sanads.models import Sanad
from sanads.transactions.autoSanad import *

TYPES = (
    ('receive', 'receive'),
    ('payment', 'payment'),
)


class Transaction(models.Model):
    code = models.IntegerField(unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactions')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='transactions', blank=True, null=True)
    date = jmodels.jDateField(blank=True)
    explanation = models.CharField(max_length=255, blank=True)
    sanad = models.ForeignKey(Sanad, on_delete=models.CASCADE, related_name='transaction', blank=True, null=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    type = models.CharField(max_length=20, choices=TYPES)

    permissions = (
        ('get_sanad', 'Can get sanads')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta:
        ordering = ['code', ]


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactionItems')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='transactionItems', blank=True, null=True)

    type = models.ForeignKey(RPType, on_delete=models.PROTECT)

    value = models.DecimalField(max_digits=24, decimal_places=0)

    date = jmodels.jDateField()

    documentNumber = models.CharField(max_length=50, blank=True)

    explanation = models.CharField(max_length=255, blank=True)

    file = models.FileField(blank=True, null=True)

    permissions = (
        ('get_sanad', 'Can get sanads')
    )

    def __str__(self):
        return self.explanation[0:30]


signals.post_save.connect(receiver=updateSanad, sender=Transaction)
signals.post_save.connect(receiver=updateSanadItems, sender=TransactionItem)
signals.post_delete.connect(receiver=clearSanad, sender=Transaction)
signals.post_delete.connect(receiver=updateSanadItems, sender=TransactionItem)

