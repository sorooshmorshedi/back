from django.contrib.admin.options import get_content_type_for_model
from django.db import models
from django.db.models import Sum
from django.db.models.functions.comparison import Coalesce
from django.db.models.query_utils import Q
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account, FloatAccount
from accounts.defaultAccounts.models import DefaultAccount
from cheques.models.ChequeModel import Cheque
from companies.models import FinancialYear
from helpers.functions import sanad_exp
from helpers.models import BaseModel, DECIMAL, DefinableMixin, LockableMixin, EXPLANATION
from helpers.views.MassRelatedCUD import MassRelatedCUD

from sanads.models import Sanad, newSanadCode, clearSanad


class Transaction(BaseModel, DefinableMixin, LockableMixin):
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
        unique_together = ('code', 'type', 'financial_year')
        permissions = (
            ('get.receiveTransaction', 'مشاهده دریافت'),
            ('create.receiveTransaction', 'تعریف دریافت'),
            ('update.receiveTransaction', 'ویرایش دریافت'),
            ('delete.receiveTransaction', 'حذف دریافت'),
            ('define.receiveTransaction', 'قطعی کردن دریافت'),
            ('lock.receiveTransaction', 'قفل کردن دریافت'),

            ('get.paymentTransaction', 'مشاهده پرداخت'),
            ('create.paymentTransaction', 'تعریف پرداخت'),
            ('update.paymentTransaction', 'ویرایش پرداخت'),
            ('delete.paymentTransaction', 'حذف پرداخت'),
            ('define.paymentTransaction', 'قطعی کردن پرداخت'),
            ('lock.paymentTransaction', 'قفل کردن پرداخت'),

            ('get.imprestTransaction', 'مشاهده پرداخت تنخواه'),
            ('create.imprestTransaction', 'تعریف پرداخت تنخواه'),
            ('update.imprestTransaction', 'ویرایش پرداخت تنخواه'),
            ('delete.imprestTransaction', 'حذف پرداخت تنخواه'),
            ('define.imprestTransaction', 'قطعی کردن پرداخت تنخواه'),
            ('lock.imprestTransaction', 'قفل کردن پرداخت تنخواه'),

            ('getOwn.receiveTransaction', 'مشاهده دریافت های خود'),
            ('updateOwn.receiveTransaction', 'ویرایش دریافت های خود'),
            ('deleteOwn.receiveTransaction', 'حذف دریافت های خود'),
            ('defineOwn.receiveTransaction', 'قطعی کردن دریافت های خود'),
            ('lockOwn.receiveTransaction', 'قفل کردن دریافت های خود'),

            ('getOwn.paymentTransaction', 'مشاهده پرداخت های خود'),
            ('updateOwn:.paymentTransaction', 'ویرایش پرداخت های خود'),
            ('deleteOwn.paymentTransaction', 'حذف پرداخت های خود'),
            ('defineOwn.paymentTransaction', 'قطعی کردن پرداخت های خود'),
            ('lockOwn.paymentTransaction', 'قفل کردن پرداخت های خود'),

            ('getOwn.imprestTransaction', 'مشاهده پرداخت تنخواه های خود'),
            ('updateOwn.imprestTransaction', 'ویرایش پرداخت تنخواه های خود'),
            ('deleteOwn.imprestTransaction', 'حذف پرداخت تنخواه های خود'),
            ('defineOwn.imprestTransaction', 'قطعی کردن پرداخت تنخواه های خود'),
            ('lockOwn.imprestTransaction', 'قفل کردن پرداخت تنخواه های خود'),

        )

    def sync(self, user, data):
        from transactions.serializers import TransactionItemCreateUpdateSerializer
        from factors.serializers import FactorPaymentSerializer
        from cheques.views import SubmitChequeApiView
        from factors.models.factor import FactorPayment
        from factors.models import Factor

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

        factor_ids_to_update = [o['factor'] for o in payments_data.get('items')]
        factor_ids_to_update += [o.factor_id for o in
                                 FactorPayment.objects.filter(id__in=payments_data.get('ids_to_delete'))]

        MassRelatedCUD(
            user,
            payments_data.get('items'),
            payments_data.get('ids_to_delete'),
            'transaction',
            self.id,
            FactorPaymentSerializer,
            FactorPaymentSerializer
        ).sync()

        if self.is_defined:
            for factor in Factor.objects.filter(id__in=factor_ids_to_update).all():
                factor.paidValue = factor.payments.filter(is_defined=True).aggregate(Sum('value'))['value__sum'] or 0
                factor.save()

    @property
    def sum(self):
        return TransactionItem.objects.filter(transaction=self).aggregate(sum=Coalesce(Sum('value'), 0))['sum']

    @property
    def label(self):
        return [t[1] for t in self.TYPES if t[0] == self.type][0]

    def _createSanad(self, user):
        sanad = Sanad(code=newSanadCode(), financial_year=self.financial_year, date=self.date)
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

        explanation = ''
        if self.type == self.RECEIVE:
            explanation = sanad_exp(
                'بابت دریافت',
                'شماره',
                self.code,
                self.explanation
            )
        elif self.type == self.PAYMENT:
            explanation = sanad_exp(
                'بابت پرداخت',
                'شماره',
                self.code,
                'مورخ',
                self.date,
                self.explanation
            )
        elif self.type == self.IMPREST:
            explanation = sanad_exp(
                'بابت پرداخت تنخواه شماره',
                self.code,
                'مورخ',
                self.date,
                'جهت',
                self.explanation
            )

        sanad.explanation = explanation
        sanad.date = self.date
        sanad.origin_content_type = get_content_type_for_model(Transaction)
        sanad.origin_id = self.id
        sanad.save()

        typeNames = []
        totalValue = 0
        for item in self.items.all():

            totalValue += item.value
            if item.type.name not in typeNames:
                typeNames.append(item.type.name)

            bed = 0
            bes = 0

            row_explanation = ''
            if self.type == Transaction.RECEIVE:
                bed = item.value
                row_explanation = sanad_exp(
                    'بابت دریافت شماره',
                    self.code,
                    'به شماره پیگیری',
                    item.documentNumber,
                    'مورخ',
                    item.date,
                    item.explanation
                )
            else:
                bes = item.value
                if self.type == Transaction.PAYMENT:
                    row_explanation = sanad_exp(
                        'بابت پرداخت شماره',
                        self.code,
                        'به شماره پیگیری',
                        item.documentNumber,
                        'مورخ',
                        item.date,
                        item.explanation
                    )
                elif self.type == Transaction.IMPREST:
                    row_explanation = sanad_exp(
                        'بابت پرداخت تنخواه شماره',
                        self.code,
                        'مورخ',
                        item.date,
                        'به شماره پیگیری',
                        item.documentNumber,
                        'جهت',
                        item.explanation
                    )

            sanad.items.create(
                bed=bed,
                bes=bes,
                explanation=row_explanation,
                account=item.account,
                floatAccount=item.floatAccount,
                costCenter=item.costCenter,
                financial_year=sanad.financial_year
            )

        last_bed = 0
        last_bes = 0
        last_row_explanation = ''

        if self.type == Transaction.RECEIVE:
            last_bes = totalValue
            last_row_explanation = sanad_exp(
                'بابت واریز طی دریافت شماره',
                self.code,
                self.explanation
            )
        else:
            last_bed = totalValue
            if self.type == Transaction.PAYMENT:
                last_row_explanation = sanad_exp(
                    'بابت دریافت طی شماره پرداخت',
                    self.code,
                    'مورخ',
                    self.date,
                    self.explanation
                )
            elif self.type == Transaction.IMPREST:
                last_row_explanation = sanad_exp(
                    'بابت دریافت تنخواه شماره',
                    self.code,
                    'مورخ',
                    self.date,
                    self.explanation
                )

        if len(self.items.all()) != 0:
            sanad.items.create(
                bed=last_bed,
                bes=last_bes,
                explanation=last_row_explanation,
                account=self.account,
                floatAccount=self.floatAccount,
                costCenter=self.costCenter,
                financial_year=sanad.financial_year
            )

        sanad.update_values()
        sanad.define()

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
        queryset = Transaction.objects.hasAccess('get', 'imprestTransaction').filter(
            is_defined=True,
            type=Transaction.IMPREST
        ).filter(
            Q(imprestSettlement=None) | Q(imprestSettlement__is_settled=False)
        )

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
    value = DECIMAL()
    date = jmodels.jDateField()
    due = jmodels.jDateField(null=True, blank=True)
    documentNumber = models.CharField(max_length=50, null=True, blank=True)
    bankName = models.CharField(max_length=255, null=True, blank=True)
    explanation = EXPLANATION()

    file = models.FileField(blank=True, null=True)

    order = models.IntegerField(default=0)

    def __str__(self):
        return "{0} - {1}".format(self.transaction.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        pass
