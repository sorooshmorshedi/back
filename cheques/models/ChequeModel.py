from django.db import models
from django.db.models import Q
from django_jalali.db import models as jmodels
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from accounts.accounts.models import Account, FloatAccount, AccountGroup
from accounts.defaultAccounts.models import DefaultAccount
from cheques.models.ChequebookModel import Chequebook
from companies.models import FinancialYear
from helpers.functions import get_current_user
from helpers.models import BaseModel, BaseManager
from sanads.models import Sanad

CHEQUE = 'c'
GUARANTEE_CHEQUE = 'gc'
PROMISSORY_NOTE = 'pn'
BANK_GUARANTEE = 'bg'

BLANK = 'blank'
NOT_PASSED = 'notPassed'
GUARANTEE = 'guarantee'
IN_FLOW = 'inFlow'
PASSED = 'passed'
BOUNCED = 'bounced'
CASHED = 'cashed'
REVOKED = 'revoked'
TRANSFERRED = 'transferred'
EXTENDED = 'extended'

CHEQUE_STATUSES = (
    (BLANK, 'سفید'),
    (NOT_PASSED, 'پاس نشده'),
    (GUARANTEE, 'ضمانتی'),
    (IN_FLOW, 'در جریان'),
    (PASSED, 'پاس شده'),
    (BOUNCED, 'برگشتی'),
    (CASHED, 'نقد شده'),
    (REVOKED, 'باطل شده'),
    (TRANSFERRED, 'انتقالی'),
    (EXTENDED, 'تمدید شده'),
)

STATUS_TREE = {
    'r': {
        BLANK: [NOT_PASSED, GUARANTEE],  # initial state
        NOT_PASSED: [IN_FLOW, PASSED, BOUNCED, CASHED, REVOKED, TRANSFERRED],
        GUARANTEE: [REVOKED, NOT_PASSED, EXTENDED],
        IN_FLOW: [PASSED],
        BOUNCED: [IN_FLOW, PASSED, CASHED, REVOKED, TRANSFERRED],
        EXTENDED: [NOT_PASSED, EXTENDED]
    },
    'p': {
        BLANK: [GUARANTEE, NOT_PASSED],  # initial state
        GUARANTEE: [REVOKED, NOT_PASSED, EXTENDED],
        NOT_PASSED: [PASSED, BOUNCED, CASHED, REVOKED],
        IN_FLOW: [PASSED],
        BOUNCED: [IN_FLOW, PASSED, CASHED, REVOKED, TRANSFERRED],
        EXTENDED: [NOT_PASSED, EXTENDED]
    }
}


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


class Cheque(BaseModel):
    TYPES = (
        (CHEQUE, 'چک'),
        (GUARANTEE_CHEQUE, 'چک ضمانتی'),
        (PROMISSORY_NOTE, 'سفته'),
        (BANK_GUARANTEE, 'ضمانت نامه بانکی'),
    )

    GUARANTEE_TYPES = (GUARANTEE_CHEQUE, PROMISSORY_NOTE, BANK_GUARANTEE)

    PERSONAL = 'p'
    COMPANY = 'c'
    OTHER_PERSON = 'op'
    OTHER_COMPANY = 'oc'
    CHEQUE_OWNER_TYPES = (
        (PERSONAL, 'شخصی'),
        (OTHER_PERSON, 'شخصی سایرین'),
        (COMPANY, 'شرکت'),
        (OTHER_COMPANY, 'شرکت سایرین')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='cheques')

    type = models.CharField(max_length=2, choices=TYPES, default=CHEQUE)
    is_paid = models.BooleanField(default=False)

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
    owner_type = models.CharField(max_length=2, choices=CHEQUE_OWNER_TYPES, blank=True, null=True)

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
        received_or_paid = 'p' if self.is_paid else 'r'
        if self.chequebook:
            return "{} - {} - {}".format(received_or_paid, self.chequebook.explanation[0:50], self.serial)
        else:
            return "{} - {} - {}".format(received_or_paid, self.explanation[0:50], self.serial)

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
        )

    def save(self, *args, **kwargs):
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

        if self.status == BLANK and self.lastAccount != self.account:
            self.lastAccount = self.account
            self.lastFloatAccount = self.floatAccount
            self.lastCostCenter = self.costCenter

        super().save(*args, **kwargs)

    def change_status(self, date, to_status, account_group: AccountGroup = None, explanation='', sanad=None):
        from cheques.status_change_sanad import StatusChangeSanad

        user = get_current_user()
        data = {
            'cheque': self.id,
            'fromStatus': self.status,
            'toStatus': to_status,
            'financial_year': user.active_financial_year.id,
            'date': date,
            'explanation': explanation,
            'sanad': sanad.id if sanad else None
        }

        def set_account(side, source):
            data[f'{side}Account'] = self.lastAccount_id = source.account_id
            data[f'{side}FloatAccount'] = self.lastFloatAccount_id = source.floatAccount_id or None
            data[f'{side}CostCenter'] = self.lastCostCenter_id = source.costCenter_id or None

        if not self.is_paid:

            if self.type in self.GUARANTEE_TYPES:
                set_account('bed', DefaultAccount.get('receivedGuarantee'))
                set_account('bes', DefaultAccount.get('receivedGuaranteeFrom'))
            else:
                set_account('bes', AccountGroup(self.lastAccount, self.lastFloatAccount, self.lastCostCenter))

                if to_status == 'revoked' or to_status == 'bounced':
                    set_account('bed', self)

                elif to_status == 'notPassed':
                    set_account('bed', DefaultAccount.get('receivedCheque'))

                else:
                    set_account('bed', account_group)

        else:
            if self.type in self.GUARANTEE_TYPES:
                set_account('bed', DefaultAccount.get('paidGuarantee'))
                set_account('bes', DefaultAccount.get('paidGuaranteeTo'))
            else:
                if self.status == 'blank' and to_status == 'revoked':
                    set_account('', self)
                else:
                    set_account('bed', AccountGroup(self.lastAccount, self.lastFloatAccount, self.lastCostCenter))

                    if to_status == 'revoked' or to_status == 'bounced':
                        set_account('bes', self)

                    elif to_status == 'passed':
                        set_account('bes', self.chequebook)

                    elif to_status == 'notPassed':
                        set_account('bes', DefaultAccount.get('paidCheque'))

                    else:
                        set_account('bes', account_group)

        from cheques.serializers import StatusChangeCreateUpdateSerializer
        serializer = StatusChangeCreateUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if not self.has_transaction:
            instance = serializer.instance
            StatusChangeSanad(instance).update()
            instance.sanad.define()

        self.status = to_status
        self.save()

        return serializer.instance

    @staticmethod
    def submit_cheque(user, data, is_guarantee=False):
        from cheques.serializers import ChequeCreateUpdateSerializer

        is_paid = data.get('is_paid', False) == 'true'

        if is_paid:
            instance = get_object_or_404(Cheque, pk=data.get('id'))
            serializer = ChequeCreateUpdateSerializer(instance=instance, data=data)
        else:
            serializer = ChequeCreateUpdateSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            status='blank',
        )

        cheque: Cheque = serializer.instance

        sanad = Sanad.objects.inFinancialYear().filter(code=data.pop('sanad_code', None)).first()

        if sanad and not sanad.isEmpty:
            raise ValidationError("سند باید خالی باشد")

        if is_guarantee:
            to_status = GUARANTEE
        else:
            to_status = NOT_PASSED

        cheque.change_status(
            date=cheque.date,
            to_status=to_status,
            explanation=cheque.explanation,
            sanad=sanad
        )

        return cheque
