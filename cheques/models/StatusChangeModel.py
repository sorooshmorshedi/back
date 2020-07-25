from django.db import models
from django_jalali.db import models as jmodels
from accounts.accounts.models import Account, FloatAccount
from cheques.models.ChequeModel import Cheque, CHEQUE_STATUSES
from companies.models import FinancialYear
from helpers.models import BaseModel
from sanads.models import Sanad, newSanadCode, clearSanad


class StatusChange(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='statusChanges')

    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='statusChanges')
    sanad = models.OneToOneField(Sanad, on_delete=models.CASCADE, related_name='statusChange', blank=True, null=True)

    bedAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='chequeStatusChangesAsBedAccount')
    bedFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT,
                                        related_name='chequeStatusChangesAsBesAccount', blank=True, null=True)
    bedCostCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT,
                                      related_name='chequeStatusChangesAsBesAccountAsCostCenter', blank=True, null=True)
    besAccount = models.ForeignKey(Account, on_delete=models.PROTECT,
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
                    createType=Sanad.AUTO,
                    financial_year=user.active_financial_year
                )
                sanad.save()
                self.sanad = sanad
                self.save()

                return sanad

    def updateSanad(self, user):
        value = self.cheque.value
        cheque = self.cheque

        if cheque.has_transaction and self.fromStatus == 'blank':
            return None

        sanad = self.sanad
        if not sanad:
            sanad = self._createSanad(user)

        clearSanad(sanad)

        due = "/".join(str(cheque.due).split("-"))

        sanad.explanation = cheque.explanation
        sanad.date = cheque.date

        if cheque.received_or_paid == Cheque.PAID:
            received_or_paid = 'پرداخت'
        else:
            received_or_paid = 'دریافت'

        if self.toStatus == 'notPassed' and self.fromStatus != 'inFlow':
            explanation = "بابت {0} چک شماره {1} به تاریخ سررسید {2} از {3}".format(received_or_paid, cheque.serial,
                                                                                    due, cheque.account.name)
        else:
            newStatus = self.toStatus
            if self.fromStatus == 'inFlow' and newStatus in ('notPassed', 'bounced'):
                newStatus = 'revokeInFlow'
            statuses = {
                'revokeInFlow': 'ابطال در جریان قرار دادن',
                'inFlow': 'در جریان قرار دادن',
                'passed': 'وصول',
                'bounced': 'برگشت',
                'cashed': 'نقد',
                'revoked': 'ابطال',
                'transferred': 'انتقال چک',
            }
            explanation = "بابت {0} چک شماره {1} به تاریخ سررسید {2} ".format(statuses[newStatus], cheque.serial, due)

        sanad.items.create(
            bed=value,
            explanation=explanation,
            account=self.bedAccount,
            floatAccount=self.bedFloatAccount,
            costCenter=self.bedCostCenter,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            bes=value,
            explanation=explanation,
            account=self.besAccount,
            costCenter=self.besCostCenter,
            financial_year=sanad.financial_year
        )
        sanad.type = 'temporary'
        sanad.save()

        return sanad
