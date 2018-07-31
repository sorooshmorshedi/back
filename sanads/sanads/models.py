from datetime import datetime
from django.db import models

from accounts.accounts.models import Account, FloatAccount
from accounts.costCenters.models import CostCenter
from sanads.RPTypes.models import RPType
from django_jalali.db import models as jmodels

SANAD_TYPES = (
    ('temporary', 'temporary'),
    ('definite', 'definite'),
)


class Sanad(models.Model):
    code = models.IntegerField(unique=True)
    explanation = models.CharField(max_length=255, blank=True)
    date = jmodels.jDateField()
    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=SANAD_TYPES)

    permissions = (
        ('get_sanad', 'Can get sanads')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta:
        ordering = ['code', ]


class SanadItem(models.Model):
    sanad = models.ForeignKey(Sanad, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='sanadItems')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='floatAccount', blank=True, null=True)
    costCenter = models.ForeignKey(CostCenter, on_delete=models.PROTECT, blank=True, null=True)

    type = models.ForeignKey(RPType, on_delete=models.PROTECT, blank=True, null=True)
    value = models.DecimalField(max_digits=24, decimal_places=0)
    valueType = models.CharField(max_length=3, choices=(('bed', 'bed'), ('bes', 'bes')))
    explanation = models.CharField(max_length=255, blank=True)

    permissions = (
        ('get_sanad', 'Can get sanads')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

