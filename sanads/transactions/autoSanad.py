from django.db.models import Max

from sanads.sanads.models import Sanad, SanadItem


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

    print(t.sanad)
    print(sanad)
    sanad.explanation = "{0} - {1}".format(t.code, t.explanation)
    sanad.date = t.date
    sanad.type = 'temporary'
    sanad.save()

    clearSanad(sender='updateSanad', instance=sanad, created=None)

    typeNames = []
    totalValue = 0
    for item in t.items.all():

        totalValue += item.value
        if item.type.name not in typeNames:
            typeNames.append(item.type.name)

        sanad.items.create(
            value=item.value,
            valueType=rowsType,
            explanation="بابت {0} {1} به شماره مستند {2} به تاریخ {3}".format(rp, item.type.name, item.documentNumber, item.date),
            account=item.account,
            floatAccount=item.floatAccount,
            type=item.type,
        )

    if len(t.items.all()) != 0:
        sanad.items.create(
            value=totalValue,
            valueType=lastRowType,
            explanation="بابت {0} {1} طی {0} شماره {2}".format(rp, ', '.join(typeNames), t.code),
            account=t.account,
            # floatAccount=t.floatAccount, ???
        )


def updateSanadItems(sender, instance, created=None, **kwargs):
    print(instance.transaction.id)
    t = instance.transaction
    updateSanad(sender='updateSanadItems', instance=t, created=None)


def clearSanad(sender, instance, created=None, **kwargs):
    for item in instance.items.all():
        item.delete()
