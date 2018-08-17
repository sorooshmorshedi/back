from django.db import models
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account, FloatAccount
from wares.models import Ware, WareHouse


class FactorExpense(models.Model):
    name = models.CharField(max_length=100, unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factorExpense')
    explanation = models.CharField(max_length=255, blank=True)


class Factor(models.Model):
    code = models.IntegerField(unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factors')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factors', blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)

    date = jmodels.jDateField()
    time = models.TimeField(blank=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    discountValue = models.IntegerField(default=0, null=True, blank=True)
    discountPercent = models.IntegerField(default=0, null=True, blank=True)
    taxValue = models.IntegerField(default=0, null=True, blank=True)
    taxPercent = models.IntegerField(default=0, null=True, blank=True)


class FactorItem(models.Model):
    ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='factorItems')
    wareHouse = models.ForeignKey(WareHouse, on_delete=models.PROTECT, related_name='factorItems')

    count = models.IntegerField()
    fee = models.IntegerField()

    discountValue = models.IntegerField(default=0, null=True, blank=True)
    discountPercent = models.IntegerField(default=0, null=True, blank=True)


