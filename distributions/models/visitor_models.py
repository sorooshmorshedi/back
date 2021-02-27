from django.db import models
from accounts.accounts.models import FloatAccount
from companies.models import FinancialYear
from distributions.models.commission_range_models import CommissionRange
from helpers.models import BaseModel, DECIMAL, EXPLANATION, TreeMixin
from users.models import User


class Visitor(BaseModel, TreeMixin):
    CODE_LENGTHS = [2, 2, 2, 2]

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='visitors')
    explanation = EXPLANATION()

    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT)
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        blank=True,
        null=True
    )

    commission_percent = models.FloatField(default=0)
    fixed_commission = DECIMAL(default=0)
    commissionRange = models.ForeignKey(
        CommissionRange,
        on_delete=models.PROTECT,
        related_name='visitors',
        blank=True,
        null=True
    )

    class Meta(BaseModel.Meta):
        ordering = ['code']
        backward_financial_year = True
        unique_together = (('financial_year', 'user', 'level'),)

        permissions = (
            ('create.visitor', 'تعریف ویزیتور'),

            ('get.visitor', 'مشاهده ویزیتور'),
            ('update.visitor', 'ویرایش ویزیتور'),
            ('delete.visitor', 'حذف ویزیتور'),

            ('getOwn.visitor', 'مشاهده ویزیتور های خود'),
            ('updateOwn.visitor', 'ویرایش ویزیتور های خود'),
            ('deleteOwn.visitor', 'حذف ویزیتور های خود'),
        )
