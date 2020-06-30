from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account
from companies.models import FinancialYear
from helpers.models import MELLI_CODE, PHONE, EXPLANATION, DECIMAL, BaseModel
from users.models import City
from wares.models import Ware


class Driver(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='drivers')
    name = models.CharField(max_length=150)
    shenasname_number = models.CharField(max_length=150, null=True, blank=True)
    melli_code = MELLI_CODE(null=True, blank=True)
    date_of_birth = jmodels.jDateTimeField(null=True, blank=True)
    father_name = models.CharField(max_length=150, null=True, blank=True)
    driving_licence_number = models.CharField(max_length=150, null=True, blank=True)
    phone = PHONE(null=True, blank=True)
    health_card_number = models.CharField(max_length=150, null=True, blank=True)
    landline_phone = models.CharField(max_length=150, null=True, blank=True)
    bank_card_number = models.CharField(max_length=150, null=True, blank=True)
    bank_account_number = models.CharField(max_length=150, null=True, blank=True)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    iban = models.CharField(max_length=150, null=True, blank=True)
    explanation = EXPLANATION()

    class Meta(BaseModel.Meta):
        backward_financial_year = True

        permissions = (
            ('get.driver', 'مشاهده راننده'),
            ('create.driver', 'تعریف راننده'),
            ('update.driver', 'ویرایش راننده'),
            ('delete.driver', 'حذف راننده'),
        )


class Car(BaseModel):
    COMPANY = 'c'
    OTHER = 'o'
    RAHMAN = 'rn'
    RAHIM = 'rm'
    EBRAHIM = 'e'

    OWNERS = (
        (COMPANY, 'شرکت'),
        (OTHER, 'دیگر'),
        (RAHMAN, 'رحمان'),
        (RAHIM, 'رحیم'),
        (EBRAHIM, 'ابراهیم')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='cars')

    car_number = ArrayField(base_field=models.CharField(max_length=3), size=4)
    type = models.CharField(max_length=100, null=True, blank=True)
    system = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.CharField(max_length=100, null=True, blank=True)
    fuel = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    engine = models.CharField(max_length=100, null=True, blank=True)
    chassis = models.CharField(max_length=100, null=True, blank=True)
    room = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    owner_name = models.CharField(max_length=150, null=True, blank=True)
    owner_melli_code = MELLI_CODE(null=True, blank=True)
    vin = models.CharField(max_length=150, null=True, blank=True)

    smart_card_number = models.CharField(max_length=150, null=True, blank=True)
    owner = models.CharField(max_length=2, choices=OWNERS)
    explanation = EXPLANATION()

    class Meta(BaseModel.Meta):
        backward_financial_year = True

        permissions = (
            ('get.car', 'مشاهده ماشین'),
            ('create.car', 'تعریف ماشین'),
            ('update.car', 'ویرایش ماشین'),
            ('delete.car', 'حذف ماشین'),
        )

    @property
    def car_number_str(self):
        return "{} {} {} ایران {}".format(*self.car_number)


class Driving(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='drivings')
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='drivings')
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='drivings')
    mobile_cost = DECIMAL()
    fixed_salary = DECIMAL()
    commission = DECIMAL()
    reward = DECIMAL()
    family = DECIMAL()
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='drivings')

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permissions = (
            ('get.driving', 'مشاهده انتصاب راننده به ماشین'),
            ('create.driving', 'تعریف انتصاب راننده به ماشین'),
            ('update.driving', 'ویرایش انتصاب راننده به ماشین'),
            ('delete.driving', 'حذف انتصاب راننده به ماشین'),
        )


class Association(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='associations')
    name = models.CharField(max_length=150)
    price = DECIMAL()
    explanation = EXPLANATION()

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permissions = (
            ('get.association', 'مشاهده کمیسیون انجمن'),
            ('create.association', 'تعریف کمیسیون انجمن'),
            ('update.association', 'ویرایش کمیسیون انجمن'),
            ('delete.association', 'حذف کمیسیون انجمن'),
        )


class RemittanceMixin(BaseModel):
    COMPANY = 'cmp'
    CONTRACTOR = 'cnt'
    TIP_PAYERS = (
        (COMPANY, 'شرکت'),
        (CONTRACTOR, 'پیمانکار')
    )

    TO_COMPANY = 'tc'
    TO_COMPANY_AND_DRIVER = 'tcd'
    COMPANY_PAYS = 'cp'

    REMITTANCE_PAYMENT_METHODS = (
        (TO_COMPANY, "کمیسیون و کرایه به شرکت"),
        (TO_COMPANY_AND_DRIVER, "کمیسیون به شرکت و کرایه به راننده"),
        (COMPANY_PAYS, "کمیسیون و کرایه با شرکت")
    )

    ware = models.ForeignKey(Ware, on_delete=models.PROTECT)
    contractor_price = DECIMAL()
    contractor = models.ForeignKey(Account, on_delete=models.PROTECT)
    tip_price = DECIMAL()
    tip_payer = models.CharField(max_length=3, choices=TIP_PAYERS)
    lading_bill_difference = DECIMAL()
    remittance_payment_method = models.CharField(max_length=3, choices=REMITTANCE_PAYMENT_METHODS)
    fare_price = DECIMAL()

    class Meta:
        abstract = True


class Remittance(RemittanceMixin):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='remittances')
    code = models.IntegerField(unique=True)
    issue_date = jmodels.jDateField()
    loading_date = jmodels.jDateField()
    end_date = jmodels.jDateField()
    amount = DECIMAL()
    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    explanation = EXPLANATION()

    origin = models.ForeignKey(City, on_delete=models.PROTECT, related_name='remittanceOrigins')
    destination = models.ForeignKey(City, on_delete=models.PROTECT, related_name='remittanceDestinations')

    class Meta(BaseModel.Meta):
        ordering = ['-code', ]
        permissions = (
            ('get.remittance', 'مشاهده حواله'),
            ('create.remittance', 'تعریف حواله'),
            ('update.remittance', 'ویرایش حواله'),
            ('delete.remittance', 'حذف حواله'),
        )


def upload_attachment_to(instance, filename):
    import random
    return 'modules/dashtbashi/{}-{}'.format(filename, str(random.getrandbits(128)))


class LadingBillSeries(BaseModel):
    serial = models.CharField(max_length=100)

    from_bill_number = models.IntegerField()
    to_bill_number = models.IntegerField()

    class Meta(BaseModel.Meta):
        permissions = (
            ('get.ladingBillSeries', 'مشاهده سری بارنامه'),
            ('create.ladingBillSeries', 'تعریف سری بارنامه'),
            ('update.ladingBillSeries', 'ویرایش سری بارنامه'),
            ('delete.ladingBillSeries', 'حذف سری بارنامه'),
        )


class LadingBillNumber(BaseModel):
    series = models.ForeignKey(LadingBillSeries, on_delete=models.CASCADE, related_name='numbers')
    number = models.IntegerField()
    is_revoked = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        permissions = (
            ('revoke.ladingBillNumber', 'ابطال شماره بارنامه'),
        )


class Lading(RemittanceMixin):
    COMPANY = 'cmp'
    CONTRACTOR = 'cnt'
    TIP_PAYERS = (
        (COMPANY, 'شرکت'),
        (CONTRACTOR, 'پیمانکار')
    )

    CREDIT = 'cr'
    CASH = 'cs'
    POS = 'p'
    RECEIVE_TYPES = (
        (CREDIT, 'نسیه'),
        (CASH, 'نقدی'),
        (POS, 'کارت خوان')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='ladings')
    remittance = models.ForeignKey(Remittance, on_delete=models.PROTECT, related_name='ladings', null=True, blank=True)
    driving = models.ForeignKey(Driving, on_delete=models.PROTECT, related_name='ladings')

    lading_number = models.IntegerField()
    lading_date = jmodels.jDateField()
    original_amount = DECIMAL()
    destination_amount = DECIMAL()

    lading_explanation = EXPLANATION()
    lading_attachment = models.FileField(null=True, blank=True, upload_to=upload_attachment_to)

    billNumber = models.ForeignKey(LadingBillNumber, on_delete=models.PROTECT, related_name='ladings')
    bill_date = jmodels.jDateField()
    bill_price = DECIMAL()

    bill_explanation = EXPLANATION()
    bill_attachment = models.FileField(null=True, blank=True, upload_to=upload_attachment_to)

    association = models.ForeignKey(Association, on_delete=models.PROTECT, related_name='ladings', null=True,
                                    blank=True)
    association_price = DECIMAL()

    receive_type = models.CharField(max_length=2, choices=RECEIVE_TYPES, null=True, blank=True)

    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    origin = models.ForeignKey(City, on_delete=models.PROTECT, related_name='ladingOrigins', null=True, blank=True)
    destination = models.ForeignKey(City, on_delete=models.PROTECT, related_name='ladingDestinations', null=True,
                                    blank=True)

    class Meta(BaseModel.Meta):
        permissions = (
            ('get.lading', 'مشاهده بارگیری'),
            ('create.lading', 'تعریف بارگیری'),
            ('update.lading', 'ویرایش بارگیری'),
            ('delete.lading', 'حذف بارگیری'),
        )
