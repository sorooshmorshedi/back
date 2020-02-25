from django.db import models
from accounts.accounts.models import Account, FloatAccount
from companies.models import FinancialYear
from helpers.models import BaseModel


class Chequebook(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='chequebooks')

    code = models.IntegerField(unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='chequebook')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='chequebook', blank=True,
                                     null=True)
    explanation = models.CharField(max_length=255, blank=True)
    serial_from = models.IntegerField()
    serial_to = models.IntegerField()

    permissions = (
        ('get_cheque', 'Can get cheques')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        verbose_name = 'دفتر چک'
        ordering = ['code', ]
