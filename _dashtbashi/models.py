from typing import Optional, Union, Sequence

from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account, FloatAccount, FloatAccountRelation
from companies.models import FinancialYear
from helpers.models import MELLI_CODE, PHONE, EXPLANATION, DECIMAL, BaseModel, DATE
from transactions.models import Transaction
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

    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='driver', null=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'driver'
        permissions = (
            ('get.driver', 'مشاهده راننده'),
            ('create.driver', 'تعریف راننده'),
            ('update.driver', 'ویرایش راننده'),
            ('delete.driver', 'حذف راننده'),

            ('getOwn.driver', 'مشاهده راننده های خود'),
            ('updateOwn.driver', 'ویرایش راننده های خود'),
            ('deleteOwn.driver', 'حذف راننده های خود'),
        )


class Car(BaseModel):
    PARTNERSHIP = 'p'
    OTHER = 'o'
    RAHMAN = 'rn'
    RAHIM = 'rm'
    EBRAHIM = 'e'

    OWNERS = (
        (PARTNERSHIP, 'شراکتی'),
        (OTHER, 'دیگر'),
        (RAHMAN, 'حاج رحمان'),
        (RAHIM, 'حاج رحیم'),
        (EBRAHIM, 'حاج ابراهیم')
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

    # just for Rahman
    expenseAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='carExpense', null=True)

    # just for Rahman
    incomeAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='carIncome', null=True)

    payableAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='carPayable', null=True)
    receivableAccount = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='carReceivable', null=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'car'
        permissions = (
            ('get.car', 'مشاهده ماشین'),
            ('create.car', 'تعریف ماشین'),
            ('update.car', 'ویرایش ماشین'),
            ('delete.car', 'حذف ماشین'),

            ('getOwn.car', 'مشاهده ماشین های خود'),
            ('updateOwn.car', 'ویرایش ماشین های خود'),
            ('deleteOwn.car', 'حذف ماشین های خود'),
        )

    @property
    def car_number_str(self):
        return "{} {} {} ایران {}".format(*self.car_number)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        # Create Accounts Here
        # parent = Account()
        # Account.objects.create(
        #     name="{}".format(self.car_number_str),
        #     parent=parent,
        #     code=parent.get_new_child_code(),
        #     level=Account.TAFSILI
        # )


class Driving(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='drivings')
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='drivings')
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='drivings')
    mobile_cost = DECIMAL()
    fixed_salary = DECIMAL()
    commission = DECIMAL()
    reward = DECIMAL()
    family = DECIMAL()

    floatAccountRelation = models.ForeignKey(FloatAccountRelation, on_delete=models.PROTECT, related_name='driving',
                                             null=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'driving'
        permissions = (
            ('get.driving', 'مشاهده انتصاب راننده به ماشین'),
            ('create.driving', 'تعریف انتصاب راننده به ماشین'),
            ('update.driving', 'ویرایش انتصاب راننده به ماشین'),
            ('delete.driving', 'حذف انتصاب راننده به ماشین'),

            ('getOwn.driving', 'مشاهده انتصاب راننده به ماشین خود'),
            ('updateOwn.driving', 'ویرایش انتصاب راننده به ماشین خود'),
            ('deleteOwn.driving', 'حذف انتصاب راننده به ماشین خود'),
        )


class Association(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='associations')
    name = models.CharField(max_length=150)
    price = DECIMAL()
    explanation = EXPLANATION()

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'association'
        permissions = (
            ('get.association', 'مشاهده کمیسیون انجمن'),
            ('create.association', 'تعریف کمیسیون انجمن'),
            ('update.association', 'ویرایش کمیسیون انجمن'),
            ('delete.association', 'حذف کمیسیون انجمن'),

            ('getOwn.association', 'مشاهده کمیسیون انجمن های خود'),
            ('updateOwn.association', 'ویرایش کمیسیون انجمن های خود'),
            ('deleteOwn.association', 'حذف کمیسیون انجمن های خود'),
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
    driver_tip_price = DECIMAL()
    driver_tip_payer = models.CharField(max_length=3, choices=TIP_PAYERS)
    lading_bill_difference = DECIMAL()
    remittance_payment_method = models.CharField(max_length=3, choices=REMITTANCE_PAYMENT_METHODS)
    fare_price = DECIMAL()

    class Meta(BaseModel.Meta):
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
        permission_basename = 'remittance'
        permissions = (
            ('get.remittance', 'مشاهده حواله'),
            ('create.remittance', 'تعریف حواله'),
            ('update.remittance', 'ویرایش حواله'),
            ('delete.remittance', 'حذف حواله'),

            ('getOwn.remittance', 'مشاهده حواله های خود'),
            ('updateOwn.remittance', 'ویرایش حواله های خود'),
            ('deleteOwn.remittance', 'حذف حواله های خود'),
        )


def upload_attachment_to(instance, filename):
    import random
    return 'modules/dashtbashi/{}-{}'.format(filename, str(random.getrandbits(128)))


class LadingBillSeries(BaseModel):
    serial = models.CharField(max_length=100)

    from_bill_number = models.IntegerField()
    to_bill_number = models.IntegerField()

    class Meta(BaseModel.Meta):
        permission_basename = 'ladingBillSeries'
        permissions = (
            ('get.ladingBillSeries', 'مشاهده سری بارنامه'),
            ('create.ladingBillSeries', 'تعریف سری بارنامه'),
            ('update.ladingBillSeries', 'ویرایش سری بارنامه'),
            ('delete.ladingBillSeries', 'حذف سری بارنامه'),

            ('getOwn.ladingBillSeries', 'مشاهده سری بارنامه های خود'),
            ('updateOwn.ladingBillSeries', 'ویرایش سری بارنامه های خود'),
            ('deleteOwn.ladingBillSeries', 'حذف سری بارنامه های خود'),
        )


class LadingBillNumber(BaseModel):
    series = models.ForeignKey(LadingBillSeries, on_delete=models.CASCADE, related_name='numbers')
    number = models.IntegerField()
    is_revoked = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        permission_basename = 'ladingBillNumber'
        permissions = (
            ('revoke.ladingBillNumber', 'ابطال شماره بارنامه'),
            ('revokeOwn.ladingBillNumber', 'ابطال شماره بارنامه خود'),
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
    cargo_tip_price = DECIMAL()

    association = models.ForeignKey(Association, on_delete=models.PROTECT, related_name='ladings', null=True,
                                    blank=True)
    association_price = DECIMAL()

    receive_type = models.CharField(max_length=2, choices=RECEIVE_TYPES, null=True, blank=True)

    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    origin = models.ForeignKey(City, on_delete=models.PROTECT, related_name='ladingOrigins', null=True, blank=True)
    destination = models.ForeignKey(City, on_delete=models.PROTECT, related_name='ladingDestinations', null=True,
                                    blank=True)
    is_paid = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        permission_basename = 'lading'
        permissions = (
            ('get.lading', 'مشاهده بارگیری'),
            ('create.lading', 'تعریف بارگیری'),
            ('update.lading', 'ویرایش بارگیری'),
            ('delete.lading', 'حذف بارگیری'),
        )


class OilCompanyLading(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='oilCompanyLadings')
    explanation = EXPLANATION()
    date = jmodels.jDateField()
    export_date = jmodels.jDateField()

    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='oilCompanyLadings')

    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        permission_basename = 'oilCompanyLading'
        permissions = (
            ('get.oilCompanyLading', 'مشاهده بارگیری شرکت نفت'),
            ('create.oilCompanyLading', 'تعریف بارگیری شرکت نفت'),
            ('update.oilCompanyLading', 'ویرایش بارگیری شرکت نفت'),
            ('delete.oilCompanyLading', 'حذف بارگیری شرکت نفت'),
        )


class OilCompanyLadingItem(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    oilCompanyLading = models.ForeignKey(OilCompanyLading, on_delete=models.CASCADE, related_name='items')

    gross_price = DECIMAL()
    insurance_price = DECIMAL()
    tax_value = DECIMAL(null=True, blank=True)
    tax_percent = models.IntegerField(default=0, null=True, blank=True)
    complication_value = DECIMAL(null=True, blank=True)
    complication_percent = models.IntegerField(default=0, null=True, blank=True)

    company_commission = DECIMAL()
    car_income = DECIMAL()

    class Meta(BaseModel.Meta):
        pass


class OtherDriverPayment(BaseModel):
    code = models.IntegerField()
    date = DATE()
    explanation = EXPLANATION()
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    driving = models.ForeignKey(Driving, on_delete=models.PROTECT, related_name='otherDriverPayments')
    ladings = models.ManyToManyField(Lading, related_name='otherDriverPayment')
    imprests = models.ManyToManyField(Transaction, related_name='otherDriverPaymentsAsImprest')
    payment = models.ForeignKey(Transaction, related_name='otherDriverPayment', on_delete=models.PROTECT)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'otherDriverPayment'
        permissions = (
            ('get.otherDriverPayment', 'مشاهده پرداخت رانندگان متفرقه '),
            ('create.otherDriverPayment', 'تعریف پرداخت رانندگان متفرقه'),
            ('update.otherDriverPayment', 'ویرایش پرداخت رانندگان متفرقه'),
            ('delete.otherDriverPayment', 'حذف پرداخت رانندگان متفرقه'),

            ('getOwn.otherDriverPayment', 'مشاهده پرداخت رانندگان متفرقه خود'),
            ('updateOwn.otherDriverPayment', 'ویرایش پرداخت رانندگان متفرقه خود'),
            ('deleteOwn.otherDriverPayment', 'حذف پرداخت رانندگان متفرقه خود'),
        )
