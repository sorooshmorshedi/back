from django.db import models

from accounts.accounts.models import Account, FloatAccount
from companies.models import FinancialYear
from helpers.models import BaseModel

EXPENSE_TYPES = (
    ('buy', 'خرید'),
    ('sale', 'فروش')
)


class Expense(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='expenses')
    name = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factorExpense')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorExpense', null=True,
                                     blank=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorExpenseAsCostCenter',
                                   blank=True, null=True)
    type = models.CharField(max_length=10, choices=EXPENSE_TYPES)
    explanation = models.CharField(max_length=255, blank=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'expense'
        permissions = (
            ('get.expense', 'مشاهده هزینه فاکتور'),
            ('create.expense', 'تعریف هزینه  فاکتور'),
            ('update.expense', 'ویرایش هزینه فاکتور'),
            ('delete.expense', 'حذف هزینه فاکتور'),

            ('getOwn.expense', 'مشاهده هزینه های فاکتور خود'),
            ('updateOwn.expense', 'ویرایش هزینه های فاکتور خود'),
            ('deleteOwn.expense', 'حذف هزینه های فاکتور خود'),
        )