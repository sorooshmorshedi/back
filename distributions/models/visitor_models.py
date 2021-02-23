from django.db import models
from django.db.models import Max

from accounts.accounts.models import Account
from companies.models import FinancialYear
from distributions.models.commission_range_models import CommissionRange
from helpers.functions import get_new_child_code
from helpers.models import BaseModel, DECIMAL, EXPLANATION
from helpers.views.MassRelatedCUD import MassRelatedCUD
from users.models import User


class Visitor(BaseModel):
    LEVELS = 4
    CODE_LENGTHS = [2, 2, 2, 2]

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='visitors')
    level = models.IntegerField()
    code = models.CharField(max_length=12, verbose_name='کد حساب')
    explanation = EXPLANATION()

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        blank=True,
        null=True
    )

    commission_percent = models.IntegerField(default=0)
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

    def get_new_child_code(self):
        last_child_code = None

        last_child = self.children.order_by('-code').first()
        if last_child:
            last_child_code = last_child.code

        return get_new_child_code(
            self.code,
            self.CODE_LENGTHS[self.level + 1],
            last_child_code
        )

    @staticmethod
    def get_new_code():
        code = Visitor.objects.inFinancialYear().filter(level=0).aggregate(
            last_code=Max('code')
        )['last_code']

        if code:
            code = int(code) + 1
        else:
            code = 0

        if code < 9:
            code += 10

        if code >= 99:
            from rest_framework import serializers
            raise serializers.ValidationError("تعداد عضو های این سطح پر شده است")

        return str(code)
