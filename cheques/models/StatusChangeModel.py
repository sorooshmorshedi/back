from django.db import models
from django_jalali.db import models as jmodels
from rest_framework.exceptions import ValidationError

from accounts.accounts.models import Account, FloatAccount
from cheques.models.ChequeModel import Cheque, CHEQUE_STATUSES
from companies.models import FinancialYear
from helpers.functions import sanad_exp
from helpers.models import BaseModel
from sanads.models import Sanad, newSanadCode, clearSanad


class StatusChange(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='statusChanges')

    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='statusChanges')
    sanad = models.OneToOneField(Sanad, on_delete=models.CASCADE, related_name='statusChange', blank=True, null=True)

    bedAccount = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='chequeStatusChangesAsBedAccount')
    bedFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT,
                                        related_name='chequeStatusChangesAsBesAccount', blank=True, null=True)
    bedCostCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT,
                                      related_name='chequeStatusChangesAsBesAccountAsCostCenter', blank=True, null=True)
    besAccount = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='chequeStatusChangesAsBedFloatAccount')
    besFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT,
                                        related_name='chequeStatusChangesAsBesFloatAccount', blank=True, null=True)
    besCostCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT,
                                      related_name='chequeStatusChangesAsBesFloatAccountAsCostCenter', blank=True,
                                      null=True)

    date = jmodels.jDateField()
    explanation = models.CharField(max_length=255, blank=True, null=True)

    # not used
    transferNumber = models.IntegerField(null=True)

    fromStatus = models.CharField(max_length=30, choices=CHEQUE_STATUSES)
    toStatus = models.CharField(max_length=30, choices=CHEQUE_STATUSES)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'تغییر وضعیت'
        ordering = ['id', ]
        permissions = (
            ('delete.receivedChequeStatusChange', 'حذف تغییر وضعیت های چک دریافتی'),

            ('delete.paidChequeStatusChange', 'حذف تغییر وضعیت های چک پرداختی'),

            ('deleteOwn.receivedChequeStatusChange', 'حذف تغییر وضعیت های چک دریافتی خود'),

            ('deleteOwn.paidChequeStatusChange', 'حذف تغییر وضعیت های چک پرداختی خود'),
        )

    def _createSanad(self, user):
        if not self.sanad:
            cheque = self.cheque
            fromStatus = self.fromStatus
            if not cheque.has_transaction or not fromStatus == 'blank':
                sanad = Sanad(
                    code=newSanadCode(),
                    date=self.date,
                    financial_year=user.active_financial_year,
                    is_auto_created=True,
                )
                sanad.save()
                self.sanad = sanad
                self.save()

                return sanad
