from django.db import models

from accounts.accounts.models import Account
from companies.models import FinancialYear
from helpers.models import BaseModel


class DefaultAccount(BaseModel):
    RECEIVE = 'receive'
    PAYMENT = 'payment'
    RECEIVE_AND_PAYMENT = 'receiveAndPayment'
    FACTOR = 'factor'
    NONE = 'none'
    USAGES = (
        (RECEIVE, 'دریافت'),
        (PAYMENT, 'پرداخت'),
        (RECEIVE_AND_PAYMENT, 'دریافت و پرداخت'),
        (FACTOR, 'فاکتور'),
        (NONE, 'هیچ کدام')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='default_accounts')
    name = models.CharField(unique=True, max_length=150)
    explanation = models.TextField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='defaultAccount')
    usage = models.CharField(choices=USAGES, max_length=20)

    programingName = models.CharField(unique=True, max_length=50, null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'حساب پیشفرض'

    def __str__(self):
        return self.name


def getDA(pn, user):
    return DefaultAccount.objects.inFinancialYear(user).get(programingName=pn)



