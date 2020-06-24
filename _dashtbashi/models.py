from django.db import models
from django_jalali.db import models as jmodels

from accounts.models import Account, FinancialYear
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
    explanation = EXPLANATION

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
    car_number = models.CharField(max_length=150)
    smart_card_number = models.CharField(max_length=150, null=True, blank=True)
    owner = models.CharField(max_length=2, choices=OWNERS)
    explanation = EXPLANATION

    class Meta(BaseModel.Meta):
        backward_financial_year = True

        permissions = (
            ('get.car', 'مشاهده ماشین'),
            ('create.car', 'تعریف ماشین'),
            ('update.car', 'ویرایش ماشین'),
            ('delete.car', 'حذف ماشین'),
        )


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

#
# class Remittance(BaseModel):
#     COMPANY = 'cmp'
#     CONTRACTOR = 'cnt'
#     TIP_PAYERS = (
#         (COMPANY, 'شرکت'),
#         (CONTRACTOR, 'پیمانکار')
#     )
#
#     TO_COMPANY = 'tc'
#     TO_COMPANY_AND_DRIVER = 'tcd'
#     COMPANY_PAYS = 'cp'
#
#     REMITTANCE_PAYMENT_METHODS = (
#         (TO_COMPANY, "کمیسیون و کرایه به شرکت"),
#         (TO_COMPANY_AND_DRIVER, "کمیسیون به شرکت و کرایه به راننده"),
#         (COMPANY_PAYS, "کمیسیون و کرایه با شرکت")
#     )
#
#     code = models.IntegerField()
#     issue_date = jmodels.jDateField()
#     loading_date = jmodels.jDateField()
#     end_date = jmodels.jDateField()
#     amount = DECIMAL()
#     ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='remittances')
#     created_at = jmodels.jDateTimeField(auto_now=True)
#     updated_at = jmodels.jDateTimeField(auto_now_add=True)
#     contractor_price = DECIMAL()
#     rental_price = DECIMAL()
#
#     origin = models.ForeignKey(City, on_delete=models.PROTECT)
#     destination = models.ForeignKey(City, on_delete=models.PROTECT)
#
#     contractor = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='drivings')
#     explanation = EXPLANATION
#     tip_price = DECIMAL()
#     tip_payer = models.CharField(max_length=3, choices=TIP_PAYERS)
#     lading_bill_difference = DECIMAL()
#     remittance_payment_method = models.CharField(max_length=3, choices=REMITTANCE_PAYMENT_METHODS)
#
#     class Meta(BaseModel.Meta):
#         ordering = ['-code', ]
#
#
# def upload_attachment_to(instance, filename):
#     import random
#     return 'attachments/{}-{}'.format(filename, str(random.getrandbits(128)))
#
#
# class Lading(BaseModel):
#     COMPANY = 'cmp'
#     CONTRACTOR = 'cnt'
#     TIP_PAYERS = (
#         (COMPANY, 'شرکت'),
#         (CONTRACTOR, 'پیمانکار')
#     )
#
#     remittance = models.ForeignKey(Remittance, on_delete=models.PROTECT, related_name='ladings')
#     number = models.IntegerField()
#     date = jmodels.jDateField()
#     original_amount = DECIMAL()
#     destination_amount = DECIMAL()
#     contractor = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='ladings')
#     driving = models.ForeignKey(Driving, on_delete=models.PROTECT, related_name='ladings')
#
#     explanation = EXPLANATION
#     lading_attachment = models.FileField(null=True, blank=True, upload_to=upload_attachment_to)
#
#     # bill_number = models.IntegerField()
#     # bill_date = jmodels.jDateField()
#     # terminal_price = DECIMAL()
#     # insurance_price = DECIMAL()
#     # rental_price = DECIMAL()
#     #
#     # bill_explanation = EXPLANATION
#     # bill_attachment = models.FileField(null=True, blank=True, upload_to=upload_attachment_to)
#
#     created_at = jmodels.jDateTimeField(auto_now=True)
#     updated_at = jmodels.jDateTimeField(auto_now_add=True)
#
#     class Meta(BaseModel.Meta):
#         pass
