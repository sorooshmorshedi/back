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

        sanad.date = cheque.date

        base_explanation = sanad_exp(
            "چک به شماره سریال",
            cheque.serial,
            "به تاریخ سررسید",
            due,
            "جهت",
            cheque.explanation
        )

        if self.toStatus == 'notPassed' and self.fromStatus != 'inFlow':

            if cheque.received_or_paid == Cheque.PAID:
                explanation = sanad_exp(
                    "بابت پرداخت",
                    base_explanation,
                )
            else:
                explanation = sanad_exp(
                    "بابت دریافت",
                    base_explanation,
                )

            bed_explanation = sanad_exp(
                "بابت دریافت",
                base_explanation
            )
            bes_explanation = sanad_exp(
                "بابت پرداخت",
                base_explanation
            )

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
            if newStatus == 'passed':
                if cheque.received_or_paid == Cheque.PAID:
                    explanation = bed_explanation = bes_explanation = sanad_exp(
                        "بابت پاس شدن",
                        base_explanation,
                    )
                else:
                    explanation = bed_explanation = bes_explanation = sanad_exp(
                        "بابت وصول",
                        base_explanation,
                    )
            elif newStatus == 'transferred':
                explanation = sanad_exp(
                    "بابت انتقال",
                    base_explanation,
                )
                bed_explanation = sanad_exp(
                    "بابت پرداخت طی انتقال",
                    base_explanation,
                )
                bes_explanation = sanad_exp(
                    "بابت انتقال چک",
                    base_explanation,
                )

            elif newStatus == 'bounced':
                explanation = bed_explanation = sanad_exp(
                    "بابت برگشت",
                    base_explanation,
                )
                bes_explanation = sanad_exp("بابت برگشت", base_explanation)

            elif newStatus == 'cashed':
                if cheque.received_or_paid == Cheque.PAID:
                    explanation = bed_explanation = bes_explanation = sanad_exp(
                        "بابت پرداخت نقدی",
                        base_explanation,
                    )
                else:
                    explanation = bed_explanation = sanad_exp(
                        "بابت وصول نقدی",
                        base_explanation,
                    )
                    bes_explanation = sanad_exp(
                        "بابت پرداخت نقدی",
                        base_explanation,
                    )

            elif newStatus == 'inFlow':
                explanation = bed_explanation = bes_explanation = sanad_exp(
                    "بابت درجریان قراردادن",
                    base_explanation,
                )

            elif newStatus == 'revoked':
                explanation = bed_explanation = sanad_exp(
                    "بابت ابطال",
                    base_explanation,
                )
                bes_explanation = sanad_exp("بابت برگشت", base_explanation)
            else:
                raise ValidationError("وضعیت جدید چک معتبر نمی باشد")

        sanad.items.create(
            bed=value,
            explanation=bed_explanation,
            account=self.bedAccount,
            floatAccount=self.bedFloatAccount,
            costCenter=self.bedCostCenter,
            financial_year=sanad.financial_year
        )
        sanad.items.create(
            bes=value,
            explanation=bes_explanation,
            account=self.besAccount,
            costCenter=self.besCostCenter,
            financial_year=sanad.financial_year
        )
        sanad.date = self.date
        sanad.explanation = explanation
        sanad.save()

        sanad.define()
        sanad.update_values()

        return sanad
