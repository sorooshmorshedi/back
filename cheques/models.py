from django.db import models
from django.db.models import signals
from django_jalali.db import models as jmodels
from rest_framework import serializers

from accounts.accounts.models import Account, FloatAccount
from cheques.signals import *
from sanads.sanads.models import SanadItem, Sanad, clearSanad

CHECK_TYPES = (
    ('paid', 'پرداختی'),
    ('received', 'دریافتی')
)

CHECK_STATUSES = (
    ('blank', 'blank'),
    ('notPassed', 'notPassed'),
    ('inFlow', 'inFlow'),
    ('passed', 'passed'),
    ('bounced', 'bounced'),
    ('cashed', 'cashed'),
    ('revoked', 'revoked'),
    ('transferred', 'transferred'),
)


class Chequebook(models.Model):

    code = models.IntegerField(unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='chequebook')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='chequebook', blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    serial_from = models.IntegerField()
    serial_to = models.IntegerField()

    permissions = (
        ('get_cheque', 'Can get cheques')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta:
        ordering = ['code', ]


class Cheque(models.Model):

    serial = models.IntegerField()
    chequebook = models.ForeignKey(Chequebook, on_delete=models.CASCADE, related_name='cheques', blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='receivedCheques', blank=True, null=True)
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='receivedCheques', blank=True, null=True)

    value = models.DecimalField(max_digits=24, decimal_places=0, blank=True, null=True)
    due = jmodels.jDateField(blank=True, null=True)
    date = jmodels.jDateField(blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, choices=CHECK_STATUSES)
    type = models.CharField(max_length=10, choices=CHECK_TYPES)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    lastAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='lastCheques', blank=True, null=True)
    lastFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='lastCheques', blank=True, null=True)

    bankName = models.CharField(max_length=100, null=True, blank=True)
    branchName = models.CharField(max_length=100, null=True, blank=True)
    accountNumber = models.CharField(max_length=50, null=True, blank=True)

    permissions = (
        ('get_cheque', 'Can get cheques')
    )

    def __str__(self):
        if self.chequebook:
            return "{0} - {1}".format(self.chequebook.explanation[0:50], self.serial)
        else:
            return "{0} - {1}".format(self.explanation[0:50], self.serial)

    class Meta:
        ordering = ['serial', ]


class StatusChange(models.Model):

    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='statusChanges')
    sanad = models.ForeignKey(Sanad, on_delete=models.CASCADE, related_name='statusChange', blank=True, null=True)

    bedAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='chequeStatusChangesAsBedAccount')
    bedFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='chequeStatusChangesAsBesAccount', blank=True, null=True)
    besAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='chequeStatusChangesAsBedFloatAccount')
    besFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='chequeStatusChangesAsBesFloatAccount', blank=True, null=True)

    date = jmodels.jDateField()
    explanation = models.CharField(max_length=255, blank=True)
    transferNumber = models.IntegerField(null=True)

    fromStatus = models.CharField(max_length=30, choices=CHECK_STATUSES)
    toStatus = models.CharField(max_length=30, choices=CHECK_STATUSES)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    permissions = (
        ('get_cheque', 'Can get cheques')
    )

    # def __str__(self):
    #     return "{0} - {1}".format(self.serial, self.explanation[0:30])

    class Meta:
        ordering = ['id', ]


signals.post_save.connect(receiver=createCheques, sender=Chequebook)
signals.pre_save.connect(receiver=validateChequebookUpdate, sender=Chequebook)
signals.pre_save.connect(receiver=validateChequeUpdate, sender=Cheque)

signals.post_save.connect(receiver=statusChangeSanad, sender=StatusChange)


def deleteStatusChange(sender, instance, using, **kwargs):
    cheque = instance.cheque
    lastStatusChangeId = StatusChange.objects.filter(cheque=cheque).latest('id').id

    if instance.id != lastStatusChangeId:
        raise serializers.ValidationError("ابتدا تغییرات جلوتر را پاک کنید")

    if cheque.statusChanges.count() == 1:
        if instance.cheque.type == 'received':
            raise serializers.ValidationError("این وضعیت غیر قابل حذف می باشد")
        else:
            cheque.account = None
            cheque.floatAccount = None
            cheque.value = None
            cheque.due = None
            cheque.date = None
            cheque.explanation = ''
            cheque.lastAccount = None
            cheque.lastFloatAccount = None

    if not cheque.transactionItem.all():
        clearSanad(instance.sanad)

    cheque.status = instance.fromStatus
    cheque.save()

signals.pre_delete.connect(receiver=deleteStatusChange, sender=StatusChange)

