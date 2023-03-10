from django.db import models
from rest_framework.exceptions import ValidationError

from accounts.accounts.models import Account, FloatAccount
from companies.models import FinancialYear
from helpers.models import BaseModel


class DefaultAccount(BaseModel):
    RECEIVE = 'receive'
    PAYMENT = 'payment'
    GUARANTEE = 'guarantee'
    FACTOR = 'factor'
    CLOSE_ACCOUNTS = 'closeAccounts'
    IMPREST = 'imprest'
    OTHER = 'other'

    DASHTBASHI = 'dashtbashi'

    COST_ACCOUNTING = 'costAccounting'

    USAGES = (
        (RECEIVE, 'دریافت'),
        (PAYMENT, 'پرداخت'),
        (GUARANTEE, 'اسناد ضمانتی'),
        (FACTOR, 'فاکتور'),
        (CLOSE_ACCOUNTS, 'بستن حساب ها'),
        (IMPREST, 'تنخواه'),
        (OTHER, 'دیگر'),

        (DASHTBASHI, 'دشتبشی'),

        (COST_ACCOUNTING, 'بهای تمام شده')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='financialYear')
    name = models.CharField(max_length=150)
    explanation = models.TextField(null=True, blank=True)

    account_level = models.CharField(max_length=1, choices=Account.ACCOUNT_LEVELS, default=Account.TAFSILI)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='defaultAccounts', blank=True,
                                null=True)
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='defaultAccounts', null=True,
                                     blank=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='defaultAccountsAsCostCenter',
                                   blank=True, null=True)
    usage = models.CharField(choices=USAGES, max_length=20)

    codename = models.CharField(max_length=255, null=True, blank=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        unique_together = ('financial_year', 'codename')
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
    def get(codename, financial_year=None):
        qs = DefaultAccount.objects.inFinancialYear(financial_year)
        try:
            default_account = qs.get(codename=codename)
            if not default_account.account:
                raise ValidationError("حساب پیشفرض {} را مشخص نشده است".format(default_account.name))

            return default_account
        except DefaultAccount.MultipleObjectsReturned as e:
            print(qs.filter(codename=codename))
            raise e
        except DefaultAccount.DoesNotExist as e:
            print(codename)
            raise e
