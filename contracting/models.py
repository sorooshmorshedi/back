from django.db import models
from django.db.models import Q
from django_jalali.db import models as jmodels

from transactions.models import Transaction
from helpers.models import BaseModel, POSTAL_CODE, EXPLANATION, DECIMAL, LockableMixin, DefinableMixin
from accounts.accounts.models import Account
from users.models import City


class Tender(BaseModel, LockableMixin, DefinableMixin):
    WARE = 'w'
    SERVICES_WITH_PRICE_LIST = 'spl'
    SERVICES_WITHOUT_PRICE_LIST = 'npl'
    CONSULTING = 'c'
    OTHER = 'o'

    TYPES = (
        (WARE, 'کالا'),
        (SERVICES_WITH_PRICE_LIST, 'خدمات با فهرست بها'),
        (SERVICES_WITHOUT_PRICE_LIST, 'خدمات بدون فهرست بها'),
        (CONSULTING, 'مشاوره'),
        (OTHER, 'سایر')
    )

    code = models.IntegerField()
    title = models.CharField(max_length=255)
    explanation = EXPLANATION()
    province = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    classification = models.CharField(max_length=3, choices=TYPES, default=OTHER)

    bidder = models.CharField(max_length=100)
    bidder_address = models.CharField(max_length=255, blank=True, null=True)
    bidder_postal_code = POSTAL_CODE(blank=True, null=True)

    received_deadline = jmodels.jDateField(blank=True, null=True)
    send_offer_deadline = jmodels.jDateField(blank=True, null=True)
    opening_date = jmodels.jDateField(blank=True, null=True)
    offer_expiration = jmodels.jDateField(blank=True, null=True)

    transaction = models.ManyToManyField(Transaction, related_name='tender', blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.title, self.code)

    class Meta(BaseModel.Meta):
        ordering = ['-pk', ]
        verbose_name = 'Tender'
        permission_basename = 'tender'
        permissions = (
            ('get.tender', 'مشاهده مناقصه'),
            ('create.tender', 'تعریف مناقصه'),
            ('update.tender', 'ویرایش مناقصه'),
            ('delete.tender', 'حذف مناقصه'),

            ('getOwn.tender', 'مشاهده مناقصه خود'),
            ('updateOwn.tender', 'ویرایش مناقصه خود'),
            ('deleteOwn.tender', 'حذف مناقصه خود'),
        )


class Contract(BaseModel, LockableMixin, DefinableMixin):
    tender = models.ForeignKey(Tender, on_delete=models.SET_NULL, related_name='contract', blank=True, null=True)
    title = models.CharField(max_length=50)
    contractor = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='contract', blank=True, null=True)
    code = models.IntegerField()
    amount = DECIMAL()
    from_date = jmodels.jDateField(blank=True, null=True)
    to_date = jmodels.jDateField(blank=True, null=True)
    max_change_amount = models.IntegerField(blank=True, null=True)
    registration = jmodels.jDateField(blank=True, null=True)
    inception = jmodels.jDateField(blank=True, null=True)
    # legal deductions
    doing_job_well = models.IntegerField(blank=True, null=True)
    insurance_payment = models.IntegerField(blank=True, null=True)
    other = models.IntegerField(blank=True, null=True)

    received_transaction = models.ManyToManyField(Transaction, related_name='contract_received', blank=True, null=True)
    guarantee_document_transaction = models.ManyToManyField(Transaction, related_name='contract_guarantee',
                                                            blank=True, null=True)

    def __str__(self):
        return "contract {} by {}".format(self.title, self.contractor)

    class Meta(BaseModel.Meta):
        ordering = ['-pk', ]
        verbose_name = 'Contract'
        permissions = (
            ('get.contract', 'مشاهده قرارداد'),
            ('create.contract', 'تعریف قرارداد'),
            ('update.contract', 'ویرایش قرارداد'),
            ('delete.contract', 'حذف قرارداد'),

            ('getOwn.contract', 'مشاهده قرارداد های خود'),
            ('updateOwn.contract', 'ویرایش قرارداد های خود'),
            ('deleteOwn.contract', 'حذف قرارداد های خود'),
        )


class Statement(BaseModel, LockableMixin, DefinableMixin):
    NORMAL = 'n'
    ADJUSTMENT = 'a'
    TEMPORARY_DELIVERY = 'td'
    DEFINITE_DELIVERY = 'dd'

    TYPES = (
        (NORMAL, 'معمولی'),
        (ADJUSTMENT, 'تعدیل'),
        (TEMPORARY_DELIVERY, 'تحویل موقت'),
        (DEFINITE_DELIVERY, 'تحویل قطعی'),
    )

    code = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=3, choices=TYPES, default=NORMAL)

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='statement', blank=True, null=True)

    value = DECIMAL()
    previous_statement_value = DECIMAL(blank=True, null=True)
    serial = models.IntegerField()
    date = jmodels.jDateField(blank=True, null=True)
    explanation = EXPLANATION()
    present_statement_value = DECIMAL(blank=True, null=True)

    def __str__(self):
        return "contract {} by {}".format(self.contract, self.code)

    class Meta(BaseModel.Meta):
        ordering = ['-pk', ]
        verbose_name = 'Statement'
        permission_basename = 'statement'
        permissions = (
            ('get.statement', 'مشاهده صورت وضعیت'),
            ('create.statement', 'تعریف صورت وضعیت'),
            ('update.statement', 'ویرایش صورت وضعیت'),
            ('delete.statement', 'حذف صورت وضعیت'),

            ('getOwn.statement', 'مشاهده صورت وضعیت های خود'),
            ('updateOwn.statement', 'ویرایش صورت وضعیت های خود'),
            ('deleteOwn.statement', 'حذف صورت وضعیت های خود'),
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self.code = self.system_code
            self.previous_statement_value = self.get_previous_value
            self.present_statement_value = self.get_present_value
        else:
            self.previous_statement_value = self.update_previous_value
            self.present_statement_value = self.update_present_value

        super().save(*args, **kwargs)

    @property
    def system_code(self):
        try:
            contract_statement = Statement.objects.filter(contract=self.contract).first()
            statement_code = contract_statement.code
            code = statement_code + 1
        except:
            code = 1
        return code

    @property
    def get_previous_value(self):
        previous_value = 0
        contract_statements = Statement.objects.filter(contract=self.contract)
        for statement in contract_statements:
            previous_value += statement.value
        return previous_value

    @property
    def update_previous_value(self):
        previous_value = 0
        contract_statements = Statement.objects.filter(Q(contract=self.contract) & Q(code__lt=self.code))
        for statement in contract_statements:
            previous_value += statement.value
        return previous_value

    @property
    def get_present_value(self):
        present_value = self.value + self.get_previous_value
        return present_value

    @property
    def update_present_value(self):
        present_value = self.value + self.update_previous_value
        return present_value


class Supplement(BaseModel, LockableMixin, DefinableMixin):
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, related_name='supplements', blank=True, null=True)
    new_contract_date = jmodels.jDateField(blank=True, null=True)
    explanation = EXPLANATION()
    increase = models.BooleanField(default=True)
    value = DECIMAL()
    date = jmodels.jDateField(blank=True, null=True)
    code = models.IntegerField()

    def __str__(self):
        return "supplement {} code {}".format(self.contract, self.code)

    class Meta(BaseModel.Meta):
        ordering = ['-pk', ]
        verbose_name = 'Supplement'
        permission_basename = 'supplement'
        permissions = (
            ('get.supplement', 'مشاهده الحاقیه'),
            ('create.supplement', 'تعریف الحاقیه'),
            ('update.supplement', 'ویرایش الحاقیه'),
            ('delete.supplement', 'حذف الحاقیه'),

            ('getOwn.supplement', 'مشاهده الحاقیه های خود'),
            ('updateOwn.supplement', 'ویرایش الحاقیه های خود'),
            ('deleteOwn.supplement', 'حذف الحاقیه های خود'),
        )
