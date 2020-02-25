from django.db import models
from django_jalali.db import models as jmodels
from accounts.accounts.models import Account, FloatAccount
from cheques.models.ChequebookModel import Chequebook
from companies.models import FinancialYear
from helpers.models import BaseModel

CHEQUE_STATUSES = (
    ('blank', 'blank'),
    ('notPassed', 'notPassed'),
    ('inFlow', 'inFlow'),
    ('passed', 'passed'),
    ('bounced', 'bounced'),
    ('cashed', 'cashed'),
    ('revoked', 'revoked'),
    ('transferred', 'transferred'),
    ('', 'any'),
)


class Cheque(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='cheques')

    RECEIVED = 'r'
    PAID = 'p'

    PERSONAL = 'p'
    COMPANY = 'c'
    OTHER_PERSON = 'op'
    OTHER_COMPANY = 'oc'

    CHEQUE_TYPES = (
        (PERSONAL, 'شخصی'),
        (OTHER_PERSON, 'شخصی سایرین'),
        (COMPANY, 'شرکت'),
        (OTHER_COMPANY, 'شرکت سایرین')
    )
    serial = models.CharField(max_length=255)
    chequebook = models.ForeignKey(Chequebook, on_delete=models.CASCADE, related_name='cheques', blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='receivedCheques', blank=True,
                                null=True)
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='receivedCheques', blank=True,
                                     null=True)

    value = models.DecimalField(max_digits=24, decimal_places=0, blank=True, null=True)
    due = jmodels.jDateField(blank=True, null=True)
    date = jmodels.jDateField(blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, choices=CHEQUE_STATUSES)
    received_or_paid = models.CharField(max_length=10, choices=((RECEIVED, 'دریافتنی'), (PAID, 'پرداختنی')))
    type = models.CharField(max_length=1, choices=CHEQUE_TYPES, blank=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    lastAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='lastCheques', blank=True,
                                    null=True)
    lastFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='lastCheques', blank=True,
                                         null=True)

    bankName = models.CharField(max_length=100, null=True, blank=True)
    branchName = models.CharField(max_length=100, null=True, blank=True)
    accountNumber = models.CharField(max_length=50, null=True, blank=True)

    has_transaction = models.BooleanField(default=False)

    permissions = (
        ('get_cheque', 'Can get cheques')
    )

    def __str__(self):
        if self.chequebook:
            return "{} - {} - {}".format(self.received_or_paid, self.chequebook.explanation[0:50], self.serial)
        else:
            return "{} - {} - {}".format(self.received_or_paid, self.explanation[0:50], self.serial)

    class Meta(BaseModel.Meta):
        verbose_name = 'چک'
        ordering = ['serial', ]

    def save(self, *args, **kwargs):
        res = super(Cheque, self).save(*args, **kwargs)
        if not self.id:
            if self.has_transaction:
                from sanads.transactions.models import TransactionItem
                try:
                    transaction_item = TransactionItem.objects.get(cheque=self)
                except TransactionItem.DoesNotExist:
                    return
                transaction_item.documentNumber = self.serial
                transaction_item.date = self.date
                transaction_item.due = self.due
                transaction_item.explanation = self.explanation
                transaction_item.value = self.value
                transaction_item.save()
        return res

