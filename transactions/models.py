from django.db import models
from django.db.models import Sum
from django.db.models.query_utils import Q
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account, FloatAccount
from accounts.defaultAccounts.models import DefaultAccount
from cheques.models.ChequeModel import Cheque
from companies.models import FinancialYear
from helpers.models import BaseModel, ConfirmationMixin
from helpers.views.MassRelatedCUD import MassRelatedCUD

from sanads.models import Sanad, newSanadCode, clearSanad


class Transaction(BaseModel, ConfirmationMixin):
    RECEIVE = 'receive'
    PAYMENT = 'payment'
    IMPREST = 'imprest'
    TYPES = (
        (RECEIVE, 'دریافت'),
        (PAYMENT, 'پرداخت'),
        (IMPREST, 'پرداخت تنخواه'),
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='transactions')
    code = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactions')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='transactions', blank=True,
                                     null=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='transactionsAsCostCenter',
                                   blank=True, null=True)
    date = jmodels.jDateField()
    explanation = models.CharField(max_length=255, blank=True)
    sanad = models.OneToOneField(Sanad, on_delete=models.CASCADE, related_name='transaction', blank=True, null=True)

    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    type = models.CharField(max_length=20, choices=TYPES)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        ordering = ['code', ]
        unique_together = ('code', 'type')
        permissions = (
            ('get.receiveTransaction', 'مشاهده دریافت'),
            ('create.receiveTransaction', 'تعریف دریافت'),
            ('update.receiveTransaction', 'ویرایش دریافت'),
            ('delete.receiveTransaction', 'حذف دریافت'),

            ('get.paymentTransaction', 'مشاهده پرداخت'),
            ('create.paymentTransaction', 'تعریف پرداخت'),
            ('update.paymentTransaction', 'ویرایش پرداخت'),
            ('delete.paymentTransaction', 'حذف پرداخت'),

            ('get.imprestTransaction', 'مشاهده پرداخت تنخواه'),
            ('create.imprestTransaction', 'تعریف پرداخت تنخواه'),
            ('update.imprestTransaction', 'ویرایش پرداخت تنخواه'),
            ('delete.imprestTransaction', 'حذف پرداخت تنخواه'),

            ('firstConfirm.receiveTransaction', 'تایید اول دریافت '),
            ('secondConfirm.receiveTransaction', 'تایید دوم دریافت '),
            ('firstConfirmOwn.receiveTransaction', 'تایید اول دریافت های خود'),
            ('secondConfirmOwn.receiveTransaction', 'تایید دوم دریافت های خود'),

            ('firstConfirm.paymentTransaction', 'تایید اول پرداخت '),
            ('secondConfirm.paymentTransaction', 'تایید دوم پرداخت '),
            ('firstConfirmOwn.paymentTransaction', 'تایید اول پرداخت های خود'),
            ('secondConfirmOwn.paymentTransaction', 'تایید دوم پرداخت های خود'),

            ('firstConfirm.imprestTransaction', 'تایید اول تنخواه '),
            ('secondConfirm.imprestTransaction', 'تایید دوم تنخواه '),
            ('firstConfirmOwn.imprestTransaction', 'تایید اول تنخواه های خود'),
            ('secondConfirmOwn.imprestTransaction', 'تایید دوم تنخواه های خود'),

        )

    def sync(self, user, data):
        from transactions.serializers import TransactionItemCreateUpdateSerializer
        from factors.serializers import FactorPaymentSerializer
        from cheques.views import SubmitChequeApiView

        items_data = data.get('items')
        payments_data = data.get('payments')

        for i in range(len(items_data.get('items'))):
            item = items_data['items'][i]
            cheque_data = item.get('cheque')
            if cheque_data:
                if item.get('id'):
                    items_data['items'].pop(i)
                else:
                    cheque_data['has_transaction'] = True
                    cheque = SubmitChequeApiView.submitCheque(user, cheque_data)
                    item['cheque'] = cheque.id

        MassRelatedCUD(
            user,
            items_data.get('items'),
            items_data.get('ids_to_delete'),
            'transaction',
            self.id,
            TransactionItemCreateUpdateSerializer,
            TransactionItemCreateUpdateSerializer,
        ).sync()

        MassRelatedCUD(
            user,
            payments_data.get('items'),
            payments_data.get('ids_to_delete'),
            'transaction',
            self.id,
            FactorPaymentSerializer,
            FactorPaymentSerializer
        ).sync()

    @property
    def sum(self):
        return TransactionItem.objects.filter(transaction=self).aggregate(Sum('value'))['value__sum']

    @property
    def label(self):
        return [t[1] for t in self.TYPES if t[0] == self.type][0]

    def _createSanad(self, user):
        sanad = Sanad(code=newSanadCode(), financial_year=self.financial_year,
                      date=self.date, is_auto_created=True)
        sanad.save()
        self.sanad = sanad
        self.save()
        return sanad

    def updateSanad(self, user):
        sanad = self.sanad
        if not sanad:
            sanad = self._createSanad(user)

        clearSanad(sanad)

        sanad.is_auto_created = True
        sanad.explanation = self.explanation
        sanad.date = self.date
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
                costCenter=item.costCenter,
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
                costCenter=self.costCenter,
                financial_year=sanad.financial_year
            )

    def delete(self, *args, **kwargs):
        clearSanad(self.sanad)
        return super(Transaction, self).delete(*args, **kwargs)

    @staticmethod
    def newCodes(transaction_type=None):
        codes = {}
        for type in Transaction.TYPES:
            type = type[0]
            if transaction_type:
                if type != transaction_type:
                    continue
            try:
                codes[type] = Transaction.objects.inFinancialYear().filter(type=type).latest('code').code + 1
            except:
                codes[type] = 1
        if transaction_type:
            return codes[transaction_type]
        else:
            return codes

    @staticmethod
    def get_not_settled_imprests_queryset(account_id=None, floatAccount_id=None, costCenter_id=None):
        queryset = Transaction.objects.hasAccess('get', 'imprestTransaction') \
            .filter(type=Transaction.IMPREST) \
            .filter(Q(imprestSettlements__isnull=True) | Q(imprestSettlements__is_settled=False))

        if account_id:
            queryset = queryset.filter(account__id=account_id)
        if floatAccount_id:
            queryset = queryset.filter(floatAccount__id=floatAccount_id)
        if costCenter_id:
            queryset = queryset.filter(costCenter__id=costCenter_id)

        return queryset


class TransactionItem(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='transactionItems')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactionItems')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='transactionItems',
                                     blank=True, null=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='transactionItemsAsCostCenter',
                                   blank=True, null=True)
    cheque = models.OneToOneField(Cheque, on_delete=models.CASCADE, related_name='transactionItem', blank=True,
                                  null=True)

    type = models.ForeignKey(DefaultAccount, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=24, decimal_places=0)
    date = jmodels.jDateField()
    due = jmodels.jDateField(null=True, blank=True)
    documentNumber = models.CharField(max_length=50, null=True, blank=True)
    bankName = models.CharField(max_length=255, null=True, blank=True)
    explanation = models.CharField(max_length=255, default="", blank=True)

    file = models.FileField(blank=True, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.transaction.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        pass
