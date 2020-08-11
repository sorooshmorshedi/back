from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account, FloatAccount, FloatAccountRelation, FloatAccountGroup
from accounts.defaultAccounts.models import DefaultAccount
from companies.models import FinancialYear
from helpers.models import MELLI_CODE, PHONE, EXPLANATION, DECIMAL, BaseModel, DATE, ConfirmationMixin
from sanads.models import Sanad
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

    def save(self, *args, **kwargs) -> None:
        if self.floatAccount:
            self.floatAccount.delete()

        self.floatAccount = FloatAccount.objects.create(
            name=self.name,
            financial_year=self.financial_year,
            is_auto_created=True,
        )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.floatAccount.delete()
        return super(Driver, self).delete(*args, **kwargs)


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
    expenseAccount = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='carExpense', null=True)

    # just for Rahman
    incomeAccount = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='carIncome', null=True)

    payableAccount = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='carPayable', null=True)

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

        if self.expenseAccount:
            self.expenseAccount.delete()
        if self.incomeAccount:
            self.incomeAccount.delete()
        if self.payableAccount:
            floatAccountGroup = self.payableAccount.floatAccountGroup
            self.payableAccount.delete()
            floatAccountGroup.delete()

        parents = []
        if self.owner == self.RAHMAN:
            parents.append({
                'attr': 'expenseAccount',
                'account': DefaultAccount.get('rahmanCarsTransportationExpense').account,
            })

            parents.append({
                'attr': 'incomeAccount',
                'account': DefaultAccount.get('rahmanCarsTransportationIncome').account,
            })

            parents.append({
                'attr': 'payableAccount',
                'account': DefaultAccount.get('payableAccountForRahmanTransportationDrivers').account,
            })
        elif self.owner == self.PARTNERSHIP:
            parents.append({
                'attr': 'expenseAccount',
                'account': DefaultAccount.get('partnershipCarsTransportationExpense').account,
            })

            parents.append({
                'attr': 'incomeAccount',
                'account': DefaultAccount.get('partnershipCarsTransportationIncome').account,
            })

            parents.append({
                'attr': 'payableAccount',
                'account': DefaultAccount.get('payableAccountForRahmanTransportationDrivers').account,
            })
        elif self.owner == self.RAHIM:
            parents.append({
                'attr': 'payableAccount',
                'account': DefaultAccount.get('partnershipAccountForRahimTransportationDrivers').account,
            })
        elif self.owner == self.EBRAHIM:
            parents.append({
                'attr': 'payableAccount',
                'account': DefaultAccount.get('partnershipAccountForEbrahimTransportationDrivers').account,
            })
        elif self.owner == self.OTHER:
            parents.append({
                'attr': 'payableAccount',
                'account': DefaultAccount.get('partnershipAccountForOtherTransportationDrivers').account,
            })

        for parent in parents:
            parent_account = parent['account']

            account = Account.objects.create(
                name=self.car_number_str,
                parent=parent_account,
                code=parent_account.get_new_child_code(),
                level=Account.TAFSILI,
                financial_year=self.financial_year,
                is_auto_created=True,
            )

            setattr(self, parent['attr'], account)

        self.payableAccount.floatAccountGroup = FloatAccountGroup.objects.create(
            name="رانندگان {}".format(self.car_number_str),
            financial_year=self.financial_year,
            is_auto_created=True,
        )
        self.payableAccount.save()

        if self.expenseAccount:
            self.expenseAccount.floatAccountGroup_id = 1
            self.expenseAccount.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.expenseAccount.delete()
        self.incomeAccount.delete()
        floatAccountGroup = self.payableAccount.floatAccountGroup
        self.payableAccount.delete()
        floatAccountGroup.delete()
        return super().delete(*args, **kwargs)


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

    def save(self, *args, **kwargs) -> None:
        if self.floatAccountRelation:
            self.floatAccountRelation.delete()

        self.floatAccountRelation = FloatAccountRelation.objects.create(
            financial_year=self.financial_year,
            floatAccount=self.driver.floatAccount,
            floatAccountGroup=self.car.payableAccount.floatAccountGroup
        )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.floatAccountRelation.delete()
        return super().delete(*args, **kwargs)


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


class Remittance(RemittanceMixin, ConfirmationMixin):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='remittances')
    code = models.IntegerField(unique=True)
    issue_date = jmodels.jDateField()
    loading_date = jmodels.jDateField()
    end_date = jmodels.jDateField()
    amount = DECIMAL()

    is_finished = models.BooleanField(default=False)

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

            ('firstConfirm.remittance', 'تایید اول حواله '),
            ('secondConfirm.remittance', 'تایید دوم حواله '),
            ('firstConfirmOwn.remittance', 'تایید اول حواله های خود'),
            ('secondConfirmOwn.remittance', 'تایید دوم حواله های خود'),
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


class Lading(RemittanceMixin, ConfirmationMixin):
    OTHER = 'o'
    COMPANY = 'cmp'
    CONTRACTOR = 'cnt'

    CREDIT = 'cr'
    CASH = 'cs'
    POS = 'p'

    BOUGHT = 'b'
    SOLD = 's'

    TIP_PAYERS = (
        (COMPANY, 'شرکت'),
        (CONTRACTOR, 'پیمانکار')
    )

    RECEIVE_TYPES = (
        (CREDIT, 'نسیه'),
        (CASH, 'نقدی'),
        (POS, 'کارت خوان')
    )

    CONTRACTOR_TYPES = (
        (COMPANY, 'شرکت'),
        (OTHER, 'دیگر')
    )

    WARE_TYPES = (
        (BOUGHT, 'خریداری شده'),
        (SOLD, 'فروش رفتخ')
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

    billNumber = models.ForeignKey(LadingBillNumber, on_delete=models.PROTECT, related_name='lading')
    bill_date = jmodels.jDateField()
    bill_price = DECIMAL()

    bill_explanation = EXPLANATION()
    bill_attachment = models.FileField(null=True, blank=True, upload_to=upload_attachment_to)
    cargo_tip_price = DECIMAL()

    association = models.ForeignKey(Association, on_delete=models.PROTECT, related_name='ladings', null=True,
                                    blank=True)
    association_price = DECIMAL()

    receive_type = models.CharField(max_length=2, choices=RECEIVE_TYPES)

    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    origin = models.ForeignKey(City, on_delete=models.PROTECT, related_name='ladingOrigins', null=True, blank=True)
    destination = models.ForeignKey(City, on_delete=models.PROTECT, related_name='ladingDestinations', null=True,
                                    blank=True)
    is_paid = models.BooleanField(default=False)

    contractor_type = models.CharField(max_length=3, choices=CONTRACTOR_TYPES, default=OTHER)
    ware_type = models.CharField(max_length=2, choices=WARE_TYPES, null=True)

    lading_total_value = DECIMAL()
    company_commission_income = DECIMAL()
    car_income = DECIMAL()

    lading_bill_total_value = DECIMAL()

    sanad = models.OneToOneField(Sanad, on_delete=models.PROTECT, related_name='ladings', blank=True, null=True)

    class Meta(BaseModel.Meta):
        permission_basename = 'lading'
        permissions = (
            ('get.lading', 'مشاهده بارگیری'),
            ('create.lading', 'تعریف بارگیری'),
            ('update.lading', 'ویرایش بارگیری'),
            ('delete.lading', 'حذف بارگیری'),

            ('getOwn.lading', 'مشاهده بارگیری های خود'),
            ('updateOwn.lading', 'ویرایش بارگیری های خود'),
            ('deleteOwn.lading', 'حذف بارگیری های خود'),

            ('firstConfirm.lading', 'تایید اول بارگیری '),
            ('secondConfirm.lading', 'تایید دوم بارگیری '),
            ('firstConfirmOwn.lading', 'تایید اول بارگیری های خود'),
            ('secondConfirmOwn.lading', 'تایید دوم بارگیری های خود'),
        )

    def save(self, *args, **kwargs) -> None:
        from _dashtbashi.sanads import LadingSanad
        super().save(*args, **kwargs)
        LadingSanad(self).update()


class OilCompanyLading(BaseModel, ConfirmationMixin):
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

            ('getOwn.oilCompanyLading', 'مشاهده بارگیری شرکت نفت خود'),
            ('updateOwn.oilCompanyLading', 'ویرایش بارگیری شرکت نفت خود'),
            ('deleteOwn.oilCompanyLading', 'حذف بارگیری شرکت نفت خود'),

            ('firstConfirm.oilCompanyLading', 'تایید اول بارگیری شرکت نفت '),
            ('secondConfirm.oilCompanyLading', 'تایید دوم بارگیری شرکت نفت '),
            ('firstConfirmOwn.oilCompanyLading', 'تایید اول بارگیری شرکت نفت خود'),
            ('secondConfirmOwn.oilCompanyLading', 'تایید دوم بارگیری شرکت نفت خود'),
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


class OtherDriverPayment(BaseModel, ConfirmationMixin):
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

            ('firstConfirm.otherDriverPayment', 'تایید اول پرداخت رانندگان متفرقه '),
            ('secondConfirm.otherDriverPayment', 'تایید دوم پرداخت رانندگان متفرقه '),
            ('firstConfirmOwn.otherDriverPayment', 'تایید اول پرداخت رانندگان متفرقه خود'),
            ('secondConfirmOwn.otherDriverPayment', 'تایید دوم پرداخت رانندگان متفرقه خود'),
        )
