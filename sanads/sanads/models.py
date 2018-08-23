from decimal import Decimal
from django.db.models import signals
from django.db import models
from accounts.accounts.models import Account, FloatAccount
from accounts.costCenters.models import CostCenter
from django_jalali.db import models as jmodels

SANAD_TYPES = (
    ('temporary', 'temporary'),
    ('definite', 'definite'),
)

SANAD_CREATE_TYPES = (
    ('auto', 'auto'),
    ('manual', 'manual')
)


class Sanad(models.Model):
    code = models.IntegerField(unique=True)
    explanation = models.CharField(max_length=255, blank=True)
    date = jmodels.jDateField()
    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=SANAD_TYPES)
    createType = models.CharField(max_length=20, choices=SANAD_CREATE_TYPES, default='manual')

    bed = models.DecimalField(max_digits=24, decimal_places=0, default=0)
    bes = models.DecimalField(max_digits=24, decimal_places=0, default=0)

    permissions = (
        ('get_sanad', 'Can get sanads')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta:
        ordering = ['-code', ]


class SanadItem(models.Model):
    sanad = models.ForeignKey(Sanad, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='sanadItems')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='floatAccount', blank=True, null=True)
    costCenter = models.ForeignKey(CostCenter, on_delete=models.PROTECT, blank=True, null=True)

    value = models.DecimalField(max_digits=24, decimal_places=0)
    valueType = models.CharField(max_length=3, choices=(('bed', 'bed'), ('bes', 'bes')))
    explanation = models.CharField(max_length=255, blank=True)

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
        obj = SanadItem.objects.get(pk=instance.id)
        subValue = obj.value
        oldType = obj.valueType

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
    sanad.save()
    for item in sanad.items.all():
        item.delete()
