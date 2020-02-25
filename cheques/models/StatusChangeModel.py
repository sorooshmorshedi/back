from django.db import models
from django_jalali.db import models as jmodels
from accounts.accounts.models import Account, FloatAccount
from cheques.models.ChequeModel import Cheque, CHEQUE_STATUSES
from companies.models import FinancialYear
from helpers.models import BaseModel
from sanads.sanads.models import Sanad, newSanadCode


class StatusChange(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='status_changes')

    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='statusChanges')
    sanad = models.OneToOneField(Sanad, on_delete=models.CASCADE, related_name='statusChange', blank=True, null=True)

    bedAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='chequeStatusChangesAsBedAccount')
    bedFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT,
                                        related_name='chequeStatusChangesAsBesAccount', blank=True, null=True)
    besAccount = models.ForeignKey(Account, on_delete=models.PROTECT,
                                   related_name='chequeStatusChangesAsBedFloatAccount')
    besFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT,
                                        related_name='chequeStatusChangesAsBesFloatAccount', blank=True, null=True)

    date = jmodels.jDateField()
    explanation = models.CharField(max_length=255, blank=True)
    transferNumber = models.IntegerField(null=True)

    fromStatus = models.CharField(max_length=30, choices=CHEQUE_STATUSES)
    toStatus = models.CharField(max_length=30, choices=CHEQUE_STATUSES)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    permissions = (
        ('get_cheque', 'Can get cheques')
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'تغییر وضعیت'
        ordering = ['id', ]

    def createSanad(self, user):
        if not self.sanad:
            cheque = self.cheque
            fromStatus = self.fromStatus
            if not cheque.has_transaction or not fromStatus == 'blank':
                sanad = Sanad(code=newSanadCode(user), date=self.date,
                              createType=Sanad.AUTO, financial_year=user.active_financial_year)
                sanad.save()
                self.sanad = sanad
                self.save()
