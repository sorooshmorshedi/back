from django.db import models
from django_jalali.db import models as jmodels
from accounts.accounts.models import Account, FloatAccount
from accounts.defaultAccounts.models import getDefaultAccount
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
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='receivedChequesAsCostCenter',
                                   blank=True, null=True)

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
    lastCostCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='lastChequesAsCostCenter', blank=True,
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
        if self.has_transaction:
            from sanads.transactions.models import TransactionItem
            transaction_item = TransactionItem.objects.filter(cheque=self).first()
            if transaction_item:
                transaction_item.documentNumber = self.serial
                transaction_item.date = self.date
                transaction_item.due = self.due
                transaction_item.explanation = self.explanation
                transaction_item.value = self.value
                transaction_item.save()

        if not self.lastAccount:
            self.lastAccount = self.account
            self.lastFloatAccount = self.floatAccount
            self.lastCostCenter = self.costCenter
            res = self.save()

        return res

    def changeStatus(self, user, date, to_status, account: Account = None, floatAccount: floatAccount = None,
                     costCenter: floatAccount = None, explanation='', sanad=None):
        data = {
            'cheque': self.id,
            'fromStatus': self.status,
            'toStatus': to_status,
            'financial_year': user.active_financial_year.id,
            'date': date,
            'explanation': explanation
        }

        if sanad:
            data['sanad'] = sanad.id

        lastFloatAccount = None
        lastCostCenter = None

        if self.received_or_paid == Cheque.RECEIVED:

            data['besAccount'] = self.lastAccount.id
            if self.lastFloatAccount:
                data['besFloatAccount'] = self.lastFloatAccount.id
            if self.lastCostCenter:
                data['besCostCenter'] = self.lastCostCenter.id

            if to_status == 'revoked' or to_status == 'bounced':
                lastAccount = self.account
                data['bedAccount'] = self.account.id
                if self.floatAccount:
                    lastFloatAccount = self.floatAccount
                    data['bedFloatAccount'] = self.floatAccount.id
                if self.costCenter:
                    lastCostCenter = self.costCenter
                    data['bedCostCenter'] = self.costCenter.id

            elif to_status == 'notPassed':
                defaultAccount = getDefaultAccount('receivedCheque', user)
                lastAccount = defaultAccount.account
                lastFloatAccount = defaultAccount.floatAccount
                lastCostCenter = defaultAccount.costCenter
                data['bedAccount'] = lastAccount.id

            else:
                lastAccount = account
                data['bedAccount'] = account.id
                if floatAccount:
                    lastFloatAccount = floatAccount
                    data['bedFloatAccount'] = floatAccount.id
                if costCenter:
                    lastCostCenter = costCenter
                    data['bedCostCenter'] = costCenter.id

        else:

            data['bedAccount'] = self.lastAccount.id
            if self.lastFloatAccount:
                data['bedFloatAccount'] = self.lastFloatAccount.id
            if self.lastCostCenter:
                data['bedCostCenter'] = self.costCenter.id

            if to_status == 'revoked' or to_status == 'bounced':
                lastAccount = self.account
                data['besAccount'] = self.account.id
                if self.floatAccount:
                    lastFloatAccount = self.floatAccount
                    data['besFloatAccount'] = self.floatAccount.id
                if self.costCenter:
                    lastCostCenter  = self.costCenter
                    data['besCostCenter'] = self.costCenter.id

            elif to_status == 'passed':
                lastAccount = self.chequebook.account
                data['besAccount'] = self.chequebook.account.id
                if self.chequebook.floatAccount:
                    lastFloatAccount = self.chequebook.floatAccount
                    data['besFloatAccount'] = self.chequebook.floatAccount.id
                if self.chequebook.costCenter:
                    lastCostCenter = self.chequebook.costCenter
                    data['besCostCenter'] = self.chequebook.costCenter.id

            elif to_status == 'notPassed':
                defaultAccount = getDefaultAccount('paidCheque', user)
                lastAccount = defaultAccount.account
                lastFloatAccount = defaultAccount.floatAccount
                lastCostCenter = defaultAccount.costCenter
                data['besAccount'] = lastAccount.id

            else:
                lastAccount = account
                data['besAccount'] = account.id
                if floatAccount:
                    lastFloatAccount = floatAccount
                    data['besFloatAccount'] = floatAccount.id
                if costCenter:
                    lastCostCenter = costCenter
                    data['besCostCenter'] = costCenter.id

        from cheques.serializers import StatusChangeSerializer
        serialized = StatusChangeSerializer(data=data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        self.lastAccount = lastAccount
        self.lastFloatAccount = lastFloatAccount
        self.lastCostCenter = lastCostCenter
        self.status = to_status
        self.save()

        return serialized.instance
