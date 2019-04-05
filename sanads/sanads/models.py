from decimal import Decimal
from django.db.models import signals
from django.db import models
from accounts.accounts.models import Account, FloatAccount
from accounts.costCenters.models import CostCenter
from django_jalali.db import models as jmodels

from companies.models import FinancialYear
from helpers.models import BaseModel


class Sanad(BaseModel):
    TEMPORARY = 'temporary'
    DEFINITE = 'definite'
    SANAD_TYPES = (
        (TEMPORARY, 'موقت'),
        (DEFINITE, 'قطعی'),
    )

    AUTO = 'auto'
    MANUAL = 'manual'
    SANAD_CREATE_TYPES = (
        (AUTO, 'خودکار'),
        (MANUAL, 'دستی')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='sanads')
    code = models.IntegerField(unique=True, verbose_name="شماره سند")
    explanation = models.CharField(max_length=255, blank=True, verbose_name="توضیحات")
    date = jmodels.jDateField(verbose_name="تاریخ")
    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=SANAD_TYPES)
    createType = models.CharField(max_length=20, choices=SANAD_CREATE_TYPES, default=MANUAL, verbose_name="نوع ثبت")

    bed = models.DecimalField(max_digits=24, decimal_places=0, default=0, verbose_name="بدهکار")
    bes = models.DecimalField(max_digits=24, decimal_places=0, default=0, verbose_name="بستانکار")

    permissions = (
        ('get_sanad', 'Can get sanads')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        ordering = ['-code', ]


class SanadItem(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='sanad_items')
    sanad = models.ForeignKey(Sanad, on_delete=models.CASCADE, related_name='items', verbose_name='سند')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='sanadItems', verbose_name='حساب')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='sanadItems', blank=True, null=True, verbose_name='حساب شناور')
    costCenter = models.ForeignKey(CostCenter, on_delete=models.PROTECT, blank=True, null=True, verbose_name='مرکز هزینه')

    value = models.DecimalField(max_digits=24, decimal_places=0)
    valueType = models.CharField(max_length=3, choices=(('bed', 'bed'), ('bes', 'bes')))
    explanation = models.CharField(max_length=255, blank=True, verbose_name='توضیحات')

    permissions = (
        ('get_sanad', 'Can get sanads')
    )

    def __str__(self):
        return "{0} - {1}".format(self.sanad.code, self.explanation[0:30])


def updateSanadValues(sender, instance, raw, using, update_fields, **kwargs):

    subValue = 0
    addValue = instance.value
    newType = instance.valueType
    oldType = newType
    if instance.id:
        try:
            obj = SanadItem.objects.get(pk=instance.id)
            subValue = obj.value
            oldType = obj.valueType
        except SanadItem.DoesNotExist:
            pass

    sanad = instance.sanad

    if oldType == 'bed':
        sanad.bed -= subValue
    else:
        sanad.bes -= subValue

    if newType == 'bed':
        sanad.bed += Decimal(addValue)
    else:
        sanad.bes += Decimal(addValue)

    sanad.save()


def updateSanadValuesOnDelete(sender, instance, using, **kwargs):
    sanad = instance.sanad
    if instance.valueType == 'bed':
        sanad.bed -= instance.value
    else:
        sanad.bes -= instance.value

    sanad.save()

signals.pre_save.connect(receiver=updateSanadValues, sender=SanadItem)
signals.pre_delete.connect(receiver=updateSanadValuesOnDelete, sender=SanadItem)


def clearSanad(sanad):
    sanad.explanation = ''
    sanad.type = 'manual'
    sanad.save()
    for item in sanad.items.all():
        item.delete()


def newSanadCode(user):
    try:
        return Sanad.objects.inFinancialYear(user).latest('code').code + 1
    except:
        return 1

