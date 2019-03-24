from django.db.models import Max

from sanads.sanads.models import Sanad, SanadItem, clearSanad


def updateSanad(sender, instance, created, **kwargs):
    t = instance
    sanad = instance.sanad

    if t.type == 'receive':
        rowsType = 'bed'
        lastRowType = 'bes'
        rp = 'دریافت'
    else:
        rowsType = 'bes'
        lastRowType = 'bed'
        rp = 'پرداخت'

    clearSanad(sanad)

    sanad.explanation = t.explanation
    sanad.date = t.date
    sanad.type = 'temporary'
    sanad.save()

    typeNames = []
    totalValue = 0
    for item in t.items.all():

        totalValue += item.value
        if item.type.name not in typeNames:
            typeNames.append(item.type.name)

        sanad.items.create(
            value=item.value,
            valueType=rowsType,
            explanation="بابت {0} {1} به شماره مستند {2} به تاریخ {3}".format(rp, item.type.name, item.documentNumber, str(item.date)),
            account=item.account,
            floatAccount=item.floatAccount,
        )

    if len(t.items.all()) != 0:
        sanad.items.create(
            value=totalValue,
            valueType=lastRowType,
            explanation="بابت {0} {1} طی {0} شماره {2}".format(rp, ', '.join(typeNames), t.code),
            account=t.account,
            floatAccount=t.floatAccount
        )


def updateSanadItems(sender, instance, created=None, **kwargs):
    t = instance.transaction
    updateSanad(sender='updateSanadItems', instance=t, created=None)


def clearTransactionSanad(sender, instance, created=None, **kwargs):
    clearSanad(instance.sanad)

