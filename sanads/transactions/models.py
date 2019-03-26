from django.db import models
from django.db.models import signals, Sum
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account, FloatAccount
from accounts.defaultAccounts.models import DefaultAccount
from sanads.transactions.autoSanad import *

from cheques.models import Cheque


class Transaction(models.Model):
    RECEIVE = 'receive'
    PAYMENT = 'payment'
    TYPES = (
        (RECEIVE, 'دریافت'),
        (PAYMENT, 'پرداخت'),
    )

    code = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactions')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='transactions', blank=True, null=True)
    date = jmodels.jDateField()
    explanation = models.CharField(max_length=255, blank=True)
    sanad = models.OneToOneField(Sanad, on_delete=models.CASCADE, related_name='transaction', blank=True, null=True)

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
        unique_together = ('code', 'type')

    @property
    def sum(self):
        return TransactionItem.objects.filter(transaction=self).aggregate(Sum('value'))['value__sum']

    @property
    def label(self):
        return [t[1] for t in self.TYPES if t[0] == self.type][0]


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactionItems')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='transactionItems', blank=True, null=True)
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='transactionItem', blank=True, null=True)

    type = models.ForeignKey(DefaultAccount, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=24, decimal_places=0)
    date = jmodels.jDateField()
    due = jmodels.jDateField(null=True, blank=True)
    documentNumber = models.CharField(max_length=50, blank=True)
    bankName = models.CharField(max_length=255, blank=True)
    explanation = models.CharField(max_length=255, blank=True)

    file = models.FileField(blank=True, null=True)

    permissions = (
        ('get_sanad', 'Can get sanads')
    )

    def __str__(self):
        return "{0} - {1}".format(self.transaction.code, self.explanation[0:30])


signals.post_save.connect(receiver=updateSanad, sender=Transaction)
signals.post_save.connect(receiver=updateSanadItems, sender=TransactionItem)
signals.post_delete.connect(receiver=clearTransactionSanad, sender=Transaction)
signals.post_delete.connect(receiver=updateSanadItems, sender=TransactionItem)

