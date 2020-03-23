from django.db import models

from accounts.accounts.models import Account, FloatAccount
from companies.models import FinancialYear
from helpers.models import BaseModel


class DefaultAccount(BaseModel):
    RECEIVE = 'receive'
    PAYMENT = 'payment'
    RECEIVE_AND_PAYMENT = 'receiveAndPayment'
    FACTOR = 'factor'
    CLOSE_ACCOUNTS = 'closeAccounts'
    NONE = 'none'
    USAGES = (
        (RECEIVE, 'دریافت'),
        (PAYMENT, 'پرداخت'),
        (RECEIVE_AND_PAYMENT, 'دریافت و پرداخت'),
        (FACTOR, 'فاکتور'),
        (CLOSE_ACCOUNTS, 'بستن حساب ها'),
        (NONE, 'هیچ کدام')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='financialYear')
    name = models.CharField(unique=True, max_length=150)
    explanation = models.TextField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='defaultAccounts')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='defaultAccounts', null=True,
                                     blank=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='defaultAccountsAsCostCenter',
                                   blank=True, null=True)
    usage = models.CharField(choices=USAGES, max_length=20)

    programingName = models.CharField(unique=True, max_length=50, null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'حساب پیشفرض'

    def __str__(self):
        return "{} {}".format(self.name, self.programingName)


def getDefaultAccount(pn):
    return DefaultAccount.objects.get(programingName=pn)
