from django.db import models
from django.db.models import signals
from django_jalali.db import models as jmodels
from rest_framework import serializers

from accounts.accounts.models import Account, FloatAccount
from sanads.sanads.models import Sanad, clearSanad

CHECK_STATUSES = (
    ('blank', 'blank'),
    ('notPassed', 'notPassed'),
    ('inFlow', 'inFlow'),
    ('passed', 'passed'),
    ('bounced', 'bounced'),
    ('cashed', 'cashed'),
    ('revoked', 'revoked'),
    ('transferred', 'transferred'),
    ('', 'any'),
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

    RECEIVED = 'r'
    PAID = 'p'

    PERSONAL = 'p'
    COMPANY = 'c'
    OTHER_PERSON = 'op'
    OTHER_COMPANY = 'oc'

    CHEQUE_TYPES = (
        (PERSONAL, 'شخصی'),
        (OTHER_PERSON, 'شخصی سایرین'),
        (COMPANY, 'شرکت'),
        (OTHER_COMPANY, 'شرکت سایرین')
    )

    serial = models.IntegerField()
    chequebook = models.ForeignKey(Chequebook, on_delete=models.CASCADE, related_name='cheques', blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='receivedCheques', blank=True, null=True)
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='receivedCheques', blank=True, null=True)

    value = models.DecimalField(max_digits=24, decimal_places=0, blank=True, null=True)
    due = jmodels.jDateField(blank=True, null=True)
    date = jmodels.jDateField(blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, choices=CHECK_STATUSES)
    received_or_paid = models.CharField(max_length=10, choices=((RECEIVED, 'دریافتنی'), (PAID, 'پرداختنی')))
    type = models.CharField(max_length=1, choices=CHEQUE_TYPES)

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
            return "{} - {} - {}".format(self.received_or_paid, self.chequebook.explanation[0:50], self.serial)
        else:
            return "{} - {} - {}".format(self.received_or_paid, self.explanation[0:50], self.serial)

    class Meta:
        ordering = ['serial', ]


class StatusChange(models.Model):

    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='statusChanges')
    sanad = models.OneToOneField(Sanad, on_delete=models.CASCADE, related_name='statusChange', blank=True, null=True)

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


def createCheques(sender, instance, created, **kwargs):
    if created:
        bank = instance.account.bank
        for i in range(instance.serial_from, instance.serial_to + 1):
            instance.cheques.create(
                serial=i,
                status='blank',
                received_or_paid=Cheque.PAID,
                bankName=bank.name,
                branchName=bank.branch,
                accountNumber=bank.accountNumber,
            )
    else:
        for cheque in instance.cheques.all():
            cheque.delete()
        for i in range(instance.serial_from, instance.serial_to + 1):
            instance.cheques.create(
                serial=i,
                status='blank',
                received_or_paid=Cheque.PAID,
            )


def validateChequebookUpdate(sender, instance, raw, using, update_fields, **kwargs):
    if update_fields \
            and ('serial_from' not in update_fields or instance.serial_from == update_fields['serial_from']) \
            and ('serial_to' not in update_fields or instance.serial_to == update_fields['serial_to']):
        return
    for cheque in instance.cheques.all():
        if cheque.status != 'blank':
            raise serializers.ValidationError("برای ویرایش دسته چک، باید وضعیت همه چک های آن سفید باشد")


def validateChequeUpdate(sender, instance, raw, using, update_fields, **kwargs):
    if not update_fields or instance.status == 'blank':
        return
    for i in update_fields:
        if i not in ['status']:
            raise serializers.ValidationError("فقط چک های سفید قابل ویرایش هستند")


def statusChangeSanad(sender, instance, created, **kwargs):
    value = instance.cheque.value
    cheque = instance.cheque
    sanad = instance.sanad
    if not created:
        clearSanad(sanad)
    sanad.explanation = cheque.explanation
    sanad.date = cheque.date

    if cheque.received_or_paid == Cheque.PAID:
        received_or_paid = 'پرداخت'
    else:
        received_or_paid = 'دریافت'

    if instance.toStatus == 'notPassed' and instance.fromStatus != 'inFlow':
        explanation = "بابت {0} چک شماره {1} به تاریخ سررسید {2} به {3}".format(received_or_paid, cheque.serial, str(cheque.due), cheque.account.name)
    else:
        newStatus = instance.toStatus
        print(instance.fromStatus, newStatus)
        if instance.fromStatus == 'inFlow' and newStatus in ('notPassed', 'bounced'):
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
        explanation = "بابت {0} چک شماره {1} به تاریخ سررسید {2} ".format(statuses[newStatus], cheque.serial, str(cheque.due))

    sanad.items.create(
        value=value,
        valueType='bed',
        explanation=explanation,
        account=instance.bedAccount,
        floatAccount=instance.bedFloatAccount,
    )
    sanad.items.create(
        value=value,
        valueType='bes',
        explanation=explanation,
        account=instance.besAccount,
        floatAccount=instance.besFloatAccount,
    )
    sanad.type = 'temporary'
    sanad.save()


def deleteStatusChange(sender, instance, using, **kwargs):
    cheque = instance.cheque
    lastStatusChangeId = StatusChange.objects.filter(cheque=cheque).latest('id').id

    if instance.id != lastStatusChangeId:
        raise serializers.ValidationError("ابتدا تغییرات جلوتر را پاک کنید")

    if cheque.statusChanges.count() == 1:
        if instance.cheque.received_or_paid == Cheque.PAID:
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


signals.post_save.connect(receiver=createCheques, sender=Chequebook)
signals.pre_save.connect(receiver=validateChequebookUpdate, sender=Chequebook)
signals.pre_save.connect(receiver=validateChequeUpdate, sender=Cheque)
signals.post_save.connect(receiver=statusChangeSanad, sender=StatusChange)
signals.pre_delete.connect(receiver=deleteStatusChange, sender=StatusChange)

