from cheques.models.ChequeModel import PASSED, TRANSFERRED, BOUNCED, CASHED, IN_FLOW, REVOKED, NOT_PASSED
from cheques.models.StatusChangeModel import StatusChange
from helpers.auto_sanad import AutoSanad
from helpers.functions import get_object_accounts, sanad_exp, date_to_str


class StatusChangeSanad(AutoSanad):

    def get_sanad_rows(self, instance: StatusChange) -> list:
        value = instance.cheque.value

        rows = [
            {
                'bed': value,
                'explanation': self.get_explanations()[1],
                'account': instance.bedAccount,
                'floatAccount': instance.bedFloatAccount,
                'costCenter': instance.bedCostCenter,
            },
            {
                'bes': value,
                'explanation': self.get_explanations()[2],
                'account': instance.besAccount,
                'floatAccount': instance.besFloatAccount,
                'costCenter': instance.besCostCenter,
            },
        ]

        return rows

    def get_sanad_date(self):
        return self.instance.date

    def get_sanad_explanations(self):
        return self.get_explanations()[0]

    def get_explanations(self):
        instance = self.instance
        cheque = instance.cheque

        base_explanation = sanad_exp(
            "چک به شماره سریال",
            cheque.serial,
            "به تاریخ سررسید",
            date_to_str(cheque.due),
            "جهت",
            cheque.explanation
        )

        if instance.toStatus == NOT_PASSED and instance.fromStatus != IN_FLOW:

            if cheque.is_paid:
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
            new_status = instance.toStatus
            if new_status == PASSED:
                if cheque.is_paid:
                    explanation = bed_explanation = bes_explanation = sanad_exp(
                        "بابت پاس شدن",
                        base_explanation,
                    )
                else:
                    explanation = bed_explanation = bes_explanation = sanad_exp(
                        "بابت وصول",
                        base_explanation,
                    )
            elif new_status == TRANSFERRED:
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

            elif new_status == BOUNCED:
                explanation = bed_explanation = sanad_exp(
                    "بابت برگشت",
                    base_explanation,
                )
                bes_explanation = sanad_exp("بابت برگشت", base_explanation)

            elif new_status == CASHED:
                if cheque.is_paid:
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

            elif new_status == IN_FLOW:
                explanation = bed_explanation = bes_explanation = sanad_exp(
                    "بابت درجریان قراردادن",
                    base_explanation,
                )

            elif new_status == REVOKED:
                explanation = bed_explanation = sanad_exp(
                    "بابت ابطال",
                    base_explanation,
                )
                bes_explanation = sanad_exp("بابت برگشت", base_explanation)
            else:
                raise Exception(f"وضعیت {new_status} تعریف نشده است ")

        return explanation, bed_explanation, bes_explanation

