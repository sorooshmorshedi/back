from django.db import models
from django.db.models import Q
from django_jalali.db import models as jmodels
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from companies.models import Company
from helpers.models import BaseModel, LockableMixin, DefinableMixin, POSTAL_CODE, DECIMAL, \
    is_valid_melli_code, EXPLANATION
from users.models import City
import datetime

from decimal import Decimal


class Workshop(BaseModel, LockableMixin, DefinableMixin):
    DAILY = 'd'
    MONTHLY = 'm'
    YEARLY = 'y'

    BASE_PAY_TYPES = (
        (DAILY, 'مزد مبنای روزانه'),
        (MONTHLY, 'مزد مبنای ماهیانه')
    )

    REWARD_TYPES = (
        (MONTHLY, 'ماهانه'),
        (YEARLY, 'سالانه')
     )

    CERTAIN = 'c'
    ON_ACCOUNT = 'o'

    HAGHE_SANAVAT_TYPES = (
        (CERTAIN, 'قطعی'),
        (ON_ACCOUNT, 'علی الحساب')
     )

    TYPE1 = 1
    TYPE2 = 3/7
    TAX_EMPLOYER_TYPES = (
        (TYPE1, '7/7'),
        (TYPE2, '2/7')
    )

    DAILY_PAY = 'd'
    BASE_PAY = 'b'
    HR_PAY = 'h'

    PAY_TYPES = (
        (DAILY_PAY, 'حداقل حقوق روزانه'),
        (BASE_PAY, 'مزد مبنا')
    )

    LEAVE_SAVE_PAY_TYPES = (
        (DAILY_PAY, 'حداقل حقوق روزانه'),
        (HR_PAY, 'جمع تمام مزایای حکم کارگزینی')
    )

    CONTINUOUS = 'c'
    NO_CONTINUOUS = 'n'

    SANAVAT_TYPES = (
        (CONTINUOUS, 'پیوسته'),
        (NO_CONTINUOUS, 'نا پیوسته')
    )

    company = models.ForeignKey(Company, related_name='workshop', on_delete=models.CASCADE, )
    code = models.IntegerField()
    contract_row = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    employer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10, validators=[
        RegexValidator(regex='^.{10}$', message='طول کد پستی باید 10 رقم باشد', code='nomatch')], blank=True, null=True)
    employer_insurance_contribution = models.IntegerField()
    branch_code = models.IntegerField(blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)

    # Workshop settings
    base_pay_type = models.CharField(max_length=1, choices=BASE_PAY_TYPES, default=DAILY)
    ezafe_kari_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    tatil_kari_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    kasre_kar_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    shab_kari_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    aele_mandi_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    nobat_kari_sob_asr_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    nobat_kari_sob_shab_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    nobat_kari_asr_shab_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    nobat_kari_sob_asr_shab_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    mission_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    leave_save_pay_type = models.CharField(max_length=1, choices=LEAVE_SAVE_PAY_TYPES, default=DAILY_PAY)

    haghe_sanavat_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    eydi_padash_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    haghe_sanavat_identification = models.CharField(max_length=1, choices=REWARD_TYPES, default=YEARLY)
    eydi_padash_identification = models.CharField(max_length=1, choices=REWARD_TYPES, default=YEARLY)

    sanavat_type = models.CharField(max_length=1, choices=SANAVAT_TYPES, default=CONTINUOUS)

    ezafe_kari_nerkh = models.DecimalField(max_digits=24, default=1.4, decimal_places=2)
    tatil_kari_nerkh = models.DecimalField(max_digits=24, default=1.96, decimal_places=2)
    kasre_kar_nerkh = models.DecimalField(max_digits=24, default=1.4, decimal_places=2)
    shab_kari_nerkh = models.DecimalField(max_digits=24, default=0.35, decimal_places=2)
    aele_mandi_nerkh = models.DecimalField(max_digits=24, default=3, decimal_places=2)
    nobat_kari_sob_asr_nerkh = models.DecimalField(max_digits=24, default=0.1, decimal_places=2)
    nobat_kari_sob_shab_nerkh = models.DecimalField(max_digits=24, default=0.225, decimal_places=2)
    nobat_kari_asr_shab_nerkh = models.DecimalField(max_digits=24, default=0.025, decimal_places=2)
    nobat_kari_sob_asr_shab_nerkh = models.DecimalField(max_digits=24, default=0.15, decimal_places=2)
    mission_pay_nerkh = models.DecimalField(max_digits=24, default=1, decimal_places=2)
    unemployed_insurance_nerkh = models.DecimalField(max_digits=24, default=0.03, decimal_places=2)
    worker_insurance_nerkh = models.DecimalField(max_digits=24, default=0.03, decimal_places=2)
    employee_insurance_nerkh = models.DecimalField(max_digits=24, default=0.2, decimal_places=2)

    haghe_sanavat_type = models.CharField(max_length=1, choices=HAGHE_SANAVAT_TYPES, default=CERTAIN)
    hade_aghal_hoghoogh = DECIMAL(default=1400000)

    made_86_nerkh = DECIMAL(default=0.1)
    hade_aksar_mashmool_bime = models.BooleanField(default=True)

    tax_employer_type = models.IntegerField(choices=TAX_EMPLOYER_TYPES, default=TYPE1)

    class Meta(BaseModel.Meta):
        verbose_name = 'Workshop'
        permission_basename = 'workshop'
        permissions = (
            ('get.workshop', 'مشاهده کارگاه'),
            ('create.workshop', 'تعریف کارگاه'),
            ('update.workshop', 'ویرایش کارگاه'),
            ('delete.workshop', 'حذف کارگاه'),

            ('getOwn.workshop', 'مشاهده کارگاه خود'),
            ('updateOwn.workshop', 'ویرایش کارگاه خود'),
            ('deleteOwn.workshop', 'حذف کارگاه خود'),
        )

    @property
    def workshop_title(self):
        return self.name + ' ' + str(self.code)

    def __str__(self):
        return self.name + ' ' + self.company.name


class WorkshopTax(BaseModel, LockableMixin, DefinableMixin):
    name = models.CharField(max_length=100, blank=True, null=True)
    from_date = jmodels.jDateField(blank=True, null=True)
    to_date = jmodels.jDateField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'WorkshopTax'
        permission_basename = 'workshop_tax'
        permissions = (
            ('get.workshop_tax', 'مشاهده  معاف مالیات'),
            ('create.workshop_tax', 'تعریف  معاف مالیات'),
            ('update.workshop_tax', 'ویرایش  معاف مالیات'),
            ('delete.workshop_tax', 'حذف  معاف مالیات'),

            ('getOwn.workshop_tax', 'مشاهده  معاف مالیات خود'),
            ('updateOwn.workshop_tax', 'ویرایش  معاف مالیات خود'),
            ('deleteOwn.workshop_tax', 'حذف  معاف مالیات خود'),
        )

    def __str__(self):
        return 'از ' + self.from_date.__str__() + ' تا' + self.to_date.__str__()

    def save(self, *args, **kwargs):
        if self.from_date.__ge__(self.to_date):
            raise ValidationError('تاریخ شروع باید از تاریخ پایان کوچکتر باشد')
        super().save(*args, **kwargs)


class WorkshopTaxRow(BaseModel, LockableMixin, DefinableMixin):
    workshop_tax = models.ForeignKey(WorkshopTax, related_name='tax_row', on_delete=models.CASCADE,
                                     blank=True, null=True)
    from_amount = DECIMAL(default=0)
    to_amount = DECIMAL(default=0)
    ratio = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = ['-pk']
        verbose_name = 'WorkshopTaxRow'
        permission_basename = 'workshop_tax_row'
        permissions = (
            ('get.workshop_tax_row', 'مشاهده ردیف معاف مالیات'),
            ('create.workshop_tax_row', 'تعریف ردیف معاف مالیات'),
            ('update.workshop_tax_row', 'ویرایش ردیف معاف مالیات'),
            ('delete.workshop_tax_row', 'حذف ردیف معاف مالیات'),

            ('getOwn.workshop_tax_row', 'مشاهده ردیف معاف مالیات خود'),
            ('updateOwn.workshop_tax_row', 'ویرایش ردیف معاف مالیات خود'),
            ('deleteOwn.workshop_tax_row', 'حذف ردیف معاف مالیات خود'),
        )

    @property
    def auto_from_amount(self):
        query = WorkshopTaxRow.objects.filter(workshop_tax=self.workshop_tax).first()
        return query.to_amount + Decimal(1)

    @property
    def monthly_from_amount(self):
        return round(self.from_amount / Decimal(12), 2)

    @property
    def monthly_to_amount(self):
        return round(self.to_amount / Decimal(12), 2)

    def __str__(self):
        return 'از ' + str(round(self.from_amount)) + ' تا ' + str(round(self.to_amount)) + ' : ' \
               + str(self.ratio) + ' % '

    def save(self, *args, **kwargs):
        query = WorkshopTaxRow.objects.filter(workshop_tax=self.workshop_tax)
        if len(query) < 1:
            self.from_amount = 0
            self.ratio = 0
        else:
            self.from_amount = self.auto_from_amount
        if self.from_amount >= self.to_amount:
            raise ValidationError('مقدار مبلغ پایان باید بزرگتر از مبلغ شروع باشد')
        super().save(*args, **kwargs)


class ContractRow(BaseModel, LockableMixin, DefinableMixin):
    ACTIVE = 'a'
    NO_ACTIVE = 'n'

    ACTIVE_TYPE = (
        (ACTIVE, 'فعال'),
        (NO_ACTIVE, 'غیر فعال')
    )

    workshop = models.ForeignKey(Workshop, related_name='contract_rows', on_delete=models.CASCADE)
    contract_row = models.CharField(max_length=10, blank=True, null=True)
    contract_number = models.IntegerField()
    registration_date = jmodels.jDateField(blank=True, null=True)
    from_date = jmodels.jDateField(blank=True, null=True)
    to_date = jmodels.jDateField(blank=True, null=True)
    topic = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(max_length=1, choices=ACTIVE_TYPE, default=NO_ACTIVE)
    assignor_name = models.CharField(max_length=100, blank=True, null=True)
    assignor_national_code = models.IntegerField(unique=True)
    assignor_workshop_code = models.IntegerField()

    contract_initial_amount = DECIMAL()
    branch = models.CharField(max_length=100, blank=True, null=True)

    class Meta(BaseModel.Meta):
        ordering = ['-pk']
        verbose_name = 'ContractRow'
        permission_basename = 'contract_row'
        permissions = (
            ('get.contract_row', 'مشاهده ردیف پیمان'),
            ('create.contract_row', 'تعریف ردیف پیمان'),
            ('update.contract_row', 'ویرایش ردیف پیمان'),
            ('delete.contract_row', 'حذف ردیف پیمان'),

            ('getOwn.contract_row', 'مشاهده ردیف پیمان خود'),
            ('updateOwn.contract_row', 'ویرایش ردیف پیمان خود'),
            ('deleteOwn.contract_row', 'حذف ردیف پیمان خود'),
        )

    def __str__(self):
        return str(self.contract_row) + ' در ' + self.workshop.workshop_title

    @property
    def title(self):
        return str(self.contract_row) + ' در کارگاه ' + self.workshop.name


class Personnel(BaseModel, LockableMixin, DefinableMixin):
    IRANIAN = 'i'
    OTHER = 'o'

    NATIONALITY_TYPE = (
        (IRANIAN, 'ایرانی'),
        (OTHER, 'غیر ایرانی')
    )

    MALE = 'm'
    FEMALE = 'f'

    GENDER_TYPE = (
        (MALE, 'مرد'),
        (FEMALE, 'زن')
    )

    DONE = 'd'
    NOT_DONE = 'n'
    EXEMPT = 'e'
    NONE = 'x'

    MILITARY_SERVICE_STATUS = (
        (DONE, 'انجام داده'),
        (NOT_DONE, 'انجام نداده'),
        (EXEMPT, 'معاف'),
        (NONE, 'هبچ کدام')

    )

    SINGLE = 's'
    MARRIED = 'm'
    CHILDREN_WARDSHIP = 'c'

    MARITAL_STATUS_TYPES = (
        (SINGLE, 'مجرد'),
        (MARRIED, 'متاهل'),
        (CHILDREN_WARDSHIP, 'سرپرست فرزند')
    )

    UNDER_DIPLOMA = 'un'
    DIPLOMA = 'di'
    ASSOCIATES = 'as'
    BACHELOR = 'ba'
    MASTER = 'ma'
    DOCTORAL = 'do'
    POSTDOCTORAL = 'pd'

    DEGREE_TYPE = (
        (UNDER_DIPLOMA, 'زیر دیپلم'),
        (DIPLOMA, 'دیپلم'),
        (ASSOCIATES, 'کاردانی'),
        (BACHELOR, 'لیسانس'),
        (MASTER, 'فوق لیسانس'),
        (DOCTORAL, 'دکترا'),
        (POSTDOCTORAL, 'فوق دکترا')
    )

    STATE = 'st'
    OPEN = 'op'
    NONE_PROFIT = 'np'

    UNIVERSITY_TYPES = (
        (STATE, 'دولتی'),
        (OPEN, 'آزاد'),
        (NONE_PROFIT, 'غیر انتفاعی')
    )

    company = models.ForeignKey(Company, related_name='personnel', on_delete=models.CASCADE)

    name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=1, choices=NATIONALITY_TYPE, default=IRANIAN)

    personnel_code = models.IntegerField(blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDER_TYPE, default=MALE)
    military_service = models.CharField(max_length=1, choices=MILITARY_SERVICE_STATUS, default=NOT_DONE)

    national_code = models.CharField(max_length=15, blank=True, null=True)

    identity_code = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = jmodels.jDateField(blank=True, null=True)
    date_of_exportation = jmodels.jDateField(blank=True, null=True)
    location_of_birth = models.CharField(max_length=50, blank=True, null=True)
    location_of_exportation = models.CharField(max_length=50, blank=True, null=True)
    sector_of_exportation = models.CharField(max_length=50, blank=True, null=True)

    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_TYPES, default=SINGLE)
    number_of_childes = models.IntegerField(default=0)

    city_phone_code = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    mobile_number_1 = models.CharField(max_length=50, blank=True, null=True)
    mobile_number_2 = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    postal_code = POSTAL_CODE(null=True, blank=True)

    insurance = models.BooleanField(default=False)
    insurance_code = models.IntegerField(blank=True, null=True)

    degree_education = models.CharField(max_length=2, choices=DEGREE_TYPE, default=DIPLOMA)
    field_of_study = models.CharField(max_length=100, null=True, blank=True)
    university_type = models.CharField(max_length=2, choices=UNIVERSITY_TYPES, blank=True, null=True)
    university_name = models.CharField(max_length=50, blank=True, null=True)

    account_bank_name = models.CharField(max_length=50, blank=True, null=True)
    account_bank_number = models.CharField(max_length=50, blank=True, null=True)
    bank_cart_number = models.CharField(max_length=50, blank=True, null=True)
    sheba_number = models.CharField(max_length=50, blank=True, null=True)

    is_personnel_active = models.BooleanField(default=False, null=True, blank=True)
    is_personnel_verified = models.BooleanField(default=False, null=True, blank=True)

    class Meta(BaseModel.Meta):
        ordering = ['-pk', ]
        verbose_name = 'Personnel'
        permission_basename = 'personnel'
        permissions = (
            ('get.personnel', 'مشاهده پرسنل'),
            ('create.personnel', 'تعریف پرسنل'),
            ('update.personnel', 'ویرایش پرسنل'),
            ('delete.personnel', 'حذف پرسنل'),

            ('getOwn.personnel', 'مشاهده پرسنل خود'),
            ('updateOwn.personnel', 'ویرایش پرسنل خود'),
            ('deleteOwn.personnel', 'حذف پرسنل خود'),
        )

    @property
    def full_name(self):
        return self.name + ' ' + self.last_name

    @property
    def system_code(self):
        try:
            company_personnel = Personnel.objects.filter(company=self.company).first()
            personnel_code = company_personnel.personnel_code
            code = personnel_code + 1
        except:
            code = 100
        return code

    def save(self, *args, **kwargs):
        if not self.id and not self.personnel_code:
            self.personnel_code = self.system_code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name + ' در ' + self.company.name


class PersonnelFamily(BaseModel, LockableMixin, DefinableMixin):
    FATHER = 'f'
    MOTHER = 'm'
    CHILD = 'c'
    SPOUSE = 's'

    RELATIVE_TYPE = (
        (FATHER, 'پدر'),
        (MOTHER, 'مادر'),
        (CHILD, 'فرزند'),
        (SPOUSE, 'همسر')
    )

    SINGLE = 's'
    MARRIED = 'm'
    CHILDREN_WARDSHIP = 'c'

    MARITAL_STATUS_TYPES = (
        (SINGLE, 'مجرد'),
        (MARRIED, 'متاهل'),
        (CHILDREN_WARDSHIP, 'سرپرست فرزند')
    )

    DONE = 'd'
    NOT_DONE = 'n'
    EXEMPT = 'e'
    NONE = 'x'

    MILITARY_SERVICE_STATUS = (
        (DONE, 'انجام داده'),
        (NOT_DONE, 'انجام نداده'),
        (EXEMPT, 'معاف'),
        (NONE, 'هیچ کدام')
    )

    STUDENT = 's'
    NON_STUDENT = 'n'

    STUDY_TYPE = (
        (STUDENT, 'محصل'),
        (NON_STUDENT, 'غیر محصل')
    )

    HEALTHY = 'h'
    PATIENT = 'p'
    MAIM = 'm'

    PHYSICAL_TYPE = (
        (HEALTHY, 'سالم'),
        (PATIENT, 'بیمار'),
        (MAIM, 'نفص عضو')
    )

    personnel = models.ForeignKey(Personnel, related_name='personnel_family', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    national_code = models.CharField(max_length=10, unique=True)
    date_of_birth = jmodels.jDateField(blank=True, null=True)
    relative = models.CharField(max_length=1, choices=RELATIVE_TYPE, default=SPOUSE)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_TYPES, default=SINGLE)
    military_service = models.CharField(max_length=1, choices=MILITARY_SERVICE_STATUS, default=NOT_DONE)
    study_status = models.CharField(max_length=1, choices=STUDY_TYPE, default=STUDENT)
    physical_condition = models.CharField(max_length=1, choices=PHYSICAL_TYPE, default=HEALTHY)

    class Meta(BaseModel.Meta):
        verbose_name = 'PersonnelFamily'
        permission_basename = 'personnel_family'
        permissions = (
            ('get.personnel_family', 'مشاهده خانواده پرسنل'),
            ('create.personnel_family', 'تعریف خانواده پرسنل'),
            ('update.personnel_family', 'ویرایش خانواده پرسنل'),
            ('delete.personnel_family', 'حذف خانواده پرسنل'),

            ('getOwn.personnel_family', 'مشاهده خانواده پرسنل خود'),
            ('updateOwn.personnel_family', 'ویرایش خانواده پرسنل خود'),
            ('deleteOwn.personnel_family', 'حذف خانواده پرسنل خود'),
        )

    @property
    def full_name(self):
        return self.name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.relative == 'c' and not self.id:
            personnel = self.personnel
            personnel.number_of_childes += 1
            personnel.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.relative == 'c':
            personnel = self.personnel
            personnel.number_of_childes -= 1
            personnel.save()
        super().delete()

    def __str__(self):
        return self.full_name + ' ' + self.get_relative_display() + ' ' + self.personnel.full_name


class WorkshopPersonnel(BaseModel, LockableMixin, DefinableMixin):
    PART_TIME = 'p'
    FULL_TIME = 'f'
    TEMPORARY = 't'
    HOURLY = 'h'
    CONTRACTUAL = 'c'

    CONTRACT_TYPES = (
        (PART_TIME, 'پاره وقت'),
        (FULL_TIME, 'تمام وقت'),
        (TEMPORARY, 'موقت'),
        (HOURLY, 'ساعتی'),
        (CONTRACTUAL, 'پیمانی')

    )

    CONTRACTUAL = 'c'
    CONVENTIONAL = 'co'
    CORPORATE = 'cr'
    FUNCTIONARY = 'fu'
    PERMANENT = 'p'
    OTHERS = 'or'

    EMPLOYMENTS_TYPES = (
        (CONTRACTUAL, 'پیمانی'),
        (CONVENTIONAL, 'قراردادی'),
        (CORPORATE, 'َشرکتی'),
        (FUNCTIONARY, 'مامور'),
        (PERMANENT, 'رسمی'),
        (OTHERS, 'سایر')

    )

    NORMAL = 'nr'
    FALLEN_CHILD = 'fc'
    STUNTMAN = 'st'
    FREEDMAN = 'fr'
    ARM = 'ar'
    BAND19 = 'bn'
    FOREIGN = 'fo'

    EMPLOYEE_TYPES = (
        (NORMAL, 'معمولی'),
        (FALLEN_CHILD, 'فرزند شهید'),
        (STUNTMAN, 'جانباز'),
        (FREEDMAN, 'آزاده'),
        (ARM, 'نیروهای مسلح'),
        (BAND19, 'مشمولین بند چهارده ماده نود و هفت'),
        (FOREIGN, 'اتباع خارجی مشمول قانون اجتناب از اخذ مالیات مضاعف')
    )

    NORMAL = 'nr'
    DEPRIVED_AREAS = 'dp'
    FREE_TRADE_ZONE = 'ft'
    SCIENCE_PARK = 'sp'

    JOB_LOCATION_STATUSES = (
        (NORMAL, 'معمولی'),
        (DEPRIVED_AREAS, 'مناطق کمتر توسعه یافته'),
        (FREE_TRADE_ZONE, 'مناطق آزاد تجاری'),
        (SCIENCE_PARK, 'پارک علم و فناوری'),
    )

    STUDY = 'st'
    FINANCIAL = 'fn'
    SOCIAL = 'so'
    HEALTH = 'he'
    IT = 'it'
    SERVICES = 'se'
    ENGINEER = 'en'
    ARGI = 'ar'
    PRODUCT = 'pr'
    SEARCH = 'sr'
    WORKER = 'wo'
    SECURITY = 'sc'
    TRANSFORM = 'tr'
    SALE = 'sa'
    JUDGE = 'ju'
    WAREHOUSE = 'wa'
    CONTROL = 'co'
    MASTER = 'ma'
    OTHER = 'ot'

    JOB_GROUP_TYPES = (
        (STUDY, 'آموزشي و فرهنگي'),
        (FINANCIAL, 'اداري و مالي'),
        (SOCIAL, 'اموراجتماعي'),
        (HEALTH, 'درماني و بهداشتي'),
        (IT, 'اطلاعات فناوري'),
        (SERVICES, 'خدمات'),
        (ENGINEER, 'فني و مهندسي'),
        (ARGI, 'كشاورزي ومحيط زيست'),
        (PRODUCT, 'تولیدی'),
        (SEARCH, 'تحقیقاتی'),
        (WORKER, 'کارگری'),
        (SECURITY, 'حراست و نگهبانی'),
        (TRANSFORM, 'ترابری'),
        (SALE, 'بازاریابی و فروش'),
        (JUDGE, 'قضات'),
        (WAREHOUSE, 'انبارداری'),
        (CONTROL, 'کنترل کیفی'),
        (MASTER, 'هیات علمی'),
        (OTHER, 'سایر'),
    )

    workshop = models.ForeignKey(Workshop, related_name='workshop_personnel', on_delete=models.CASCADE, blank=True, null=True)
    personnel = models.ForeignKey(Personnel, related_name='workshop_personnel', on_delete=models.CASCADE, blank=True, null=True)
    contract_row = models.ManyToManyField(ContractRow, related_name='workshop_personnel', blank=True)

    insurance_add_date = jmodels.jDateField(blank=True, null=True)
    work_title = models.CharField(max_length=100, blank=True, null=True)

    previous_insurance_history_out_workshop = models.IntegerField(blank=True, null=True)
    previous_insurance_history_in_workshop = models.IntegerField(blank=True, null=True)
    current_insurance_history_in_workshop = models.IntegerField(blank=True, null=True)
    insurance_history_totality = models.IntegerField(blank=True, null=True)

    job_position = models.CharField(max_length=100)
    job_group = models.CharField(max_length=2, choices=JOB_GROUP_TYPES)
    job_location = models.CharField(max_length=100)
    job_location_status = models.CharField(max_length=2, choices=JOB_LOCATION_STATUSES, default=NORMAL)

    employment_type = models.CharField(max_length=2, choices=EMPLOYMENTS_TYPES, default=CONVENTIONAL)
    contract_type = models.CharField(max_length=2, choices=CONTRACT_TYPES, default=FULL_TIME)
    employee_status = models.CharField(max_length=2, choices=EMPLOYEE_TYPES, default=NORMAL)

    haghe_sanavat_days = models.IntegerField(default=0)
    haghe_sanavat_identify_amount = DECIMAL(default=0)

    @property
    def my_title(self):
        return self.personnel.full_name + ' در کارگاه ' + self.workshop.name

    class Meta(BaseModel.Meta):
        verbose_name = 'WorkshopPersonnel'
        permission_basename = 'workshop_personnel'
        permissions = (
            ('get.workshop_personnel', 'مشاهده پرسنل کارگاه'),
            ('create.workshop_personnel', 'تعریف پرسنل کارگاه'),
            ('update.workshop_personnel', 'ویرایش پرسنل کارگاه'),
            ('delete.workshop_personnel', 'حذف پرسنل کارگاه'),

            ('getOwn.workshop_personnel', 'مشاهده پرسنل کارگاه خود'),
            ('updateOwn.workshop_personnel', 'ویرایش پرسنل کارگاه خود'),
            ('deleteOwn.workshop_personnel', 'حذف پرسنل کارگاه خود'),
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self.current_insurance_history_in_workshop = 0
        self.insurance_history_totality = self.previous_insurance_history_in_workshop +\
                                            self.previous_insurance_history_out_workshop +\
                                            self.current_insurance_history_in_workshop
        super().save(*args, **kwargs)

    def __str__(self):
        return self.my_title



class Contract(BaseModel, LockableMixin, DefinableMixin):
    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name='contract',
                                            on_delete=models.CASCADE, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    insurance = models.BooleanField(default=False)
    insurance_add_date = jmodels.jDateField(blank=True, null=True)
    contract_from_date = jmodels.jDateField(blank=True, null=True)
    contract_to_date = jmodels.jDateField(blank=True, null=True)
    quit_job_date = jmodels.jDateField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'Contract'
        permission_basename = 'contract'
        permissions = (
            ('get.contract', 'مشاهده قرارداد'),
            ('create.contract', 'تعریف قرارداد'),
            ('update.contract', 'ویرایش قرارداد'),
            ('delete.contract', 'حذف قرارداد'),

            ('getOwn.contract', 'مشاهده قرارداد خود'),
            ('updateOwn.contract', 'ویرایش قرارداد خود'),
            ('deleteOwn.contract', 'حذف قرارداد خود'),
        )

    def save(self, *args, **kwargs):
        if not self.insurance:
            self.workshop_personnel.insurance_add_date = None
        else:
            self.workshop_personnel.insurance_add_date = self.contract_from_date
        if not self.quit_job_date:
            self.workshop_personnel.current_insurance_history_in_workshop =\
                self.contract_to_date.month + self.contract_from_date.month
        if self.quit_job_date:
            self.workshop_personnel.current_insurance_history_in_workshop =\
                self.quit_job_date.month + self.contract_from_date.month

        self.workshop_personnel.save()
        super().save(*args, **kwargs)

    @property
    def workshop_personnel_display(self):
        return self.workshop_personnel.my_title

    def __str__(self):
        return str(self.code) + ' برای ' + self.workshop_personnel_display


class LeaveOrAbsence(BaseModel, LockableMixin, DefinableMixin):
    ENTITLEMENT = 'e'
    ILLNESS = 'i'
    WITHOUT_SALARY = 'w'
    ABSENCE = 'a'
    MATTER_73 = 'm'

    LEAVE_TYPES = (
        (ENTITLEMENT, 'استحقاقی'),
        (ILLNESS, 'استعلاجی'),
        (WITHOUT_SALARY, 'بدون حقوق'),
        (ABSENCE, 'غیبت'),
        (MATTER_73, 'ماده 73'),
    )

    HOURLY = 'h'
    DAILY = 'd'

    ENTITLEMENT_LEAVE_TYPES = (
        (HOURLY, 'ساعتی'),
        (DAILY, 'روزانه'),

    )

    CHILDBIRTH = 'c'
    MARRIAGE = 'm'
    SPOUSAL_DEATH = 's'
    CHILD_DEATH = 'd'
    PARENT_DEATH = 'p'

    MATTER_73_LEAVE_TYPES = (
        (CHILDBIRTH, 'زایمان'),
        (MARRIAGE, 'ازدواج'),
        (SPOUSAL_DEATH, 'مرگ همسر'),
        (CHILD_DEATH, 'مرگ فرزند'),
        (PARENT_DEATH, 'مرگ پدر یا مادر'),

    )

    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name='leave', on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPES, default=WITHOUT_SALARY)
    entitlement_leave_type = models.CharField(max_length=2, choices=ENTITLEMENT_LEAVE_TYPES, blank=True, null=True)
    matter_73_leave_type = models.CharField(max_length=2, choices=MATTER_73_LEAVE_TYPES, blank=True, null=True)
    from_date = jmodels.jDateField(blank=True, null=True)
    to_date = jmodels.jDateField(blank=True, null=True)
    date = jmodels.jDateField(blank=True, null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)
    explanation = EXPLANATION()
    cause_of_incident = EXPLANATION()
    time_period = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=2)

    @property
    def final_by_day(self):
        if self.leave_type == 'e' and self.entitlement_leave_type == 'h':
            duration = datetime.timedelta(hours=self.to_hour.hour - self.from_hour.hour,
                                            minutes=self.to_hour.minute - self.from_hour.minute)
            final_by_day = (duration.seconds / 60) / 440
        else:
            difference = self.to_date - self.from_date
            final_by_day = difference.days + 1
            if self.leave_type == 'm' and final_by_day > 3:
                final_by_day = 3
        return final_by_day

    def save(self, *args, **kwargs):
        if self.leave_type == 'm':
            duration = datetime.timedelta(days=2)
            if self.to_date.day - self.from_date.day > 2:
                self.to_date = self.from_date + duration
        if self.leave_type == 'e' and self.entitlement_leave_type == 'h':
            self.from_date, self.to_date, = None, None
            if not self.from_hour or not self.to_hour or not self.date:
                raise ValidationError('برای مرخصی ساعتی ساعت شروع و پایان و تاریخ را وارد کنید')
        elif self.leave_type == 'e' and self.entitlement_leave_type == 'd':
            self.date, self.from_hour, self.to_hour = None, None, None
            if not self.from_date or not self.to_date:
                raise ValidationError('برای مرخصی روزانه تاریح شروع و پایان را وارد کنید')
        elif self.leave_type == 'i':
            self.from_hour, self.to_hour, self.date = None, None, None
            if not self.from_date or not self.to_date:
                raise ValidationError('برای مرخصی استعلاجی تاریح شروع و پایان را وارد کنید')
            if not self.cause_of_incident:
                raise ValidationError('برای مرخصی استعلاجی علت حادثه را وارد کنید')
        elif self.leave_type == 'w' or self.leave_type == 'a':
            self.from_hour, self.to_hour, self.date = None, None, None
            if not self.from_date or not self.to_date:
                raise ValidationError(' تاریح شروع و پایان را وارد کنید')
        self.time_period = self.final_by_day
        super().save(*args, **kwargs)

    class Meta(BaseModel.Meta):
        verbose_name = 'LeaveOrAbsence'
        permission_basename = 'leave_or_absence'
        permissions = (
            ('get.leave_or_absence', 'مشاهده مرخصی'),
            ('create.leave_or_absence', 'تعریف مرخصی'),
            ('update.leave_or_absence', 'ویرایش مرخصی'),
            ('delete.leave_or_absence', 'حذف مرخصی'),

            ('getOwn.leave_or_absence', 'مشاهده مرخصی خود'),
            ('updateOwn.leave_or_absence', 'ویرایش مرخصی خود'),
            ('deleteOwn.leave_or_absence', 'حذف مرخصی خود'),
        )

    def __str__(self):
        return str(self.final_by_day) + 'روز برای ' + self.workshop_personnel.personnel.full_name


class HRLetter(BaseModel, LockableMixin, DefinableMixin):
    BASE_PAY = 'b'
    PENSION = 'p'
    UN_PENSION = 'u'

    NATURE_TYPES = (
        (BASE_PAY, 'دستمزد رورانه'),
        (PENSION, 'مستمر'),
        (UN_PENSION, 'غیر مستمر')
    )

    THEME = 't'
    PERSONNEL = 'p'

    HRLETTER_TYPES = (
        (THEME, 'قالب'),
        (PERSONNEL, 'شخصی')
    )

    contract = models.ForeignKey(Contract, related_name='hr_letter', on_delete=models.CASCADE,
                                    blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_template = models.CharField(max_length=1, choices=HRLETTER_TYPES)

    pay_done = models.BooleanField(default=False)
    daily_pay_base = models.IntegerField(default=0)
    monthly_pay_base = models.IntegerField(default=0)
    day_hourly_pay_base = models.IntegerField(default=0)
    month_hourly_pay_base = models.IntegerField(default=0)
    insurance_pay_day = models.IntegerField(default=0)
    insurance_benefit = models.IntegerField(default=0)
    insurance_not_included = models.IntegerField(default=0)

    hoghooghe_roozane_use_tax = models.BooleanField(default=True)
    hoghooghe_roozane_use_insurance = models.BooleanField(default=True)
    hoghooghe_roozane_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    hoghooghe_roozane_amount = DECIMAL(default=0)
    hoghooghe_roozane_base = models.BooleanField(default=False)

    paye_sanavat_use_tax = models.BooleanField(default=True)
    paye_sanavat_use_insurance = models.BooleanField(default=True)
    paye_sanavat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    paye_sanavat_amount = DECIMAL(default=0)
    paye_sanavat_base = models.BooleanField(default=False)

    haghe_sarparasti_use_tax = models.BooleanField(default=True)
    haghe_sarparasti_use_insurance = models.BooleanField(default=True)
    haghe_sarparasti_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_sarparasti_amount = DECIMAL(default=0)
    haghe_sarparasti_base = models.BooleanField(default=False)

    haghe_modiriyat_use_tax = models.BooleanField(default=True)
    haghe_modiriyat_use_insurance = models.BooleanField(default=True)
    haghe_modiriyat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_modiriyat_amount = DECIMAL(default=0)
    haghe_modiriyat_base = models.BooleanField(default=False)

    haghe_jazb_use_tax = models.BooleanField(default=True)
    haghe_jazb_use_insurance = models.BooleanField(default=True)
    haghe_jazb_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_jazb_amount = DECIMAL(default=0)
    haghe_jazb_base = models.BooleanField(default=False)

    fogholade_shoghl_use_tax = models.BooleanField(default=True)
    fogholade_shoghl_use_insurance = models.BooleanField(default=True)
    fogholade_shoghl_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    fogholade_shoghl_amount = DECIMAL(default=0)
    fogholade_shoghl_base = models.BooleanField(default=False)

    haghe_tahsilat_use_tax = models.BooleanField(default=True)
    haghe_tahsilat_use_insurance = models.BooleanField(default=True)
    haghe_tahsilat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_tahsilat_amount = DECIMAL(default=0)
    haghe_tahsilat_base = models.BooleanField(default=False)

    fogholade_sakhti_kar_use_tax = models.BooleanField(default=True)
    fogholade_sakhti_kar_use_insurance = models.BooleanField(default=True)
    fogholade_sakhti_kar_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    fogholade_sakhti_kar_amount = DECIMAL(default=0)
    fogholade_sakhti_kar_base = models.BooleanField(default=False)

    haghe_ankal_use_tax = models.BooleanField(default=True)
    haghe_ankal_use_insurance = models.BooleanField(default=True)
    haghe_ankal_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_ankal_amount = DECIMAL(default=0)
    haghe_ankal_base = models.BooleanField(default=False)

    fogholade_badi_abohava_use_tax = models.BooleanField(default=True)
    fogholade_badi_abohava_use_insurance = models.BooleanField(default=True)
    fogholade_badi_abohava_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    fogholade_badi_abohava_amount = DECIMAL(default=0)
    fogholade_badi_abohava_base = models.BooleanField(default=False)

    mahroomiat_tashilat_zendegi_use_tax = models.BooleanField(default=True)
    mahroomiat_tashilat_zendegi_use_insurance = models.BooleanField(default=True)
    mahroomiat_tashilat_zendegi_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    mahroomiat_tashilat_zendegi_amount = DECIMAL(default=0)
    mahroomiat_tashilat_zendegi_base = models.BooleanField(default=False)

    fogholade_mahal_khedmat_use_tax = models.BooleanField(default=True)
    fogholade_mahal_khedmat_use_insurance = models.BooleanField(default=True)
    fogholade_mahal_khedmat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    fogholade_mahal_khedmat_amount = DECIMAL(default=0)
    fogholade_mahal_khedmat_base = models.BooleanField(default=False)

    fogholade_sharayet_mohit_kar_use_tax = models.BooleanField(default=True)
    fogholade_sharayet_mohit_kar_use_insurance = models.BooleanField(default=True)
    fogholade_sharayet_mohit_kar_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    fogholade_sharayet_mohit_kar_amount = DECIMAL(default=0)
    fogholade_sharayet_mohit_kar_base = models.BooleanField(default=False)

    haghe_maskan_use_tax = models.BooleanField(default=True)
    haghe_maskan_use_insurance = models.BooleanField(default=True)
    haghe_maskan_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_maskan_amount = DECIMAL(default=0)
    haghe_maskan_base = models.BooleanField(default=False)

    ayabo_zahab_use_tax = models.BooleanField(default=True)
    ayabo_zahab_use_insurance = models.BooleanField(default=True)
    ayabo_zahab_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    ayabo_zahab_amount = DECIMAL(default=0)
    ayabo_zahab_base = models.BooleanField(default=False)

    bon_kharo_bar_use_tax = models.BooleanField(default=True)
    bon_kharo_bar_use_insurance = models.BooleanField(default=True)
    bon_kharo_bar_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    bon_kharo_bar_amount = DECIMAL(default=0)
    bon_kharo_bar_base = models.BooleanField(default=False)

    yarane_ghaza_use_tax = models.BooleanField(default=True)
    yarane_ghaza_use_insurance = models.BooleanField(default=True)
    yarane_ghaza_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    yarane_ghaza_amount = DECIMAL(default=0)
    yarane_ghaza_base = models.BooleanField(default=False)

    haghe_shir_use_tax = models.BooleanField(default=True)
    haghe_shir_use_insurance = models.BooleanField(default=True)
    haghe_shir_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_shir_amount = DECIMAL(default=0)
    haghe_shir_base = models.BooleanField(default=False)

    haghe_taahol_use_tax = models.BooleanField(default=True)
    haghe_taahol_use_insurance = models.BooleanField(default=True)
    haghe_taahol_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_taahol_amount = DECIMAL(default=0)
    haghe_taahol_base = models.BooleanField(default=False)

    komakhazine_mahdekoodak_use_tax = models.BooleanField(default=True)
    komakhazine_mahdekoodak_use_insurance = models.BooleanField(default=True)
    komakhazine_mahdekoodak_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    komakhazine_mahdekoodak_amount = DECIMAL(default=0)
    komakhazine_mahdekoodak_base = models.BooleanField(default=False)

    komakhazine_varzesh_use_tax = models.BooleanField(default=True)
    komakhazine_varzesh_use_insurance = models.BooleanField(default=True)
    komakhazine_varzesh_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    komakhazine_varzesh_amount = DECIMAL(default=0)
    komakhazine_varzesh_base= models.BooleanField(default=False)

    komakhazine_mobile_use_tax = models.BooleanField(default=True)
    komakhazine_mobile_use_insurance = models.BooleanField(default=True)
    komakhazine_mobile_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    komakhazine_mobile_amount = DECIMAL(default=0)
    komakhazine_mobile_base = models.BooleanField(default=False)

    mazaya_mostamar_gheyre_naghdi_use_tax = models.BooleanField(default=True)
    mazaya_mostamar_gheyre_naghdi_use_insurance = models.BooleanField(default=True)
    mazaya_mostamar_gheyre_naghdi_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=PENSION)
    mazaya_mostamar_gheyre_naghdi_amount = DECIMAL(default=0)
    mazaya_mostamar_gheyre_naghdi_base = models.BooleanField(default=False)

    ezafe_kari_use_tax = models.BooleanField(default=True)
    ezafe_kari_use_insurance = models.BooleanField(default=True)
    ezafe_kari_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=UN_PENSION)

    haghe_owlad_use_tax = models.BooleanField(default=True)
    haghe_owlad_use_insurance = models.BooleanField(default=True)
    haghe_owlad_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=UN_PENSION)

    jome_kari_use_tax = models.BooleanField(default=True)
    jome_kari_use_insurance = models.BooleanField(default=True)
    jome_kari_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=UN_PENSION)

    shab_kari_use_tax = models.BooleanField(default=True)
    shab_kari_use_insurance = models.BooleanField(default=True)
    shab_kari_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=UN_PENSION)

    tatil_kari_use_tax = models.BooleanField(default=True)
    tatil_kari_use_insurance = models.BooleanField(default=True)
    tatil_kari_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=UN_PENSION)

    nobat_kari_use_tax = models.BooleanField(default=True)
    nobat_kari_use_insurance = models.BooleanField(default=True)
    nobat_kari_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=UN_PENSION)

    haghe_maamooriat_use_tax = models.BooleanField(default=True)
    haghe_maamooriat_use_insurance = models.BooleanField(default=True)
    haghe_maamooriat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=UN_PENSION)

    haghe_sanavat_use_tax = models.BooleanField(default=True)
    haghe_sanavat_use_insurance = models.BooleanField(default=True)

    eydi_padash_use_tax = models.BooleanField(default=True)
    eydi_padash_use_insurance = models.BooleanField(default=True)

    maskan = models.BooleanField(default=False)
    otomobil = models.BooleanField(default=False)
    include_made_86 = models.BooleanField(default=False)

    def __str__(self):
        if self.contract:
            return ' حکم کارگزینی ' + self.contract.workshop_personnel_display
        else:
            return 'قالب حکم کارگزینی ' + self.name


    class Meta(BaseModel.Meta):
        verbose_name = 'HRLetter'
        permission_basename = 'hr_letter'
        permissions = (
            ('get.hr_letter', 'مشاهده حکم کار گزینی'),
            ('create.hr_letter', 'تعریف حکم کار گزینی'),
            ('update.hr_letter', 'ویرایش حکم کار گزینی'),
            ('delete.hr_letter', 'حذف حکم کار گزینی'),

            ('getOwn.hr_letter', 'مشاهده حکم کار گزینی خود'),
            ('updateOwn.hr_letter', 'ویرایش حکم کار گزینی خود'),
            ('deleteOwn.hr_letter', 'حذف حکم کار گزینی خود'),
        )

    @property
    def get_hr_items(self):

        hr_letter_items = []

        hr_letter_items.append({
            'insurance': self.hoghooghe_roozane_use_insurance,
            'nature': self.hoghooghe_roozane_nature,
            'base': self.hoghooghe_roozane_base,
            'amount': self.hoghooghe_roozane_amount
        })
        hr_letter_items.append({
            'insurance': self.paye_sanavat_use_insurance,
            'nature': self.paye_sanavat_nature,
            'base': self.paye_sanavat_base,
            'amount': self.paye_sanavat_amount
        })
        hr_letter_items.append({
            'insurance': self.haghe_sarparasti_use_insurance,
            'nature': self.haghe_sarparasti_nature,
            'base': self.haghe_sarparasti_base,
            'amount': self.haghe_sarparasti_amount
        })
        hr_letter_items.append({
            'insurance': self.haghe_modiriyat_use_insurance,
            'nature': self.haghe_modiriyat_nature,
            'base': self.haghe_modiriyat_base,
            'amount': self.haghe_modiriyat_amount
        })
        hr_letter_items.append({
            'insurance': self.haghe_jazb_use_insurance,
            'nature': self.haghe_jazb_nature,
            'base': self.haghe_jazb_base,
            'amount': self.haghe_jazb_amount
        })
        hr_letter_items.append({
            'insurance': self.fogholade_shoghl_use_insurance,
            'nature': self.fogholade_shoghl_nature,
            'base': self.fogholade_shoghl_base,
            'amount': self.fogholade_shoghl_amount
        })
        hr_letter_items.append({
            'insurance': self.haghe_tahsilat_use_insurance,
            'nature': self.haghe_tahsilat_nature,
            'base': self.haghe_tahsilat_base,
            'amount': self.haghe_tahsilat_amount
        })
        hr_letter_items.append({
            'insurance': self.fogholade_sakhti_kar_use_insurance,
            'nature': self.fogholade_sakhti_kar_nature,
             'base': self.fogholade_sakhti_kar_base,
            'amount': self.fogholade_sakhti_kar_amount
        })
        hr_letter_items.append({
            'insurance': self.haghe_ankal_use_insurance,
            'nature': self.haghe_ankal_nature,
            'base': self.haghe_ankal_base,
            'amount': self.haghe_ankal_amount
        })
        hr_letter_items.append({
            'insurance': self.fogholade_badi_abohava_use_insurance,
            'nature': self.fogholade_badi_abohava_nature,
            'base': self.fogholade_badi_abohava_base,
            'amount': self.fogholade_badi_abohava_amount
        })
        hr_letter_items.append({
            'insurance': self.mahroomiat_tashilat_zendegi_use_insurance,
            'nature': self.mahroomiat_tashilat_zendegi_nature,
            'base': self.mahroomiat_tashilat_zendegi_base,
            'amount': self.mahroomiat_tashilat_zendegi_amount
        })
        hr_letter_items.append({
            'insurance': self.fogholade_mahal_khedmat_use_insurance,
            'nature': self.fogholade_mahal_khedmat_nature,
            'base': self.fogholade_mahal_khedmat_base,
            'amount': self.fogholade_mahal_khedmat_amount
        })
        hr_letter_items.append({
            'insurance': self.fogholade_sharayet_mohit_kar_use_insurance,
            'nature': self.fogholade_sharayet_mohit_kar_nature,
            'base': self.fogholade_sharayet_mohit_kar_base,
            'amount': self.fogholade_sharayet_mohit_kar_amount
        })
        hr_letter_items.append({
            'insurance': self.haghe_maskan_use_insurance,
            'nature': self.haghe_maskan_nature,
             'base': self.haghe_maskan_base,
            'amount': self.haghe_maskan_base
        })
        hr_letter_items.append({
            'insurance': self.ayabo_zahab_use_insurance,
            'nature': self.ayabo_zahab_nature,
            'base': self.ayabo_zahab_base,
            'amount': self.ayabo_zahab_amount
        })
        hr_letter_items.append({
            'insurance': self.bon_kharo_bar_use_insurance,
            'nature': self.bon_kharo_bar_nature,
            'base': self.bon_kharo_bar_base,
            'amount': self.bon_kharo_bar_amount
        })
        hr_letter_items.append({
            'insurance': self.yarane_ghaza_use_insurance,
            'nature': self.yarane_ghaza_nature,
            'base': self.yarane_ghaza_base,
            'amount': self.yarane_ghaza_amount
        })
        hr_letter_items.append({
            'insurance': self.haghe_shir_use_insurance,
            'nature': self.haghe_shir_nature,
            'base': self.haghe_shir_base,
            'amount': self.haghe_shir_amount
        })
        hr_letter_items.append({
            'insurance': self.haghe_taahol_use_insurance,
            'nature': self.haghe_taahol_nature,
            'base': self.haghe_taahol_base,
            'amount': self.haghe_taahol_amount
        })
        hr_letter_items.append({
            'insurance': self.komakhazine_mahdekoodak_use_insurance,
            'nature': self.komakhazine_mahdekoodak_nature,
            'base': self.komakhazine_mahdekoodak_base,
            'amount': self.komakhazine_mahdekoodak_amount
        })
        hr_letter_items.append({
            'insurance': self.komakhazine_varzesh_use_insurance,
            'nature': self.komakhazine_varzesh_nature,
            'base': self.komakhazine_varzesh_base,
            'amount': self.komakhazine_varzesh_amount
        })
        hr_letter_items.append({
            'insurance': self.komakhazine_mobile_use_insurance,
            'nature': self.komakhazine_mobile_nature,
            'base': self.komakhazine_mobile_base,
            'amount': self.komakhazine_mobile_amount
        })
        hr_letter_items.append({
            'insurance': self.mazaya_mostamar_gheyre_naghdi_use_insurance,
            'nature': self.mazaya_mostamar_gheyre_naghdi_nature,
            'base': self.mazaya_mostamar_gheyre_naghdi_base,
            'amount': self.mazaya_mostamar_gheyre_naghdi_amount
        })

        return hr_letter_items

    @property
    def calculate_pay_bases(self):
        daily, monthly = 0, 0
        hr_letter_items = self.get_hr_items
        for i in range(0, 23):
            if hr_letter_items[i]['base'] and hr_letter_items[i]['amount']:
                if i < 2:
                    daily += round(hr_letter_items[i]['amount'])
                    monthly += round(hr_letter_items[i]['amount'] * 30)
                else:
                    daily += round(hr_letter_items[i]['amount'] / 30)
                    monthly += round(hr_letter_items[i]['amount'])
        month_hourly = monthly / 220
        day_hourly = daily / 7.33
        return daily, monthly, day_hourly, month_hourly


    @property
    def calculate_save_leave_base(self):
        daily = 0
        hr_letter_items = self.get_hr_items
        for i in range(0, 23):
            if hr_letter_items[i]['amount']:
                if i < 2:
                    daily += round(hr_letter_items[i]['amount'])
                else:
                    daily += round(hr_letter_items[i]['amount'] / 30)
        return daily


    @property
    def calculate_insurance_pay_base(self):
        insurance_pay_base = 0
        hr_letter_items = self.get_hr_items
        for i in range(0, 22):
            if hr_letter_items[i]['insurance'] and hr_letter_items[i]['nature'] == 'b':
                if i < 2:
                    insurance_pay_base += round(hr_letter_items[i]['amount'])
                else:
                    insurance_pay_base += round(hr_letter_items[i]['amount'] / 30)
        print('base ' , insurance_pay_base)
        return insurance_pay_base

    @property
    def calculate_insurance_benefit(self):
        insurance_benefit = 0
        hr_letter_items = self.get_hr_items
        for i in range(0, 22):
            if hr_letter_items[i]['insurance'] and hr_letter_items[i]['nature'] != 'b':
                if i < 2:
                    insurance_benefit += round(hr_letter_items[i]['amount'] * 30)
                else:
                    insurance_benefit += round(hr_letter_items[i]['amount'])
        print('benifit ', insurance_benefit)

        return insurance_benefit

    @property
    def calculate_insurance_not_included(self):
        insurance_not_included = 0
        hr_letter_items = self.get_hr_items
        for i in range(0, 22):
            if not hr_letter_items[i]['insurance']:
                if i < 2:
                    insurance_not_included += round(hr_letter_items[i]['amount'] * 30)
                else:
                    insurance_not_included += round(hr_letter_items[i]['amount'])
        return insurance_not_included

    def save(self, *args, **kwargs):
        if self.pay_done:
            raise ValidationError(message='حکم غیرقابل تفییر است')

        self.daily_pay_base, self.monthly_pay_base, self.day_hourly_pay_base, self.month_hourly_pay_base =\
            self.calculate_pay_bases
        self.insurance_pay_day = self.calculate_insurance_pay_base
        self.insurance_benefit = self.calculate_insurance_benefit
        self.insurance_not_included = self.calculate_insurance_not_included
        if self.is_template == 't':
            self.contract, self.pay_done = None, False
            if not self.name:
                raise ValidationError(message='برای قالب حکم کارگزینی خود نام وارد کنید')
        else:
            if not self.contract:
                raise ValidationError(message='قرارداد را وارد کنید')
        super().save(*args, **kwargs)


class Mission(BaseModel, LockableMixin, DefinableMixin):
    HOURLY = 'h'
    DAILY = 'd'

    MISSION_TYPES = (
        (HOURLY, 'ساعتی'),
        (DAILY, 'روزانه'),

    )

    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name='mission', on_delete=models.CASCADE)
    mission_type = models.CharField(max_length=2, choices=MISSION_TYPES, default=DAILY)
    from_date = jmodels.jDateField(blank=True, null=True)
    to_date = jmodels.jDateField(blank=True, null=True)
    date = jmodels.jDateField(blank=True, null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    explanation = EXPLANATION()
    topic = EXPLANATION()
    is_in_payment = models.BooleanField(default=False)
    time_period = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=2)

    @property
    def final_by_day(self):
        if self.mission_type == 'h':
            duration = datetime.timedelta(hours=self.to_hour.hour - self.from_hour.hour,
                                            minutes=self.to_hour.minute - self.from_hour.minute)
            final_by_day = (duration.seconds / 60) / 440
        else:
            difference = self.to_date - self.from_date
            final_by_day = difference.days + 1
        return final_by_day

    class Meta(BaseModel.Meta):
        verbose_name = 'Mission'
        permission_basename = 'mission'
        permissions = (
            ('get.mission', 'مشاهده ماموریت'),
            ('create.mission', 'تعریف ماموریت'),
            ('update.mission', 'ویرایش ماموریت'),
            ('delete.mission', 'حذف ماموریت'),

            ('getOwn.mission', 'مشاهده ماموریت خود'),
            ('updateOwn.mission', 'ویرایش ماموریت خود'),
            ('deleteOwn.mission', 'حذف ماموریت خود'),
        )

    def save(self, *args, **kwargs):
        if self.mission_type == 'h':
            self.from_date, self.to_date, = None, None
            if not self.from_hour or not self.to_hour or not self.date:
                raise ValidationError('برای ماموریت ساعتی ساعت شروع و پایان و تاریخ را وارد کنید')
        else:
            self.date, self.from_hour, self.to_hour = None, None, None
            if not self.from_date or not self.to_date:
                raise ValidationError('برای ماموریت روزانه تاریح شروع و پایان را وارد کنید')
        self.time_period = self.final_by_day
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.time_period) + ' برای ' + self.workshop_personnel.personnel.full_name


class ListOfPay(BaseModel, LockableMixin, DefinableMixin):

    workshop = models.ForeignKey(Workshop, related_name="list_of_pay", on_delete=models.CASCADE,
                                 null=True, blank=True)
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    month_days = models.IntegerField(default=30)
    start_date = jmodels.jDateField()
    end_date = jmodels.jDateField()

    class Meta(BaseModel.Meta):
        verbose_name = 'ListOfPay'
        permission_basename = 'list_of_pay'
        permissions = (
            ('get.list_of_pay', 'مشاهده حقوق و دستمزد'),
            ('create.list_of_pay', 'تعریف حقوق و دستمزد'),
            ('update.list_of_pay', 'ویرایش حقوق و دستمزد'),
            ('delete.list_of_pay', 'حذف حقوق و دستمزد'),

            ('getOwn.list_of_pay', 'مشاهده حقوق و دستمزد خود'),
            ('updateOwn.list_of_pay', 'ویرایش حقوق و دستمزد خود'),
            ('deleteOwn.list_of_pay', 'حذف حقوق و دستمزد خود'),
        )

    @property
    def get_contracts(self):
        contracts = []
        workshop_personnel = WorkshopPersonnel.objects.filter(workshop=self.workshop)
        workshop_contracts = Contract.objects.filter(workshop_personnel__in=workshop_personnel)
        for contract in workshop_contracts:
            if not contract.quit_job_date:
                end = contract.contract_to_date
            else:
                end = contract.quit_job_date
            if contract.contract_from_date.__le__(self.start_date) and end.__ge__(self.end_date):
                contracts.append(contract.id)
            if contract.contract_from_date.__ge__(self.start_date) and end.__le__(self.end_date):
                contracts.append(contract.id)
            if contract.contract_from_date.__le__(self.start_date) and end.__gt__(self.start_date) and \
                    end.__lt__(self.end_date):
                contracts.append(contract.id)
            if contract.contract_from_date.__ge__(self.start_date) and end.__ge__(self.end_date) and \
                    contract.contract_from_date.__lt__(self.end_date):
                contracts.append(contract.id)

        filtered_contracts = Contract.objects.filter(pk__in=contracts)
        return filtered_contracts

    @property
    def data_for_insurance(self):
        contracts = self.get_contracts
        personnel_count = []
        items = self.list_of_pay_item
        items_data = []
        for item in items.all():
            items_data.append(item.data_for_insurance)
        total_worktime = 0
        total_day_pay = 0
        total_month_pay = 0
        total_benefit = 0
        total_base = 0
        total_insurance = 0
        for item in items_data:
            total_worktime += item['DSW_ROOZ']
            total_day_pay += item['DSW_ROOZ']
            total_month_pay += item['DSW_MAH']
            total_benefit += item['DSW_MAZ']
            total_base += item['DSW_TOTL']
            total_insurance += item['DSW_BIME']
        for contract in contracts:
            if contract.workshop_personnel.personnel.id not in personnel_count:
                personnel_count.append(contract.workshop_personnel.personnel.id)
        DSKKAR = {
            'DSK_ID': str(self.workshop.code),
            'DSK_NAME': self.workshop.name,
            'DSK_FARM': self.workshop.employer_name,
            'DSK_ADRS': self.workshop.address[:100],
            'DSK_KIND': 0,
            'DSK_YY': int(str(self.year)[2:]),
            'DSK_MM': self.month,
            'DSK_LISTNO': '0000',
            'DSK_DISC': '',
            'DSK_NUM': len(personnel_count),
            'DSK_TDD': total_worktime,
            'DSK_TROOZ': total_day_pay,
            'DSK_TMAH': total_month_pay,
            'DSK_TMAZ': total_benefit,
            'DSK_TMASH': total_benefit + total_month_pay,
            'DSK_TTOTL': total_base,
            'DSK_TBIME': total_insurance,
            'DSK_TKOSO': round((total_benefit + total_month_pay) * self.workshop.employee_insurance_nerkh),
            'DSK_TBIC': round((total_benefit + total_month_pay) * self.workshop.unemployed_insurance_nerkh),
            'DSK_RATE': self.workshop.employer_insurance_contribution,
            'DSK_PRATE': 0,
            'DSK_BIMH': 0,
            'DSK_PYM': '000',
        }
        return DSKKAR, items_data

    def personnel_insurance_worktime(self, pk):
        workshop_contracts = self.get_contracts
        insurance_worktime = 0
        for contract in workshop_contracts:
            insurance_start = contract.insurance_add_date
            if contract.workshop_personnel.personnel.id == pk and contract.insurance:
                if not contract.quit_job_date:
                    end = contract.contract_to_date
                else:
                    end = contract.quit_job_date
                if insurance_start.__le__(self.start_date) and end.__ge__(self.end_date):
                    insurance_worktime += self.month_days
                if insurance_start.__ge__(self.start_date) and end.__le__(self.end_date):
                    insurance_worktime += end.day - insurance_start.day
                if insurance_start.__le__(self.start_date) and end.__gt__(self.start_date) and \
                        end.__lt__(self.end_date):
                    insurance_worktime += end.day
                if insurance_start.__ge__(self.start_date) and end.__ge__(self.end_date) and \
                        insurance_start.__lt__(self.end_date):
                    insurance_worktime += self.month_days - insurance_start.day + 1
        return insurance_worktime

    @property
    def info_for_items(self):
        personnel_normal_worktime = {}
        contract_start = {}
        contract_end = {}
        filtered_contracts = self.get_contracts
        for contract in filtered_contracts:
            if contract.workshop_personnel.personnel.is_personnel_active:
                if not contract.quit_job_date:
                    end = contract.contract_to_date
                else:
                    end = contract.quit_job_date
                if contract.contract_from_date.__le__(self.start_date) and end.__ge__(self.end_date):
                    personnel_normal_worktime[contract.id] = self.month_days
                    contract_start[contract.id] = self.start_date
                    contract_end[contract.id] = self.end_date
                if contract.contract_from_date.__ge__(self.start_date) and end.__le__(self.end_date):
                    personnel_normal_worktime[contract.id] = end.day - contract.contract_from_date.day
                    contract_start[contract.id] = contract.contract_from_date
                    contract_end[contract.id] = end
                if contract.contract_from_date.__le__(self.start_date) and end.__gt__(self.start_date) and \
                        end.__lt__(self.end_date):
                    personnel_normal_worktime[contract.id] = end.day
                    contract_start[contract.id] = self.start_date
                    contract_end[contract.id] = end
                if contract.contract_from_date.__ge__(self.start_date) and end.__ge__(self.end_date) and \
                        contract.contract_from_date.__lt__(self.end_date):
                    personnel_normal_worktime[contract.id] = self.month_days - contract.contract_from_date.day + 1
                    contract_start[contract.id] = contract.contract_from_date
                    contract_end[contract.id] = self.end_date
        contract_personnel = {}
        for contract in filtered_contracts:
            contract_personnel[contract.id] = contract.workshop_personnel.personnel.id
        response_data = []
        for contract in contract_personnel:
            absence_types = {'i': 0, 'w': 0, 'a': 0, 'e': 0, 'm': 0, 'eh': 0, 'ed': 0}
            mission_day = 0
            contract = Contract.objects.get(pk=contract)
            workshop_personnel = contract.workshop_personnel
            is_insurance = contract.insurance
            filtered_absence = LeaveOrAbsence.objects.filter(workshop_personnel=workshop_personnel)
            filtered_mission = Mission.objects.filter(workshop_personnel=workshop_personnel)

            for absence in filtered_absence.all():
                if absence.workshop_personnel == workshop_personnel:
                    if absence.leave_type == 'e' and absence.entitlement_leave_type == 'h' and\
                            absence.date.__ge__(contract_start[contract.id]) and absence.date.__le__(contract_end[contract.id]):
                        absence_types['eh'] += absence.to_hour.hour - absence.from_hour.hour
                    if absence.leave_type == 'e' and absence.entitlement_leave_type == 'd':
                        if absence.from_date.__ge__(contract_start[contract.id]) and absence.to_date.__le__(contract_end[contract.id]):
                            absence_types['ed'] += absence.time_period
                        elif absence.from_date.__lt__(contract_start[contract.id]) and absence.to_date.__le__(contract_end[contract.id]) and \
                                absence.to_date.__gt__(contract_start[contract.id]):
                            absence_types['ed'] += absence.to_date.day
                        elif absence.from_date.__gt__(contract_start[contract.id]) and absence.to_date.__gt__(contract_end[contract.id]) and \
                                absence.from_date.__le__(contract_end[contract.id]):
                            absence_types['ed'] += contract_end[contract.id].day - absence.from_date.day
                        elif absence.from_date.__le__(contract_start[contract.id]) and absence.to_date.__ge__(contract_end[contract.id]):
                            absence_types['ed'] += contract_end[contract.id].day - contract_start[contract.id].day
                    if absence.from_date.__ge__(contract_start[contract.id]) and absence.to_date.__le__(contract_end[contract.id]):
                        absence_types[absence.leave_type] += absence.time_period
                    elif absence.from_date.__lt__(contract_start[contract.id]) and absence.to_date.__le__(contract_end[contract.id]) and \
                            absence.to_date.__gt__(contract_start[contract.id]):
                        absence_types[absence.leave_type] += absence.to_date.day
                    elif absence.from_date.__gt__(contract_start[contract.id]) and absence.to_date.__gt__(contract_end[contract.id]) and \
                            absence.from_date.__le__(contract_end[contract.id]):
                        absence_types[absence.leave_type] += contract_end[contract.id].day - absence.from_date.day + 1
                    elif absence.from_date.__le__(contract_start[contract.id]) and absence.to_date.__ge__(contract_end[contract.id]):
                        absence_types[absence.leave_type] += contract_end[contract.id].day - contract_start[contract.id].day
                    absence_types['e'] = absence_types['ed'] + Decimal(round(absence_types['eh'] / 7.33, 2))

            for mission in filtered_mission.all():
                if mission.workshop_personnel.personnel == workshop_personnel.personnel and mission.mission_type != 'h'\
                        and mission.is_in_payment:
                    if mission.from_date.__ge__(contract_start[contract.id]) and mission.to_date.__le__(contract_end[contract.id]):
                        mission_day += mission.time_period
                    elif mission.from_date.__lt__(contract_start[contract.id]) and mission.to_date.__le__(contract_end[contract.id]) and \
                            mission.to_date.__gt__(contract_start[contract.id]):
                        mission_day += mission.to_date.day
                    elif mission.from_date.__gt__(contract_start[contract.id]) and mission.to_date.__gt__(contract_end[contract.id]) and \
                            mission.from_date.__le__(contract_end[contract.id]):
                        mission_day += contract_end[contract.id].day - mission.from_date.day
                    elif mission.from_date.__le__(contract_start[contract.id]) and mission.to_date.__ge__(contract_end[contract.id]):
                        mission_day += contract_end[contract.id].day - contract_start[contract.id].day

            normal = personnel_normal_worktime[contract.id]
            real_work = normal - absence_types['a'] - int(absence_types['i']) - int(absence_types['w'])
            response_data.append(
                {
                    'pk': workshop_personnel.personnel.id,
                    'leaves': absence_types,
                    'name': workshop_personnel.personnel.name + ' ' + workshop_personnel.personnel.last_name,
                    'normal_work': normal,
                    'real_work': real_work,
                    'mission': mission_day,
                    'insurance': is_insurance,
                    'contract': contract.id,
                }
            )
        return response_data

    def __str__(self):
        return 'حقوق و دستمزد ' + ' ' + str(self.year) + '/' + str(self.month) + ' کارگاه ' +\
               self.workshop.workshop_title


class ListOfPayItem(BaseModel, LockableMixin, DefinableMixin):
    YES = 'y'
    NO = 'n'

    INCURANCE_TYPES = (
        (YES, 'بله'),
        (NO, 'خیر'),
    )

    list_of_pay = models.ForeignKey(ListOfPay, related_name="list_of_pay_item", on_delete=models.CASCADE,
                                     blank=True, null=True)
    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name="list_of_pay_item",
                                           on_delete=models.CASCADE, blank=True, null=True)
    contract = models.ForeignKey(Contract, related_name="list_of_pay_item",
                                           on_delete=models.CASCADE, blank=True, null=True)
    contract_row = models.ForeignKey(ContractRow, related_name="list_of_pay_item", on_delete=models.CASCADE,
                                     blank=True, null=True)
    hoghoogh_roozane = DECIMAL()
    pay_base = models.IntegerField(default=0)
    sanavat_base = DECIMAL(default=0)
    sanavat_month = models.IntegerField(default=0)
    aele_mandi_child = models.IntegerField(default=0)
    total_insurance_month = models.IntegerField(default=0)
    is_insurance = models.CharField(max_length=2, choices=INCURANCE_TYPES, default=NO)
    hourly_pay_base = models.IntegerField(default=0)
    normal_worktime = models.IntegerField(default=0)
    entitlement_leave_day = models.DecimalField(max_digits=24, decimal_places=2, default=0)
    matter_47_leave_day = models.DecimalField(max_digits=24, decimal_places=2, default=0)
    daily_entitlement_leave_day = models.IntegerField(default=0)
    hourly_entitlement_leave_day = models.IntegerField(default=0)
    absence_day = models.IntegerField(default=0)
    illness_leave_day = models.IntegerField(default=0)
    without_salary_leave_day = models.IntegerField(default=0)
    mission_day = models.IntegerField(default=0)
    real_worktime = models.IntegerField(default=0)

    mission_amount = DECIMAL(default=0, blank=True, null=True)
    mission_nerkh = models.DecimalField(max_digits=24, default=1, decimal_places=2)

    ezafe_kari = models.DecimalField(default=0, max_digits=24, decimal_places=2)
    ezafe_kari_amount = DECIMAL(default=0)
    ezafe_kari_nerkh = models.DecimalField(max_digits=24, default=1.96, decimal_places=2)
    ezafe_kari_total = models.IntegerField(default=0)

    tatil_kari = models.DecimalField(default=0, max_digits=24, decimal_places=2)
    tatil_kari_amount = DECIMAL(default=0)
    tatil_kari_nerkh = models.DecimalField(max_digits=24, default=1.96, decimal_places=2)
    tatil_kari_total = models.IntegerField(default=0)


    kasre_kar = models.DecimalField(default=0, max_digits=24, decimal_places=2)
    kasre_kar_amount = DECIMAL(default=0)
    kasre_kar_nerkh = models.DecimalField(max_digits=24, default=1.4, decimal_places=2)
    kasre_kar_total = models.IntegerField(default=0)


    shab_kari = models.DecimalField(default=0, max_digits=24, decimal_places=2)
    shab_kari_amount = DECIMAL(default=0)
    shab_kari_nerkh = models.DecimalField(max_digits=24, default=0.35, decimal_places=2)
    shab_kari_total = models.IntegerField(default=0)


    nobat_kari_sob_asr = models.IntegerField(default=0)
    nobat_kari_sob_asr_amount = DECIMAL(default=0)
    nobat_kari_sob_asr_nerkh = models.DecimalField(max_digits=24, default=0.1, decimal_places=2)


    nobat_kari_sob_shab = models.IntegerField(default=0)
    nobat_kari_sob_shab_amount = DECIMAL(default=0)
    nobat_kari_sob_shab_nerkh = models.DecimalField(max_digits=24, default=0.225, decimal_places=2)


    nobat_kari_asr_shab = models.IntegerField(default=0)
    nobat_kari_asr_shab_amount = DECIMAL(default=0)
    nobat_kari_asr_shab_nerkh = models.DecimalField(max_digits=24, default=0.025, decimal_places=2)


    nobat_kari_sob_asr_shab = models.IntegerField(default=0)
    nobat_kari_sob_asr_shab_amount = DECIMAL(default=0)
    nobat_kari_sob_asr_shab_nerkh = models.DecimalField(max_digits=24, default=0.15, decimal_places=2)


    aele_mandi_amount = DECIMAL(default=0)
    aele_mandi_nerkh = models.DecimalField(max_digits=24, default=3, decimal_places=2)
    aele_mandi = models.IntegerField(default=0)

    sayer_ezafat = DECIMAL(default=0)
    mazaya_gheyr_mostamar = DECIMAL(default=0)
    calculate_payment = models.BooleanField(default=False)

    #tax kosoorat
    hazine_made_137 = models.IntegerField(default=0)
    kosoorat_insurance = models.IntegerField(default=0)
    sayer_moafiat = models.IntegerField(default=0)
    manategh_tejari_moafiat = models.IntegerField(default=0)
    ejtenab_maliat_mozaaf = models.IntegerField(default=0)
    naghdi_gheye_naghdi_tax = models.IntegerField(default=0)

    total_payment = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        verbose_name = 'ListOfPayItem'
        permission_basename = 'list_of_pay_item'
        permissions = (
            ('get.list_of_pay_item', 'مشاهده آیتم های حقوق و دستمزد'),
            ('create.list_of_pay_item', 'تعریف آیتم های حقوق و دستمزد'),
            ('update.list_of_pay_item', 'ویرایش آیتم های حقوق و دستمزد'),
            ('delete.list_of_pay_item', 'حذف آیتم های حقوق و دستمزد'),

            ('getOwn.list_of_pay_item', 'مشاهده آیتم های حقوق و دستمزد خود'),
            ('updateOwn.list_of_pay_item', 'ویرایش آیتم های حقوق و دستمزد خود'),
            ('deleteOwn.list_of_pay_item', 'حذف آیتم های حقوق و دستمزد خود'),
        )

    @property
    def get_hr_letter(self):
        try:
            return self.contract.hr_letter.first()
        except AttributeError:
            raise ValidationError('حکم کارگزینی ثبت نشده')


    @property
    def tax_included_payment(self):
        hr = self.get_hr_letter
        total = Decimal(0)
        if hr.hoghooghe_roozane_use_tax:
            total += self.hoghoogh_roozane * Decimal(self.real_worktime)
        if hr.paye_sanavat_use_tax and self.sanavat_month >= 12:
            total += self.sanavat_base * Decimal(self.real_worktime)
        if hr.haghe_owlad_use_tax:
            total += self.aele_mandi
        if hr.ezafe_kari_use_tax:
            total += self.ezafe_kari_amount * Decimal(self.ezafe_kari_nerkh) * Decimal(self.ezafe_kari)
        if hr.tatil_kari_use_tax:
            total += self.tatil_kari_amount * Decimal(self.tatil_kari_nerkh) * Decimal(self.tatil_kari)
        if hr.shab_kari_use_tax:
            total += self.shab_kari * Decimal(self.shab_kari_nerkh) * Decimal(self.shab_kari_amount)
        total -= self.kasre_kar_amount * Decimal(self.kasre_kar_nerkh) * Decimal(self.kasre_kar)
        if hr.haghe_maamooriat_use_tax:
            total += Decimal(self.mission_day) * self.mission_nerkh * self.mission_amount
        if hr.nobat_kari_use_tax:
            total += Decimal(self.nobat_kari_sob_asr) * self.nobat_kari_sob_asr_nerkh * self.nobat_kari_sob_asr_amount
            total += Decimal(self.nobat_kari_sob_shab) * self.nobat_kari_sob_shab_nerkh * self.nobat_kari_sob_shab_amount
            total += Decimal(self.nobat_kari_asr_shab) * self.nobat_kari_asr_shab_nerkh * self.nobat_kari_asr_shab_amount
            total += Decimal(self.nobat_kari_sob_asr_shab) * self.nobat_kari_sob_asr_shab_nerkh * \
                    self.nobat_kari_sob_asr_shab_amount
        if hr.haghe_sarparasti_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_sarparasti_amount)
        if hr.haghe_modiriyat_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_modiriyat_amount)
        if hr.haghe_jazb_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_jazb_amount)
        if hr.fogholade_shoghl_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_shoghl_amount)
        if hr.haghe_tahsilat_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_tahsilat_amount)
        if hr.fogholade_sakhti_kar_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_sakhti_kar_amount)
        if hr.haghe_ankal_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_ankal_amount)
        if hr.fogholade_badi_abohava_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_badi_abohava_amount)
        if hr.mahroomiat_tashilat_zendegi_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.mahroomiat_tashilat_zendegi_amount)
        if hr.fogholade_mahal_khedmat_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_mahal_khedmat_amount)
        if hr.fogholade_sharayet_mohit_kar_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_sharayet_mohit_kar_amount)
        if hr.haghe_maskan_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_maskan_amount)
        if hr.ayabo_zahab_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.ayabo_zahab_amount)
        if hr.bon_kharo_bar_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.bon_kharo_bar_amount)
        if hr.yarane_ghaza_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.yarane_ghaza_amount)
        if hr.haghe_shir_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_shir_amount)
        if hr.haghe_taahol_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_taahol_amount)
        if hr.komakhazine_mahdekoodak_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_mahdekoodak_amount)
        if hr.komakhazine_varzesh_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_varzesh_amount)
        if hr.komakhazine_mobile_use_tax:
            total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_mobile_amount)

        return round(total)

    @property
    def tax_included_naghdi_payment(self):
        total = self.tax_included_payment
        total -= self.tax_moafiat['hazine_made_137']
        total -= self.tax_moafiat['tamin_ejemae']
        total -= self.tax_moafiat['hagh_made_137']
        total -= self.tax_moafiat['sayer_moafiat']
        total -= self.tax_moafiat['sayer_gheyre_mostamar_naghdi']
        if self.tax_moafiat['mande_moafiat_mazaya_gheyre_naghdi'] < 0:
            total += self.tax_moafiat['mande_moafiat_mazaya_gheyre_naghdi']
        total -= self.tax_moafiat['band_10_made_91']
        total -= self.tax_moafiat['band_5_made_91']
        total -= self.tax_moafiat['manategh_tejari_moafiat']
        total -= self.tax_moafiat['ejtenab_maliat_mozaaf']
        total -= self.tax_moafiat['naghdi_gheye_naghdi_tax']

        return total

    @property
    def tax_included_ghyer_naghdi_payment(self):
        if self.tax_moafiat['mande_moafiat_mazaya_gheyre_naghdi'] < 0:
            total = - self.tax_moafiat['mande_moafiat_mazaya_gheyre_naghdi']
        else:
            total = 0
        return total


    @property
    def pension_payment(self):
        hr = self.get_hr_letter
        total = Decimal(0)
        if hr.haghe_owlad_nature == 'p':
            total += self.aele_mandi
        if hr.hoghooghe_roozane_nature == 'p':
            total += self.hoghoogh_roozane * Decimal(self.real_worktime)
        if hr.paye_sanavat_nature == 'p' and self.sanavat_month >= 12:
            total += self.sanavat_base * Decimal(self.real_worktime)
        if hr.haghe_sarparasti_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_sarparasti_amount)
        if hr.haghe_modiriyat_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_modiriyat_amount)
        if hr.haghe_jazb_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_jazb_amount)
        if hr.fogholade_shoghl_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_shoghl_amount)
        if hr.haghe_tahsilat_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_tahsilat_amount)
        if hr.fogholade_sakhti_kar_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_sakhti_kar_amount)
        if hr.haghe_ankal_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_ankal_amount)
        if hr.fogholade_badi_abohava_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_badi_abohava_amount)
        if hr.mahroomiat_tashilat_zendegi_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.mahroomiat_tashilat_zendegi_amount)
        if hr.fogholade_mahal_khedmat_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_mahal_khedmat_amount)
        if hr.fogholade_sharayet_mohit_kar_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_sharayet_mohit_kar_amount)
        if hr.haghe_maskan_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_maskan_amount)
        if hr.ayabo_zahab_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.ayabo_zahab_amount)
        if hr.bon_kharo_bar_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.bon_kharo_bar_amount)
        if hr.yarane_ghaza_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.yarane_ghaza_amount)
        if hr.haghe_shir_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_shir_amount)
        if hr.haghe_taahol_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_taahol_amount)
        if hr.komakhazine_mahdekoodak_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_mahdekoodak_amount)
        if hr.komakhazine_varzesh_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_varzesh_amount)
        if hr.komakhazine_mobile_nature == 'p':
            total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_mobile_amount)
        total += hr.mazaya_mostamar_gheyre_naghdi_amount
        return total


    @property
    def un_pension_payment(self):
        hr = self.get_hr_letter
        total = Decimal(0)
        if hr.hoghooghe_roozane_nature == 'u':
            total += self.hoghoogh_roozane * Decimal(self.real_worktime)
        if hr.paye_sanavat_nature == 'u' and self.sanavat_month >= 12:
            total += self.sanavat_base * Decimal(self.real_worktime)
        if hr.haghe_owlad_nature == 'u':
            total += self.aele_mandi
        total += self.ezafe_kari_amount * Decimal(self.ezafe_kari_nerkh) * Decimal(self.ezafe_kari)
        total += self.tatil_kari_amount * Decimal(self.tatil_kari_nerkh) * Decimal(self.tatil_kari)
        total += self.shab_kari * Decimal(self.shab_kari_nerkh) * Decimal(self.shab_kari_amount)
        total += Decimal(self.mission_day) * self.mission_nerkh * self.mission_amount
        total += Decimal(self.nobat_kari_sob_asr) * self.nobat_kari_sob_asr_nerkh * self.nobat_kari_sob_asr_amount
        total += Decimal(self.nobat_kari_sob_shab) * self.nobat_kari_sob_shab_nerkh * self.nobat_kari_sob_shab_amount
        total += Decimal(self.nobat_kari_asr_shab) * self.nobat_kari_asr_shab_nerkh * self.nobat_kari_asr_shab_amount
        total += Decimal(self.nobat_kari_sob_asr_shab) * self.nobat_kari_sob_asr_shab_nerkh * \
                 self.nobat_kari_sob_asr_shab_amount
        if hr.haghe_sarparasti_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_sarparasti_amount)
        if hr.haghe_modiriyat_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_modiriyat_amount)
        if hr.haghe_jazb_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_jazb_amount)
        if hr.fogholade_shoghl_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_shoghl_amount)
        if hr.haghe_tahsilat_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_tahsilat_amount)
        if hr.fogholade_sakhti_kar_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_sakhti_kar_amount)
        if hr.haghe_ankal_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_ankal_amount)
        if hr.fogholade_badi_abohava_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_badi_abohava_amount)
        if hr.mahroomiat_tashilat_zendegi_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.mahroomiat_tashilat_zendegi_amount)
        if hr.fogholade_mahal_khedmat_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_mahal_khedmat_amount)
        if hr.fogholade_sharayet_mohit_kar_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.fogholade_sharayet_mohit_kar_amount)
        if hr.haghe_maskan_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_maskan_amount)
        if hr.ayabo_zahab_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.ayabo_zahab_amount)
        if hr.bon_kharo_bar_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.bon_kharo_bar_amount)
        if hr.yarane_ghaza_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.yarane_ghaza_amount)
        if hr.haghe_shir_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_shir_amount)
        if hr.haghe_taahol_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.haghe_taahol_amount)
        if hr.komakhazine_mahdekoodak_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_mahdekoodak_amount)
        if hr.komakhazine_varzesh_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_varzesh_amount)
        if hr.komakhazine_mobile_nature == 'u':
            total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_mobile_amount)
        total += self.mazaya_gheyr_mostamar
        total += Decimal(self.sayer_ezafat)
        return total

    @property
    def tax_moafiat(self):
        hr = self.get_hr_letter
        year, month, month_day = self.list_of_pay.year, self.list_of_pay.month, self.list_of_pay.month_days
        tax = WorkshopTax.objects.first()
        tax_rows = WorkshopTaxRow.objects.filter(workshop_tax=tax)
        tax_row = tax_rows.get(from_amount=Decimal(0))

        response = {}
        response['hazine_made_137'] = self.hazine_made_137
        response['tamin_ejemae'] = self.data_for_insurance['DSW_BIME'] * self.workshop_personnel.workshop.tax_employer_type
        response['hagh_made_137'] = response['tamin_ejemae'] + round(self.kosoorat_insurance)
        response['sayer_moafiat'] = self.sayer_moafiat
        if not hr.haghe_maamooriat_use_tax:
            response['sayer_gheyre_mostamar_naghdi'] = round(self.mission_total)
        else:
            response['sayer_gheyre_mostamar_naghdi'] = 0
        moafiat = 2 / 12 * round(tax_row.to_amount) / 12
        response['mande_moafiat_mazaya_gheyre_naghdi'] = moafiat - round(self.mazaya_gheyr_mostamar) + \
                                                         round(hr.mazaya_mostamar_gheyre_naghdi_amount)
        response['band_10_made_91'] = 0
        response['band_5_made_91'] = 0
        if self.workshop_personnel.job_location_status == 'dp':
            job_loc_zarib = 0.5
        else:
            job_loc_zarib = 1
        response['job_location_status'] = job_loc_zarib
        response['manategh_tejari_moafiat'] = round(self.manategh_tejari_moafiat)
        response['ejtenab_maliat_mozaaf'] = round(self.ejtenab_maliat_mozaaf)
        response['naghdi_gheye_naghdi_tax'] = round(self.naghdi_gheye_naghdi_tax)
        return response

    @property
    def get_year_payment(self):
        items = ListOfPayItem.objects.filter(Q(list_of_pay__year=self.list_of_pay.year) &
                                             Q(list_of_pay__month__lt=self.list_of_pay.month) &
                                             Q(workshop_personnel=self.workshop_personnel)).all()
        year_payment = Decimal(0)
        for item in items:
            year_payment += item.tax_included_naghdi_payment
            year_payment += item.tax_included_ghyer_naghdi_payment
        return year_payment

    @property
    def get_last_tax(self):
        item = ListOfPayItem.objects.filter(Q(list_of_pay__year=self.list_of_pay.year) &
                                             Q(list_of_pay__month__lt=self.list_of_pay.month) &
                                             Q(workshop_personnel=self.workshop_personnel)).first()
        if item:
            return item.calculate_month_tax
        else:
            return 0
    @property
    def calculate_month_tax(self):
        hr = self.get_hr_letter
        if hr.include_made_86:
            tax = (self.tax_included_naghdi_payment + self.tax_included_ghyer_naghdi_payment) / 10
        else:
            tax = Decimal(0)
            year, month, month_day = self.list_of_pay.year, self.list_of_pay.month, self.list_of_pay.month_days
            year_amount = self.get_year_payment + self.tax_included_ghyer_naghdi_payment + self.tax_included_naghdi_payment
            mytax = WorkshopTax.objects.first()
            tax_rows = WorkshopTaxRow.objects.filter(workshop_tax=mytax)
            tax_row = tax_rows.get(from_amount=Decimal(0))
            start = 0
            while year_amount >= Decimal(0):
                if year_amount + start <= (tax_row.to_amount * Decimal(month) / Decimal(12)):
                    tax += (year_amount * tax_row.ratio / 100)
                    return round(tax) - round(self.get_last_tax)
                elif year_amount + start > (tax_row.to_amount * Decimal(month) / Decimal(12)):
                    tax += ((tax_row.to_amount * Decimal(month) / Decimal(12))
                            - (tax_row.from_amount * Decimal(month) / Decimal(12))) * tax_row.ratio / 100
                    year_amount -= ((tax_row.to_amount * Decimal(month) / Decimal(12)) -
                                    (tax_row.from_amount * Decimal(month) / Decimal(12)))
                    try:
                        tax_row = tax_rows.get(from_amount=tax_row.to_amount + Decimal(1))
                        start = tax_row.from_amount * Decimal(month) / Decimal(12)
                    except:
                        return round(tax) - round(self.get_last_tax)
        return round(tax) - round(self.get_last_tax)

    @property
    def get_tax_report(self):
        hr = self.get_hr_letter
        response = {}
        response['jame_nakhales_mostamar_naghdi'] = self.pension_payment -\
                                                    Decimal(hr.mazaya_mostamar_gheyre_naghdi_amount)
        response['nakhales_ezafe_kari'] = self.ezafe_kari_amount + self.tatil_kari_amount

        response['gheyre_mostamar_naghdi'] = self.un_pension_payment - self.mazaya_gheyr_mostamar - \
                                             response['nakhales_ezafe_kari']
        response['mazaya_mostamar_gheyre_naghdi'] = hr.mazaya_mostamar_gheyre_naghdi_amount
        response['mazaya_gheyre_mostamar_gheyre_naghdi'] = self.mazaya_gheyr_mostamar
        return response

    @property
    def haghe_bime_bime_shavande(self):
        hr = self.get_hr_letter
        response = round((hr.insurance_benefit + hr.insurance_pay_day) *
              self.workshop_personnel.workshop.employee_insurance_nerkh )
        return response


    @property
    def data_for_insurance(self):
        hr = self.get_hr_letter
        contracts = self.list_of_pay.get_contracts
        contract = contracts.filter(workshop_personnel=self.workshop_personnel).last()
        if contract.quit_job_date:
            quit_job_date = contract.quit_job_date.__str__().replace('-', '')
        else:
            quit_job_date = '000000'
        DSKWOR = {
            'DSW_ID': str(self.workshop_personnel.workshop.code),
            'DSW_YY': int(str(self.list_of_pay.year)[2:]),
            'DSW_MM': self.list_of_pay.month,
            'DSW_LISTNO': '0',
            'DSW_ID1': str(self.workshop_personnel.personnel.insurance_code),
            'DSW_FNAME': self.workshop_personnel.personnel.name,
            'DSW_LNAME': self.workshop_personnel.personnel.last_name,
            'DSW_DNAME': self.workshop_personnel.personnel.father_name,
            'DSW_IDNO': str(self.workshop_personnel.personnel.identity_code),
            'DSW_IDPLC': str(self.workshop_personnel.personnel.location_of_exportation),
            'DSW_IDATE': self.workshop_personnel.personnel.date_of_exportation.__str__().replace('-', ''),
            'DSW_BDATE': self.workshop_personnel.personnel.location_of_birth.__str__().replace('-', ''),
            'DSW_SEX': self.workshop_personnel.personnel.get_gender_display(),
            'DSW_NAT': self.workshop_personnel.personnel.get_nationality_display(),
            'DSW_OCP': self.workshop_personnel.work_title,
            'DSW_SDATE': contract.insurance_add_date.__str__().replace('-', ''),
            'DSW_EDATE': quit_job_date,
            'DSW_DD': self.list_of_pay.personnel_insurance_worktime(self.workshop_personnel.personnel.id),
            'DSW_ROOZ': hr.insurance_pay_day,
            'DSW_MAH': hr.insurance_pay_day *
                        self.list_of_pay.personnel_insurance_worktime(self.workshop_personnel.personnel.id),
            'DSW_MAZ': hr.insurance_benefit,
            'DSW_MASH': hr.insurance_benefit + hr.insurance_pay_day *
                       self.list_of_pay.personnel_insurance_worktime(self.workshop_personnel.personnel.id),
            'DSW_TOTL': hr.insurance_benefit + hr.insurance_not_included + hr.insurance_pay_day *
                       self.list_of_pay.personnel_insurance_worktime(self.workshop_personnel.personnel.id),
            'DSW_BIME': self.haghe_bime_bime_shavande,
            'DSW_PRATE': 0,
            'DSW_JOB': 0,
            'PER_NATCOD': str(self.workshop_personnel.personnel.national_code),

        }
        return DSKWOR

    @property
    def hoghoogh_mahane(self):
        return round(self.hoghoogh_roozane * self.real_worktime, 2)

    @property
    def sanavat_mahane(self):
        return round(self.sanavat_base * self.real_worktime, 2)

    @property
    def mission_total(self):
        return round(Decimal(self.mission_day) * self.mission_nerkh * self.mission_amount)

    @property
    def get_aele_mandi_info(self):
        personnel_family = PersonnelFamily.objects.filter(personnel=self.workshop_personnel.personnel)
        aele_mandi_child = 0
        self.total_insurance_month = self.workshop_personnel.insurance_history_totality
        for person in personnel_family:
            if person.relative == 'c' and person.marital_status == 's':
                person_age = self.list_of_pay.year - person.date_of_birth.year
                if person_age <= 18:
                    aele_mandi_child += 1
                elif person.study_status == 's' or person.physical_condition != 'h':
                    aele_mandi_child += 1
        return aele_mandi_child

    @property
    def get_sanavt_info(self):
        hr = self.get_hr_letter
        sanavat_base = hr.paye_sanavat_amount
        sanavat_month = 0
        if self.workshop_personnel.workshop.sanavat_type == 'c':
            sanavat_month = self.workshop_personnel.current_insurance_history_in_workshop
        elif self.workshop_personnel.workshop.sanavat_type == 'n':
            sanavat_month = self.workshop_personnel.current_insurance_history_in_workshop +\
                                 self.workshop_personnel.previous_insurance_history_in_workshop
        return sanavat_base, sanavat_month

    def calculate_hr_item_in_real_work_time(self, item):
        total = Decimal(self.real_worktime) * item / Decimal(self.list_of_pay.month_days)
        return total

    @property
    def get_total_payment(self):
        hr = self.get_hr_letter
        month_day = self.list_of_pay.month_days
        total = Decimal(0)
        total += self.hoghoogh_roozane * Decimal(self.real_worktime)
        if self.sanavat_month >= 12:
            total += self.sanavat_base * Decimal(self.real_worktime)
        if self.total_insurance_month >= 24:
            total += Decimal(self.aele_mandi_child) * self.aele_mandi_amount * self.aele_mandi_nerkh *\
                     Decimal(self.real_worktime) / Decimal(month_day)
            self.aele_mandi = round(Decimal(self.aele_mandi_child) * self.aele_mandi_amount * self.aele_mandi_nerkh *\
                     Decimal(self.real_worktime) / Decimal(month_day))
        self.ezafe_kari_total = int(self.ezafe_kari_amount * Decimal(self.ezafe_kari_nerkh) * Decimal(self.ezafe_kari))
        total += self.ezafe_kari_amount * Decimal(self.ezafe_kari_nerkh) * Decimal(self.ezafe_kari)
        self.tatil_kari_total = round(self.tatil_kari_amount * Decimal(self.tatil_kari_nerkh) * Decimal(self.tatil_kari))
        total += self.tatil_kari_amount * Decimal(self.tatil_kari_nerkh) * Decimal(self.tatil_kari)
        self.shab_kari_total = round(self.shab_kari * Decimal(self.shab_kari_nerkh) * Decimal(self.shab_kari_amount))
        total += self.shab_kari * Decimal(self.shab_kari_nerkh) * Decimal(self.shab_kari_amount)
        self.kasre_kar_total = round(self.kasre_kar_amount * Decimal(self.kasre_kar_nerkh) * Decimal(self.kasre_kar))
        total -= self.kasre_kar_amount * Decimal(self.kasre_kar_nerkh) * Decimal(self.kasre_kar)
        total += Decimal(self.mission_day) * self.mission_nerkh * self.mission_amount
        total += Decimal(self.nobat_kari_sob_asr) * self.nobat_kari_sob_asr_nerkh * self.nobat_kari_sob_asr_amount
        total += Decimal(self.nobat_kari_sob_shab) * self.nobat_kari_sob_shab_nerkh * self.nobat_kari_sob_shab_amount
        total += Decimal(self.nobat_kari_asr_shab) * self.nobat_kari_asr_shab_nerkh * self.nobat_kari_asr_shab_amount
        total += Decimal(self.nobat_kari_sob_asr_shab) * self.nobat_kari_sob_asr_shab_nerkh * \
                 self.nobat_kari_sob_asr_shab_amount

        total += self.calculate_hr_item_in_real_work_time(hr.haghe_sarparasti_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_modiriyat_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_jazb_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.fogholade_shoghl_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_tahsilat_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.fogholade_sakhti_kar_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_ankal_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.fogholade_badi_abohava_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.mahroomiat_tashilat_zendegi_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.fogholade_mahal_khedmat_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.fogholade_sharayet_mohit_kar_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_maskan_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.bon_kharo_bar_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.yarane_ghaza_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_shir_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_mahdekoodak_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_varzesh_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_mobile_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.mazaya_mostamar_gheyre_naghdi_amount)

        total += self.mazaya_gheyr_mostamar
        total += self.sayer_ezafat
        return total


    def set_info_from_workshop(self):
        hr = self.get_hr_letter
        self.hoghoogh_roozane = hr.hoghooghe_roozane_amount
        hourly_pay = round(self.hoghoogh_roozane / Decimal(7.33))
        if self.workshop_personnel.workshop.base_pay_type == 'd':
            self.pay_base = hr.daily_pay_base
            self.hourly_pay_base = hr.day_hourly_pay_base
        elif self.workshop_personnel.workshop.base_pay_type == 'm':
            self.pay_base = hr.monthly_pay_base
            self.hourly_pay_base = hr.month_hourly_pay_base

        self.ezafe_kari_nerkh = self.workshop_personnel.workshop.ezafe_kari_nerkh
        if self.workshop_personnel.workshop.ezafe_kari_pay_type == 'd':
            self.ezafe_kari_amount = hourly_pay
        if self.workshop_personnel.workshop.ezafe_kari_pay_type == 'b':
            self.ezafe_kari_amount = self.hourly_pay_base

        self.tatil_kari_nerkh = self.workshop_personnel.workshop.tatil_kari_nerkh
        if self.workshop_personnel.workshop.tatil_kari_pay_type == 'd':
            self.tatil_kari_amount = hourly_pay
        if self.workshop_personnel.workshop.tatil_kari_pay_type == 'b':
            self.tatil_kari_amount = self.hourly_pay_base

        self.kasre_kar_nerkh = self.workshop_personnel.workshop.kasre_kar_nerkh
        if self.workshop_personnel.workshop.kasre_kar_pay_type == 'd':
            self.kasre_kar_amount = hourly_pay
        if self.workshop_personnel.workshop.kasre_kar_pay_type == 'b':
            self.kasre_kar_amount = self.hourly_pay_base

        self.shab_kari_nerkh = self.workshop_personnel.workshop.shab_kari_nerkh
        if self.workshop_personnel.workshop.shab_kari_pay_type == 'd':
            self.shab_kari_amount = hourly_pay
        if self.workshop_personnel.workshop.shab_kari_pay_type == 'b':
            self.shab_kari_amount = self.hourly_pay_base

        self.nobat_kari_sob_asr_nerkh = self.workshop_personnel.workshop.nobat_kari_sob_asr_nerkh
        if self.workshop_personnel.workshop.nobat_kari_sob_asr_pay_type == 'd':
            self.nobat_kari_sob_asr_amount = self.hoghoogh_roozane
        if self.workshop_personnel.workshop.nobat_kari_sob_asr_pay_type == 'b':
            self.nobat_kari_sob_asr_amount = self.pay_base

        self.nobat_kari_sob_shab_nerkh = self.workshop_personnel.workshop.nobat_kari_sob_shab_nerkh
        if self.workshop_personnel.workshop.nobat_kari_sob_shab_pay_type == 'd':
            self.nobat_kari_sob_shab_amount = self.hoghoogh_roozane
        if self.workshop_personnel.workshop.nobat_kari_sob_shab_pay_type == 'b':
            self.nobat_kari_sob_shab_amount = self.pay_base

        self.nobat_kari_asr_shab_nerkh = self.workshop_personnel.workshop.nobat_kari_asr_shab_nerkh
        if self.workshop_personnel.workshop.nobat_kari_asr_shab_pay_type == 'd':
            self.nobat_kari_asr_shab_amount = self.hoghoogh_roozane
        if self.workshop_personnel.workshop.nobat_kari_asr_shab_pay_type == 'b':
            self.nobat_kari_asr_shab_amount = self.pay_base

        self.nobat_kari_sob_asr_shab_nerkh = self.workshop_personnel.workshop.nobat_kari_sob_asr_shab_nerkh
        if self.workshop_personnel.workshop.nobat_kari_sob_asr_shab_pay_type == 'd':
            self.nobat_kari_sob_asr_shab_amount = self.hoghoogh_roozane
        if self.workshop_personnel.workshop.nobat_kari_sob_asr_shab_pay_type == 'b':
            self.nobat_kari_sob_asr_shab_amount = self.pay_base

        self.aele_mandi_nerkh = self.workshop_personnel.workshop.aele_mandi_nerkh
        if self.workshop_personnel.workshop.aele_mandi_pay_type == 'd':
            self.aele_mandi_amount = self.hoghoogh_roozane
        if self.workshop_personnel.workshop.aele_mandi_pay_type == 'b':
            self.aele_mandi_amount = self.pay_base

        self.mission_nerkh = self.workshop_personnel.workshop.mission_pay_nerkh
        if self.workshop_personnel.workshop.mission_pay_type == 'd':
            self.mission_amount = self.hoghoogh_roozane
        if self.workshop_personnel.workshop.mission_pay_type == 'b':
            self.mission_amount = self.pay_base

    @property
    def calculate_yearly_haghe_sanavat(self):
        hr = self.get_hr_letter
        year_worktime = 0
        if self.workshop_personnel.workshop.haghe_sanavat_pay_type == 'b':
            base_pay = hr.daily_pay_base
        else:
            base_pay = hr.hoghooghe_roozane_amount

        previous_items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                                      & Q(list_of_pay__year__lt=self.list_of_pay.year))
        if self.workshop_personnel.workshop.haghe_sanavat_type == 'o':
            work_years = []
            for item in previous_items:
                if item.list_of_pay.year not in work_years:
                    work_years.append(item.list_of_pay.year)
            total_worktime = 0
            list_of_pay_items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                                      & Q(list_of_pay__year__lte=self.list_of_pay.year))
            for pay_list in list_of_pay_items:
                total_worktime += pay_list.real_worktime
                total_worktime += pay_list.illness_leave_day

            until_this_year = round(base_pay) * 30 * total_worktime / (len(work_years) + 1)
            list_of_pay_item = ListOfPayItem.objects.filter(list_of_pay__year=work_years[0]).first()
            return until_this_year - list_of_pay_item.calculate_yearly_haghe_sanavat


        elif self.workshop_personnel.workshop.haghe_sanavat_type == 'c':
            items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                                 & Q(list_of_pay__year=self.list_of_pay.year))
            for item in items:
                year_worktime += item.real_worktime
                year_worktime += item.illness_leave_day
            return round(base_pay) * 30 * year_worktime / 365

    @property
    def calculate_yearly_eydi(self):
        hr = self.get_hr_letter
        year_worktime = 0
        if self.workshop_personnel.workshop.eydi_padash_pay_type == 'b':
            base_pay = hr.daily_pay_base
        else:
            base_pay = hr.hoghooghe_roozane_amount

        items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                             & Q(list_of_pay__year=self.list_of_pay.year))
        for item in items:
            year_worktime += item.real_worktime
            year_worktime += item.illness_leave_day
        return round(base_pay) * 60 * year_worktime / 365

    @property
    def calculate_monthly_haghe_sanavat(self):
        hr = self.get_hr_letter
        if self.workshop_personnel.workshop.haghe_sanavat_pay_type == 'b':
            base_pay = hr.daily_pay_base
        else:
            base_pay = hr.hoghooghe_roozane_amount
        return round(base_pay) * 30 * (self.real_worktime + self.illness_leave_day) / 365

    @property
    def calculate_monthly_eydi(self):
        hr = self.get_hr_letter
        if self.workshop_personnel.workshop.eydi_padash_pay_type == 'b':
            base_pay = hr.daily_pay_base
        else:
            base_pay = hr.hoghooghe_roozane_amount
        return round(base_pay) * 60 * (self.real_worktime + self.illness_leave_day) / 365

    @property
    def calculate_monthly_eydi_tax(self):
        hr = self.get_hr_letter
        if hr.eydi_padash_use_tax:
            mytax = WorkshopTax.objects.first()
            tax_rows = WorkshopTaxRow.objects.filter(workshop_tax=mytax)
            tax_row = tax_rows.get(from_amount=Decimal(0))
            moafiat_limit = tax_row.to_amount / 12 /12
            eydi = self.calculate_monthly_eydi
            moaf = moafiat_limit - eydi
            if moaf <= 0:
                eydi_tax = -moaf
            else:
                eydi_tax = 0

            return eydi_tax
        else:
            return 0

    @property
    def calculate_yearly_eydi_tax(self):
        hr = self.get_hr_letter
        if hr.eydi_padash_use_tax:
            mytax = WorkshopTax.objects.first()
            tax_rows = WorkshopTaxRow.objects.filter(workshop_tax=mytax)
            tax_row = tax_rows.get(from_amount=Decimal(0))
            moafiat_limit = tax_row.to_amount / 12
            eydi = self.calculate_yearly_eydi
            moaf = moafiat_limit - eydi
            if moaf <= 0:
                eydi_tax = -moaf
            else:
                eydi_tax = 0

            return eydi_tax
        else:
            return 0

    @property
    def calculate_save_leave(self):
        hr = self.get_hr_letter
        year_worktime = 0
        items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                             & Q(list_of_pay__year=self.list_of_pay.year))
        leave_available = 29
        for item in items:
            leave_available -= item.entitlement_leave_day
            year_worktime += item.real_worktime
        if leave_available >= 9:
            save_leave = 9
        else:
            save_leave = leave_available
        if self.workshop_personnel.workshop.leave_save_pay_type == 'h':
            pay_base = hr.calculate_save_leave_base
        else:
            pay_base = self.workshop_personnel.workshop.hade_aghal_hoghoogh

        save_leave_amount = save_leave * pay_base * year_worktime / 365


        return save_leave, save_leave_amount


    def save(self, *args, **kwargs):
        if not self.id:
            self.sanavat_base, self.sanavat_month = self.get_sanavt_info
            self.set_info_from_workshop()
            self.aele_mandi_child = self.get_aele_mandi_info
        if self.calculate_payment:
            self.total_payment = int(self.get_total_payment)
        super().save(*args, **kwargs)

