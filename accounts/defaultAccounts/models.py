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
    IMPREST = 'imprest'
    OTHER = 'other'
    USAGES = (
        (RECEIVE, 'دریافت'),
        (PAYMENT, 'پرداخت'),
        (RECEIVE_AND_PAYMENT, 'دریافت و پرداخت'),
        (FACTOR, 'فاکتور'),
        (CLOSE_ACCOUNTS, 'بستن حساب ها'),
        (IMPREST, 'تنخواه'),
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

    codename = models.CharField(unique=True, max_length=255, null=True, blank=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'defaultAccount'
        permissions = (
            ('get.defaultAccount', 'مشاهده حساب های پیشفرض'),
            ('create.defaultAccount', 'تعریف حساب پیشفرض'),
            ('update.defaultAccount', 'ویرایش حساب پیشفرض'),
            ('delete.defaultAccount', 'حذف حساب پیشفرض'),

            ('getOwn.defaultAccount', 'مشاهده حساب های پیشفرض خود'),
            ('updateOwn.defaultAccount', 'ویرایش حساب پیشفرض خود'),
            ('deleteOwn.defaultAccount', 'حذف حساب پیشفرض خود'),
        )

    def __str__(self):
        return "{} {}".format(self.name, self.codename)

    @staticmethod
    def get(codename):
        return DefaultAccount.objects.get(codename=codename)
