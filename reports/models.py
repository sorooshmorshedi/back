from django.db import models

from companies.models import FinancialYear
from helpers.models import BaseModel


class ExportVerifier(BaseModel):
    SANAD = 'S'
    FACTOR_BUY = 'FB'
    FACTOR_SALE = 'FS'
    FACTOR_BACK_FROM_BUY = 'FBFB'
    FACTOR_BACK_FROM_SALE = 'FBFS'
    RECEIPT = 'RT'
    REMITTANCE = 'RC'
    TRANSACTION_RECEIVE = 'TR'
    TRANSACTION_PAYMENT = 'TP'

    FORMS = (
        (SANAD, 'سند'),
        (FACTOR_BUY, 'فاکتور خرید'),
        (FACTOR_SALE, 'فاکتور فروش'),
        (FACTOR_BACK_FROM_BUY, 'فاکتور برگشت از خرید'),
        (FACTOR_BACK_FROM_SALE, 'فاکتور برگشت از فروش'),
        (RECEIPT, 'رسید'),
        (REMITTANCE, 'حواله'),
        (TRANSACTION_RECEIVE, 'دریافت'),
        (TRANSACTION_PAYMENT, 'پرداخت'),
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='export_verifiers')
    name = models.CharField(max_length=200, blank=True, null=True)
    post = models.CharField(max_length=255)
    form = models.CharField(choices=FORMS, max_length=4)

    class Meta(BaseModel.Meta):
        default_permissions = ()

    def __str__(self):
        form_name = ''
        for form in self.FORMS:
            if self.form == form[0]:
                form_name = form[1]
                break
        return "{} {} ({})".format(self.name, self.post, form_name)
