from django.db.models import Max

from sanads.sanads.models import Sanad, SanadItem, clearSanad, newSanadCode
from sanads.transactions.models import Transaction


def updateSanad(sender, instance, created, **kwargs):
    t = instance
    sanad = instance.sanad

    if not sanad:
        return

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

        bed = bes = 0
        if t.type == Transaction.RECEIVE:
            bed = item.value
            rp = 'دریافت'
        else:
            bes = item.value
            rp = 'پرداخت'

        sanad.items.create(
            bed=bed,
            bes=bes,
            explanation="بابت {0} {1} به شماره مستند {2} به تاریخ {3}".format(rp, item.type.name, item.documentNumber,
                                                                              str(item.date)),
            account=item.account,
            floatAccount=item.floatAccount,
            financial_year=sanad.financial_year
        )

    bed = bes = 0
    if t.type == Transaction.RECEIVE:
        bes = totalValue
        rp = 'دریافت'
    else:
        bed = totalValue
        rp = 'پرداخت'

    if len(t.items.all()) != 0:
        sanad.items.create(
            bed=bed,
            bes=bes,
            explanation="بابت {0} {1} طی {0} شماره {2}".format(rp, ', '.join(typeNames), t.code),
            account=t.account,
            floatAccount=t.floatAccount,
            financial_year=sanad.financial_year
        )


def updateSanadItems(sender, instance, created=None, **kwargs):
    t = instance.transaction
    updateSanad(sender='updateSanadItems', instance=t, created=None)


def clearTransactionSanad(sender, instance, created=None, **kwargs):
    clearSanad(instance.sanad)
