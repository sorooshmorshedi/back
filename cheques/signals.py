from rest_framework import serializers
from django.db.models import signals
from cheques.models import Cheque, Chequebook, StatusChange
from sanads.sanads.models import clearSanad


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
                financial_year=instance.financial_year
            )
    else:
        for cheque in instance.cheques.all():
            cheque.delete()
        for i in range(instance.serial_from, instance.serial_to + 1):
            instance.cheques.create(
                serial=i,
                status='blank',
                received_or_paid=Cheque.PAID,
                financial_year=instance.financial_year
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
    if cheque.has_transaction and instance.fromStatus == 'blank':
        return
    sanad = instance.sanad
    if not sanad:
        return
    if not created:
        clearSanad(sanad)
    sanad.explanation = cheque.explanation
    sanad.date = cheque.date

    if cheque.received_or_paid == Cheque.PAID:
        received_or_paid = 'پرداخت'
    else:
        received_or_paid = 'دریافت'

    if instance.toStatus == 'notPassed' and instance.fromStatus != 'inFlow':
        explanation = "بابت {0} چک شماره {1} به تاریخ سررسید {2} از {3}".format(received_or_paid, cheque.serial, str(cheque.due), cheque.account.name)
    else:
        newStatus = instance.toStatus
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
        financial_year=sanad.financial_year
    )
    sanad.items.create(
        value=value,
        valueType='bes',
        explanation=explanation,
        account=instance.besAccount,
        floatAccount=instance.besFloatAccount,
        financial_year=sanad.financial_year
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

    if not cheque.has_transaction:
        clearSanad(instance.sanad)

    cheque.status = instance.fromStatus

    if cheque.received_or_paid == Cheque.RECEIVED:
        lastAccount = instance.besAccount
        lastFloatAccount = instance.besFloatAccount
    else:
        lastAccount = instance.bedAccount
        lastFloatAccount = instance.bedFloatAccount

    cheque.lastAccount = lastAccount
    cheque.lastFloatAccount = lastFloatAccount

    cheque.save()


def saveCheque(sender, instance, created, **kwargs):
    cheque = instance
    if not created:
        if cheque.has_transaction:
            from sanads.transactions.models import TransactionItem
            try:
                ti = TransactionItem.objects.get(cheque=cheque)
            except TransactionItem.DoesNotExist:
                return
            ti.documentNumber = cheque.serial
            ti.date = cheque.date
            ti.due = cheque.due
            ti.explanation = cheque.explanation
            ti.value = cheque.value
            ti.save()

signals.pre_save.connect(receiver=validateChequebookUpdate, sender=Chequebook)
signals.post_save.connect(receiver=createCheques, sender=Chequebook)

signals.pre_save.connect(receiver=validateChequeUpdate, sender=Cheque)
signals.post_save.connect(receiver=saveCheque, sender=Cheque)

signals.pre_delete.connect(receiver=deleteStatusChange, sender=StatusChange)
signals.post_save.connect(receiver=statusChangeSanad, sender=StatusChange)



