from django.db import models
from django_jalali.db import models as jmodels
from rest_framework.exceptions import ValidationError

from accounts.accounts.models import Account, FloatAccount
from companies.models import FinancialYear
from helpers.functions import get_new_code
from helpers.models import BaseModel, DECIMAL, EXPLANATION, upload_to
from sanads.models import Sanad
from transactions.models import Transaction


class ImprestSettlement(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    code = models.IntegerField()
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, related_name='imprestSettlement')
    sanad = models.OneToOneField(Sanad, on_delete=models.PROTECT, related_name='imprestSettlement', blank=True,
                                 null=True)
    explanation = EXPLANATION()
    date = jmodels.jDateField()

    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    settled_value = DECIMAL()
    is_settled = models.BooleanField(default=False)

    @property
    def remain_value(self):
        return self.transaction.sanad.bed - self.settled_value

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation)

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

    def sync(self):
        settled_value = 0
        for item in self.items.all():
            settled_value += item.value

        if settled_value > self.transaction.sum:
            raise ValidationError({'non_field_errors': ["مجموع نباید از مبلغ پرداختی بیشتر باشد"]})

        self.is_settled = settled_value == self.transaction.sum
        self.settled_value = settled_value
        self.save()

        from imprests.sanads import ImprestSettlementSanad
        ImprestSettlementSanad(self).update()

    @staticmethod
    def settle_imprest(imprest: Transaction, date, account, floatAccount=None, costCenter=None, explanation=""):

        imprest_settlement = getattr(imprest, 'imprestSettlement', None)
        if not imprest_settlement:
            imprest_settlement = ImprestSettlement.objects.create(
                financial_year=imprest.financial_year,
                code=get_new_code(ImprestSettlement),
                transaction=imprest,
                date=date,
                is_auto_created=True,
            )

        ImprestSettlementItem.objects.create(
            financial_year=imprest.financial_year,
            imprestSettlement=imprest_settlement,
            date=date,
            account=account,
            floatAccount=floatAccount,
            costCenter=costCenter,
            value=imprest_settlement.remain_value,
            explanation=explanation,
            is_auto_created=True,
        )

        imprest_settlement.sync()

        return imprest_settlement


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

    order = models.IntegerField(default=0)

    def __str__(self):
        return "{0} - {1}".format(self.pk, self.explanation)

    class Meta(BaseModel.Meta):
        pass
