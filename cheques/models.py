from django.db import models
from django_jalali.db import models as jmodels
from accounts.accounts.models import Account, FloatAccount
from companies.models import FinancialYear
from helpers.models import BaseModel
from sanads.sanads.models import Sanad, newSanadCode

CHECK_STATUSES = (
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


class Chequebook(BaseModel):

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='chequebooks')

    code = models.IntegerField(unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='chequebook')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='chequebook', blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    serial_from = models.IntegerField()
    serial_to = models.IntegerField()

    permissions = (
        ('get_cheque', 'Can get cheques')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.explanation[0:30])

    class Meta(BaseModel.Meta):
        verbose_name = 'دفتر چک'
        ordering = ['code', ]


class Cheque(BaseModel):

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='cheques')

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
    serial = models.CharField(max_length=255)
    chequebook = models.ForeignKey(Chequebook, on_delete=models.CASCADE, related_name='cheques', blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='receivedCheques', blank=True, null=True)
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='receivedCheques', blank=True, null=True)

    value = models.DecimalField(max_digits=24, decimal_places=0, blank=True, null=True)
    due = jmodels.jDateField(blank=True, null=True)
    date = jmodels.jDateField(blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, choices=CHECK_STATUSES)
    received_or_paid = models.CharField(max_length=10, choices=((RECEIVED, 'دریافتنی'), (PAID, 'پرداختنی')))
    type = models.CharField(max_length=1, choices=CHEQUE_TYPES, blank=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    lastAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='lastCheques', blank=True, null=True)
    lastFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='lastCheques', blank=True, null=True)

    bankName = models.CharField(max_length=100, null=True, blank=True)
    branchName = models.CharField(max_length=100, null=True, blank=True)
    accountNumber = models.CharField(max_length=50, null=True, blank=True)

    has_transaction = models.BooleanField(default=False)

    permissions = (
        ('get_cheque', 'Can get cheques')
    )

    def __str__(self):
        if self.chequebook:
            return "{} - {} - {}".format(self.received_or_paid, self.chequebook.explanation[0:50], self.serial)
        else:
            return "{} - {} - {}".format(self.received_or_paid, self.explanation[0:50], self.serial)

    class Meta(BaseModel.Meta):
        verbose_name = 'چک'
        ordering = ['serial', ]


class StatusChange(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='status_changes')

    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='statusChanges')
    sanad = models.OneToOneField(Sanad, on_delete=models.CASCADE, related_name='statusChange', blank=True, null=True)

    bedAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='chequeStatusChangesAsBedAccount')
    bedFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='chequeStatusChangesAsBesAccount', blank=True, null=True)
    besAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='chequeStatusChangesAsBedFloatAccount')
    besFloatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='chequeStatusChangesAsBesFloatAccount', blank=True, null=True)

    date = jmodels.jDateField()
    explanation = models.CharField(max_length=255, blank=True)
    transferNumber = models.IntegerField(null=True)

    fromStatus = models.CharField(max_length=30, choices=CHECK_STATUSES)
    toStatus = models.CharField(max_length=30, choices=CHECK_STATUSES)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    permissions = (
        ('get_cheque', 'Can get cheques')
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'تغییر وضعیت'
        ordering = ['id', ]

    def createSanad(self, user):
        if not self.sanad:
            cheque = self.cheque
            fromStatus = self.fromStatus
            if not cheque.has_transaction or not fromStatus == 'blank':
                sanad = Sanad(code=newSanadCode(user), date=self.date,
                              createType=Sanad.AUTO, financial_year=user.active_financial_year)
                sanad.save()
                self.sanad = sanad
                self.save()

