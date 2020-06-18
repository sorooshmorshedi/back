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
    OTHER = 'other'
    USAGES = (
        (RECEIVE, 'دریافت'),
        (PAYMENT, 'پرداخت'),
        (RECEIVE_AND_PAYMENT, 'دریافت و پرداخت'),
        (FACTOR, 'فاکتور'),
        (CLOSE_ACCOUNTS, 'بستن حساب ها'),
        (OTHER, 'دیگر')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='financialYear')
    name = models.CharField(max_length=150)
    explanation = models.TextField(null=True, blank=True)

    account_level = models.IntegerField(choices=Account.ACCOUNT_LEVELS, default=Account.TAFSILI)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='defaultAccounts')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='defaultAccounts', null=True,
                                     blank=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='defaultAccountsAsCostCenter',
                                   blank=True, null=True)
    usage = models.CharField(choices=USAGES, max_length=20)

    nickname = models.CharField(unique=True, max_length=50, null=True, blank=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permissions = (
            ('get.defaultAccount', 'مشاهده حساب های پیشفرض'),
            ('create.defaultAccount', 'تعریف حساب پیشفرض'),
            ('update.defaultAccount', 'ویرایش حساب پیشفرض'),
            ('delete.defaultAccount', 'حذف حساب پیشفرض'),
        )

    def __str__(self):
        return "{} {}".format(self.name, self.nickname)

    @staticmethod
    def get(nickname):
        return DefaultAccount.objects.get(nickname=nickname)


def getDefaultAccount(pn):
    return DefaultAccount.objects.get(nickname=pn)
