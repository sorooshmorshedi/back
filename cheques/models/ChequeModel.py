from django.db import models
from django.db.models import Q
from django_jalali.db import models as jmodels
from accounts.accounts.models import Account, FloatAccount
from accounts.defaultAccounts.models import DefaultAccount
from cheques.models.ChequebookModel import Chequebook
from companies.models import FinancialYear
from helpers.models import BaseModel, ConfirmationMixin, BaseManager

CHEQUE_STATUSES = (
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


class ChequeManager(BaseManager):

    def inFinancialYear(self, financial_year=None):
        from helpers.functions import get_current_user
        qs = super().get_queryset()

        if not financial_year:
            user = get_current_user()

            if not user:
                return super().get_queryset()

            financial_year = user.active_financial_year

        qs = qs.filter(financial_year__company=financial_year.company)

        return qs.filter(
            Q(
                Q(financial_year__id__lt=financial_year.id) & Q(status__in=('blank', 'notPassed', 'bounced'))
            ) | Q(
                financial_year__id=financial_year.id
            )
        )


class Cheque(BaseModel, ConfirmationMixin):
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

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='cheques')
    serial = models.IntegerField()
    chequebook = models.ForeignKey(Chequebook, on_delete=models.CASCADE, related_name='cheques', blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='receivedCheques', blank=True,
                                null=True)
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='receivedCheques', blank=True,
                                     null=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='receivedChequesAsCostCenter',
                                   blank=True, null=True)

    value = models.DecimalField(max_digits=24, decimal_places=0, blank=True, null=True)
    due = jmodels.jDateField(blank=True, null=True)
    date = jmodels.jDateField(blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, choices=CHEQUE_STATUSES)
    received_or_paid = models.CharField(max_length=10, choices=((RECEIVED, 'دریافتنی'), (PAID, 'پرداختنی')))
    type = models.CharField(max_length=2, choices=CHEQUE_TYPES, blank=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    lastAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='lastCheques', blank=True,
                                    null=True)
    lastFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='lastCheques', blank=True,
                                         null=True)
    lastCostCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='lastChequesAsCostCenter',
                                       blank=True,
                                       null=True)

    bankName = models.CharField(max_length=100, null=True, blank=True)
    branchName = models.CharField(max_length=100, null=True, blank=True)
    accountNumber = models.CharField(max_length=50, null=True, blank=True)

    has_transaction = models.BooleanField(default=False)

    objects = ChequeManager()

    def __str__(self):
        if self.chequebook:
            return "{} - {} - {}".format(self.received_or_paid, self.chequebook.explanation[0:50], self.serial)
        else:
            return "{} - {} - {}".format(self.received_or_paid, self.explanation[0:50], self.serial)

    class Meta(BaseModel.Meta):
        verbose_name = 'چک'
        ordering = ['serial', ]
        permissions = (
            ('get.receivedCheque', 'مشاهده چک دریافتی'),
            ('update.receivedCheque', 'ویرایش چک دریافتی'),
            ('delete.receivedCheque', 'حذف چک دریافتی'),

            ('submit.receivedCheque', 'ثبت چک دریافتی'),
            ('changeStatus.receivedCheque', 'تغییر وضعیت دریافتی'),

            ('get.paidCheque', 'مشاهده چک پرداختی'),
            ('update.paidCheque', 'ویرایش چک پرداختی'),
            ('delete.paidCheque', 'حذف چک پرداختی'),

            ('submit.paidCheque', 'ثبت چک پرداختی'),
            ('changeStatus.paidCheque', 'تغییر وضعیت پرداختی'),

            ('getOwn.receivedCheque', 'مشاهده چک های دریافتی خود'),
            ('updateOwn.receivedCheque', 'ویرایش چک های دریافتی خود'),
            ('deleteOwn.receivedCheque', 'حذف چک های دریافتی خود'),

            ('changeStatusOwn.receivedCheque', 'تغییر وضعیت های دریافتی خود'),

            ('getOwn.paidCheque', 'مشاهده چک های پرداختی خود'),
            ('updateOwn.paidCheque', 'ویرایش چک های پرداختی خود'),
            ('deleteOwn.paidCheque', 'حذف چک های پرداختی خود'),

            ('changeStatusOwn.paidCheque', 'تغییر وضعیت های پرداختی خود'),

            ('firstConfirm.receivedCheque', 'تایید اول چک دریافتی'),
            ('secondConfirm.receivedCheque', 'تایید دوم چک دریافتی'),
            ('firstConfirmOwn.receivedCheque', 'تایید اول چک های دریافتی خود'),
            ('secondConfirmOwn.receivedCheque', 'تایید دوم چک های دریافتی خود'),

            ('firstConfirm.paidCheque', 'تایید اول چک پرداختی '),
            ('secondConfirm.paidCheque', 'تایید دوم چک پرداختی '),
            ('firstConfirmOwn.paidCheque', 'تایید اول چک های پرداختی خود'),
            ('secondConfirmOwn.paidCheque', 'تایید دوم چک های پرداختی خود'),
        )

    def save(self, *args, **kwargs):
        res = super(Cheque, self).save(*args, **kwargs)
        if self.has_transaction:
            from transactions.models import TransactionItem
            transaction_item = TransactionItem.objects.filter(cheque=self).first()
            if transaction_item:
                transaction_item.documentNumber = self.serial
                transaction_item.date = self.date
                transaction_item.due = self.due
                transaction_item.explanation = self.explanation
                transaction_item.value = self.value
                transaction_item.save()

        if self.status == 'blank' and self.lastAccount != self.account:
            self.lastAccount = self.account
            self.lastFloatAccount = self.floatAccount
            self.lastCostCenter = self.costCenter
            res = self.save()

        return res

    def changeStatus(self, user, date, to_status, account: Account = None, floatAccount: FloatAccount = None,
                     costCenter: FloatAccount = None, explanation='', sanad=None):
        data = {
            'cheque': self.id,
            'fromStatus': self.status,
            'toStatus': to_status,
            'financial_year': user.active_financial_year.id,
            'date': date,
            'explanation': explanation
        }

        if sanad:
            data['sanad'] = sanad.id

        lastFloatAccount = None
        lastCostCenter = None

        if self.received_or_paid == Cheque.RECEIVED:

            data['besAccount'] = self.lastAccount.id
            if self.lastFloatAccount:
                data['besFloatAccount'] = self.lastFloatAccount.id
            if self.lastCostCenter:
                data['besCostCenter'] = self.lastCostCenter.id

            if to_status == 'revoked' or to_status == 'bounced':
                lastAccount = self.account
                data['bedAccount'] = self.account.id
                if self.floatAccount:
                    lastFloatAccount = self.floatAccount
                    data['bedFloatAccount'] = self.floatAccount.id
                if self.costCenter:
                    lastCostCenter = self.costCenter
                    data['bedCostCenter'] = self.costCenter.id

            elif to_status == 'notPassed':
                defaultAccount = DefaultAccount.get('receivedCheque')
                lastAccount = defaultAccount.account
                lastFloatAccount = defaultAccount.floatAccount
                lastCostCenter = defaultAccount.costCenter
                data['bedAccount'] = lastAccount.id

            else:
                lastAccount = account
                data['bedAccount'] = account.id
                if floatAccount:
                    lastFloatAccount = floatAccount
                    data['bedFloatAccount'] = floatAccount.id
                if costCenter:
                    lastCostCenter = costCenter
                    data['bedCostCenter'] = costCenter.id

        else:

            data['bedAccount'] = self.lastAccount.id
            if self.lastFloatAccount:
                data['bedFloatAccount'] = self.lastFloatAccount.id
            if self.lastCostCenter:
                data['bedCostCenter'] = self.costCenter.id

            if to_status == 'revoked' or to_status == 'bounced':
                lastAccount = self.account
                data['besAccount'] = self.account.id
                if self.floatAccount:
                    lastFloatAccount = self.floatAccount
                    data['besFloatAccount'] = self.floatAccount.id
                if self.costCenter:
                    lastCostCenter = self.costCenter
                    data['besCostCenter'] = self.costCenter.id

            elif to_status == 'passed':
                lastAccount = self.chequebook.account
                data['besAccount'] = self.chequebook.account.id
                if self.chequebook.floatAccount:
                    lastFloatAccount = self.chequebook.floatAccount
                    data['besFloatAccount'] = self.chequebook.floatAccount.id
                if self.chequebook.costCenter:
                    lastCostCenter = self.chequebook.costCenter
                    data['besCostCenter'] = self.chequebook.costCenter.id

            elif to_status == 'notPassed':
                defaultAccount = DefaultAccount.get('paidCheque')
                lastAccount = defaultAccount.account
                lastFloatAccount = defaultAccount.floatAccount
                lastCostCenter = defaultAccount.costCenter

                data['besAccount'] = lastAccount.id
                if lastFloatAccount:
                    data['besFloatAccount'] = lastFloatAccount.id
                if lastCostCenter:
                    data['besCostCenter'] = lastCostCenter.id

            else:
                lastAccount = account
                data['besAccount'] = account.id
                if floatAccount:
                    lastFloatAccount = floatAccount
                    data['besFloatAccount'] = floatAccount.id
                if costCenter:
                    lastCostCenter = costCenter
                    data['besCostCenter'] = costCenter.id

        from cheques.serializers import StatusChangeSerializer
        serialized = StatusChangeSerializer(data=data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        self.lastAccount = lastAccount
        self.lastFloatAccount = lastFloatAccount
        self.lastCostCenter = lastCostCenter
        self.status = to_status
        self.save()

        return serialized.instance
