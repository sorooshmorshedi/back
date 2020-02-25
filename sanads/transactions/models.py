from django.db import models
from django.db.models import signals, Sum
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account, FloatAccount
from accounts.defaultAccounts.models import DefaultAccount
from cheques.models.ChequeModel import Cheque
from companies.models import FinancialYear
from helpers.models import BaseModel

from sanads.sanads.models import Sanad, newSanadCode, clearSanad


class Transaction(BaseModel):
    RECEIVE = 'receive'
    PAYMENT = 'payment'
    TYPES = (
        (RECEIVE, 'دریافت'),
        (PAYMENT, 'پرداخت'),
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='transactions')
    code = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactions')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='transactions', blank=True,
                                     null=True)
    date = jmodels.jDateField()
    explanation = models.CharField(max_length=255, blank=True)
    sanad = models.OneToOneField(Sanad, on_delete=models.CASCADE, related_name='transaction', blank=True, null=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    type = models.CharField(max_length=20, choices=TYPES)

    permissions = (
        ('get_sanad', 'Can get sanads')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        ordering = ['code', ]
        unique_together = ('code', 'type')

    @property
    def sum(self):
        return TransactionItem.objects.filter(transaction=self).aggregate(Sum('value'))['value__sum']

    @property
    def label(self):
        return [t[1] for t in self.TYPES if t[0] == self.type][0]

    def createSanad(self, user):
        sanad = Sanad(code=newSanadCode(user), financial_year=self.financial_year,
                      date=self.date, createType=Sanad.AUTO)
        sanad.save()
        self.sanad = sanad
        self.save()

    def updateSanad(self):
        sanad = self.sanad
        if not sanad:
            raise Sanad.DoesNotExist

        clearSanad(sanad)

        sanad.explanation = self.explanation
        sanad.date = self.date
        sanad.type = Sanad.TEMPORARY
        sanad.save()

        typeNames = []
        totalValue = 0
        for item in self.items.all():

            totalValue += item.value
            if item.type.name not in typeNames:
                typeNames.append(item.type.name)

            bed = 0
            bes = 0

            if self.type == Transaction.RECEIVE:
                bed = item.value
                rp = 'دریافت'
            else:
                bes = item.value
                rp = 'پرداخت'

            sanad.items.create(
                bed=bed,
                bes=bes,
                explanation="بابت {0} {1} به شماره مستند {2} به تاریخ {3}".format(rp, item.type.name,
                                                                                  item.documentNumber, str(item.date)),
                account=item.account,
                floatAccount=item.floatAccount,
                financial_year=sanad.financial_year
            )

        last_bed = 0
        last_bes = 0

        if self.type == Transaction.RECEIVE:
            last_bes = totalValue
            rp = 'دریافت'
        else:
            last_bed = totalValue
            rp = 'پرداخت'

        if len(self.items.all()) != 0:
            sanad.items.create(
                bed=last_bed,
                bes=last_bes,
                explanation="بابت {0} {1} طی {0} شماره {2}".format(rp, ', '.join(typeNames), self.code),
                account=self.account,
                floatAccount=self.floatAccount,
                financial_year=sanad.financial_year
            )

    @staticmethod
    def newCodes(user, transaction_type=None):
        codes = {}
        for type in Transaction.TYPES:
            type = type[0]
            if transaction_type:
                if type != transaction_type:
                    continue
            try:
                codes[type] = Transaction.objects.inFinancialYear(user).filter(type=type).latest('code').code + 1
            except:
                codes[type] = 1
        if transaction_type:
            return codes[transaction_type]
        else:
            return codes


class TransactionItem(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='transactionItems')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactionItems')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='transactionItems',
                                     blank=True, null=True)
    cheque = models.OneToOneField(Cheque, on_delete=models.CASCADE, related_name='transactionItem', blank=True,
                                  null=True)

    type = models.ForeignKey(DefaultAccount, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=24, decimal_places=0)
    date = jmodels.jDateField()
    due = jmodels.jDateField(null=True, blank=True)
    documentNumber = models.CharField(max_length=50, blank=True)
    bankName = models.CharField(max_length=255, blank=True)
    explanation = models.CharField(max_length=255, blank=True)

    file = models.FileField(blank=True, null=True)

    permissions = (
        ('get_sanad', 'Can get sanads')
    )

    def __str__(self):
        return "{0} - {1}".format(self.transaction.code, self.explanation[0:30])

# signals.post_save.connect(receiver=updateSanad, sender=Transaction)
# signals.post_save.connect(receiver=updateSanadItems, sender=TransactionItem)
# signals.post_delete.connect(receiver=clearTransactionSanad, sender=Transaction)
# signals.post_delete.connect(receiver=updateSanadItems, sender=TransactionItem)
