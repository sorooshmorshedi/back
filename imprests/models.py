import uuid
from django.db import models
from django_jalali.db import models as jmodels
from rest_framework.exceptions import ValidationError

from accounts.accounts.models import Account, FloatAccount
from companies.models import FinancialYear
from helpers.models import BaseModel, DECIMAL, EXPLANATION, ConfirmationMixin
from transactions.models import Transaction


class ImprestSettlement(BaseModel, ConfirmationMixin):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    code = models.IntegerField()
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name='imprestSettlements')
    explanation = EXPLANATION()
    date = jmodels.jDateField()

    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    settled_value = DECIMAL()
    is_settled = models.BooleanField(default=False)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        ordering = ['-code', ]
        permission_basename = 'imprestSettlement'
        permissions = (
            ('get.imprestSettlement', 'مشاهده تسویه تنخواه'),
            ('create.imprestSettlement', 'تعریف تسویه تنخواه'),
            ('update.imprestSettlement', 'ویرایش تسویه تنخواه'),
            ('delete.imprestSettlement', 'حذف تسویه تنخواه'),

            ('getOwn.imprestSettlement', 'مشاهده تسویه تنخواه های خود'),
            ('updateOwn.imprestSettlement', 'ویرایش تسویه تنخواه های خود'),
            ('deleteOwn.imprestSettlement', 'حذف تسویه تنخواه های خود'),

            ('firstConfirm.imprestSettlement', 'تایید اول تنخواه '),
            ('secondConfirm.imprestSettlement', 'تایید دوم تنخواه '),
            ('firstConfirmOwn.imprestSettlement', 'تایید اول تنخواه های خود'),
            ('secondConfirmOwn.imprestSettlement', 'تایید دوم تنخواه های خود'),
        )

    def update_settlement_data(self):
        settled_value = 0
        for item in self.items.all():
            settled_value += item.value

        if settled_value > self.transaction.sum:
            raise ValidationError({'non_field_errors': ["مجموع نباید از مبلغ پرداختی بیشتر باشد"]})

        self.is_settled = settled_value == self.transaction.sum
        self.settled_value = settled_value
        self.save()


def upload_to(instance, filename):
    directory = instance.__class__.__name__
    return "{}/{}-{}".format(directory, uuid.uuid1(), filename)


class ImprestSettlementItem(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    imprestSettlement = models.ForeignKey(ImprestSettlement, on_delete=models.CASCADE, related_name='items')

    date = jmodels.jDateField()
    explanation = EXPLANATION()

    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='imprestSettlementItems')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='imprestSettlementItems',
                                     blank=True, null=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT,
                                   related_name="imprestSettlementItemsAsCostCenter", blank=True, null=True)
    value = DECIMAL()

    attachment = models.FileField(upload_to=upload_to, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.pk, self.explanation)

    class Meta(BaseModel.Meta):
        pass
