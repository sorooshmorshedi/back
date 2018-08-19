from rest_framework import serializers

from sanads.sanads.models import clearSanad


def createCheques(sender, instance, created, **kwargs):
    if created:
        for i in range(instance.serial_from, instance.serial_to + 1):
            instance.cheques.create(
                serial=i,
                status='blank',
                type='paid',
            )
    else:
        for cheque in instance.cheques.all():
            cheque.delete()
        for i in range(instance.serial_from, instance.serial_to + 1):
            instance.cheques.create(
                serial=i,
                status='blank',
                type='paid',
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

    if cheque.type == 'paid':
        chequeType = 'پرداخت'
    else:
        chequeType = 'دریافت'

    if instance.toStatus == 'notPassed' and instance.fromStatus != 'inFlow':
        explanation = "بابت {0} چک شماره {1} به تاریخ سررسید {2} به {3}".format(chequeType, cheque.serial, str(cheque.due), cheque.account.name)
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


