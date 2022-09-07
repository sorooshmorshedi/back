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

    BASE_PAY_TYPES = (
        (DAILY, 'مزد مبنای روزانه'),
        (MONTHLY, 'مزد مبنای ماهیانه')
    )

    DAILY_PAY = 'd'
    BASE_PAY = 'b'

    PAY_TYPES = (
        (DAILY_PAY, 'حداقل حقوق روزانه'),
        (BASE_PAY, 'مزد مبنا')
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


class ContractRow(BaseModel, LockableMixin, DefinableMixin):
    ACTIVE = 'a'
    NO_ACTIVE = 'n'

    ACTIVE_TYPE = (
        (ACTIVE, 'فعال'),
        (NO_ACTIVE, 'غیر فعال')
    )

    workshop = models.ForeignKey(Workshop, related_name='contract_rows', on_delete=models.CASCADE)
    contract_row = models.IntegerField()
    contract_number = models.IntegerField()
    registration_date = jmodels.jDateField(blank=True, null=True)
    from_date = jmodels.jDateField(blank=True, null=True)
    to_date = jmodels.jDateField(blank=True, null=True)

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
        return str(self.contract_row) + ' in ' + self.workshop.name


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
        (MALE, 'آقا'),
        (FEMALE, 'خانم')
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

    LEAVE_TYPES = (
        (ENTITLEMENT, 'استحقاقی'),
        (ILLNESS, 'استعلاجی'),
        (WITHOUT_SALARY, 'بدون حقوق'),
        (ABSENCE, 'غیبت'),
    )

    HOURLY = 'h'
    DAILY = 'd'

    ENTITLEMENT_LEAVE_TYPES = (
        (HOURLY, 'ساعتی'),
        (DAILY, 'روزانه'),

    )

    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name='leave', on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPES, default=WITHOUT_SALARY)
    entitlement_leave_type = models.CharField(max_length=2, choices=ENTITLEMENT_LEAVE_TYPES, blank=True, null=True)
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
        return final_by_day

    def save(self, *args, **kwargs):
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
        (BASE_PAY, 'حقوق پایه'),
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

    hoghooghe_roozane_use_tax = models.BooleanField(default=False)
    hoghooghe_roozane_use_insurance = models.BooleanField(default=False)
    hoghooghe_roozane_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    hoghooghe_roozane_amount = DECIMAL(default=0)
    hoghooghe_roozane_base = models.BooleanField(default=False)

    paye_sanavat_use_tax = models.BooleanField(default=False)
    paye_sanavat_use_insurance = models.BooleanField(default=False)
    paye_sanavat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    paye_sanavat_amount = DECIMAL(default=0)
    paye_sanavat_base = models.BooleanField(default=False)

    haghe_sarparasti_use_tax = models.BooleanField(default=False)
    haghe_sarparasti_use_insurance = models.BooleanField(default=False)
    haghe_sarparasti_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_sarparasti_amount = DECIMAL(default=0)
    haghe_sarparasti_base = models.BooleanField(default=False)

    haghe_modiriyat_use_tax = models.BooleanField(default=False)
    haghe_modiriyat_use_insurance = models.BooleanField(default=False)
    haghe_modiriyat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_modiriyat_amount = DECIMAL(default=0)
    haghe_modiriyat_base = models.BooleanField(default=False)

    haghe_jazb_use_tax = models.BooleanField(default=False)
    haghe_jazb_use_insurance = models.BooleanField(default=False)
    haghe_jazb_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_jazb_amount = DECIMAL(default=0)
    haghe_jazb_base = models.BooleanField(default=False)

    fogholade_shoghl_use_tax = models.BooleanField(default=False)
    fogholade_shoghl_use_insurance = models.BooleanField(default=False)
    fogholade_shoghl_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    fogholade_shoghl_amount = DECIMAL(default=0)
    fogholade_shoghl_base = models.BooleanField(default=False)

    haghe_tahsilat_use_tax = models.BooleanField(default=False)
    haghe_tahsilat_use_insurance = models.BooleanField(default=False)
    haghe_tahsilat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_tahsilat_amount = DECIMAL(default=0)
    haghe_tahsilat_base = models.BooleanField(default=False)

    fogholade_sakhti_kar_use_tax = models.BooleanField(default=False)
    fogholade_sakhti_kar_use_insurance = models.BooleanField(default=False)
    fogholade_sakhti_kar_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    fogholade_sakhti_kar_amount = DECIMAL(default=0)
    fogholade_sakhti_kar_base = models.BooleanField(default=False)

    haghe_ankal_use_tax = models.BooleanField(default=False)
    haghe_ankal_use_insurance = models.BooleanField(default=False)
    haghe_ankal_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_ankal_amount = DECIMAL(default=0)
    haghe_ankal_base = models.BooleanField(default=False)

    fogholade_badi_abohava_use_tax = models.BooleanField(default=False)
    fogholade_badi_abohava_use_insurance = models.BooleanField(default=False)
    fogholade_badi_abohava_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    fogholade_badi_abohava_amount = DECIMAL(default=0)
    fogholade_badi_abohava_base = models.BooleanField(default=False)

    mahroomiat_tashilat_zendegi_use_tax = models.BooleanField(default=False)
    mahroomiat_tashilat_zendegi_use_insurance = models.BooleanField(default=False)
    mahroomiat_tashilat_zendegi_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    mahroomiat_tashilat_zendegi_amount = DECIMAL(default=0)
    mahroomiat_tashilat_zendegi_base = models.BooleanField(default=False)

    fogholade_mahal_khedmat_use_tax = models.BooleanField(default=False)
    fogholade_mahal_khedmat_use_insurance = models.BooleanField(default=False)
    fogholade_mahal_khedmat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    fogholade_mahal_khedmat_amount = DECIMAL(default=0)
    fogholade_mahal_khedmat_base = models.BooleanField(default=False)

    fogholade_sharayet_mohit_kar_use_tax = models.BooleanField(default=False)
    fogholade_sharayet_mohit_kar_use_insurance = models.BooleanField(default=False)
    fogholade_sharayet_mohit_kar_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    fogholade_sharayet_mohit_kar_amount = DECIMAL(default=0)
    fogholade_sharayet_mohit_kar_base = models.BooleanField(default=False)

    haghe_maskan_use_tax = models.BooleanField(default=False)
    haghe_maskan_use_insurance = models.BooleanField(default=False)
    haghe_maskan_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_maskan_amount = DECIMAL(default=0)
    haghe_maskan_base = models.BooleanField(default=False)

    ayabo_zahab_use_tax = models.BooleanField(default=False)
    ayabo_zahab_use_insurance = models.BooleanField(default=False)
    ayabo_zahab_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    ayabo_zahab_amount = DECIMAL(default=0)
    ayabo_zahab_base = models.BooleanField(default=False)

    bon_kharo_bar_use_tax = models.BooleanField(default=False)
    bon_kharo_bar_use_insurance = models.BooleanField(default=False)
    bon_kharo_bar_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    bon_kharo_bar_amount = DECIMAL(default=0)
    bon_kharo_bar_base = models.BooleanField(default=False)

    yarane_ghaza_use_tax = models.BooleanField(default=False)
    yarane_ghaza_use_insurance = models.BooleanField(default=False)
    yarane_ghaza_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    yarane_ghaza_amount = DECIMAL(default=0)
    yarane_ghaza_base = models.BooleanField(default=False)

    haghe_shir_use_tax = models.BooleanField(default=False)
    haghe_shir_use_insurance = models.BooleanField(default=False)
    haghe_shir_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_shir_amount = DECIMAL(default=0)
    haghe_shir_base = models.BooleanField(default=False)

    haghe_taahol_use_tax = models.BooleanField(default=False)
    haghe_taahol_use_insurance = models.BooleanField(default=False)
    haghe_taahol_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    haghe_taahol_amount = DECIMAL(default=0)
    haghe_taahol_base = models.BooleanField(default=False)

    komakhazine_mahdekoodak_use_tax = models.BooleanField(default=False)
    komakhazine_mahdekoodak_use_insurance = models.BooleanField(default=False)
    komakhazine_mahdekoodak_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    komakhazine_mahdekoodak_amount = DECIMAL(default=0)
    komakhazine_mahdekoodak_base = models.BooleanField(default=False)

    komakhazine_varzesh_use_tax = models.BooleanField(default=False)
    komakhazine_varzesh_use_insurance = models.BooleanField(default=False)
    komakhazine_varzesh_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    komakhazine_varzesh_amount = DECIMAL(default=0)
    komakhazine_varzesh_base= models.BooleanField(default=False)

    komakhazine_mobile_use_tax = models.BooleanField(default=False)
    komakhazine_mobile_use_insurance = models.BooleanField(default=False)
    komakhazine_mobile_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=BASE_PAY)
    komakhazine_mobile_amount = DECIMAL(default=0)
    komakhazine_mobile_base = models.BooleanField(default=False)


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
    def calculate_pay_bases(self):
        hr_letter_items = []
        hr_letter_items.append({'base': self.hoghooghe_roozane_base, 'amount': self.hoghooghe_roozane_amount})
        hr_letter_items.append({'base': self.paye_sanavat_base, 'amount': self.paye_sanavat_amount})
        hr_letter_items.append({'base': self.haghe_sarparasti_base, 'amount': self.haghe_sarparasti_amount})
        hr_letter_items.append({'base': self.haghe_modiriyat_base, 'amount': self.haghe_modiriyat_amount})
        hr_letter_items.append({'base': self.haghe_jazb_base, 'amount': self.haghe_jazb_amount})
        hr_letter_items.append({'base': self.fogholade_shoghl_base, 'amount': self.fogholade_shoghl_amount})
        hr_letter_items.append({'base': self.haghe_tahsilat_base, 'amount': self.haghe_tahsilat_amount})
        hr_letter_items.append({'base': self.fogholade_sakhti_kar_base, 'amount': self.fogholade_sakhti_kar_amount})
        hr_letter_items.append({'base': self.haghe_ankal_base, 'amount': self.haghe_ankal_amount})
        hr_letter_items.append({'base': self.fogholade_badi_abohava_base, 'amount': self.fogholade_badi_abohava_amount})
        hr_letter_items.append({'base': self.mahroomiat_tashilat_zendegi_base, 'amount': self.mahroomiat_tashilat_zendegi_amount})
        hr_letter_items.append({'base': self.fogholade_mahal_khedmat_base, 'amount': self.fogholade_mahal_khedmat_amount})
        hr_letter_items.append({'base': self.fogholade_sharayet_mohit_kar_base, 'amount': self.fogholade_sharayet_mohit_kar_amount})
        hr_letter_items.append({'base': self.haghe_maskan_base, 'amount': self.haghe_maskan_base})
        hr_letter_items.append({'base': self.ayabo_zahab_base, 'amount': self.ayabo_zahab_amount})
        hr_letter_items.append({'base': self.bon_kharo_bar_base, 'amount': self.bon_kharo_bar_amount})
        hr_letter_items.append({'base': self.yarane_ghaza_base, 'amount': self.yarane_ghaza_amount})
        hr_letter_items.append({'base': self.haghe_shir_base, 'amount': self.haghe_shir_amount})
        hr_letter_items.append({'base': self.haghe_taahol_base, 'amount': self.haghe_taahol_amount})
        hr_letter_items.append({'base': self.komakhazine_mahdekoodak_base, 'amount': self.komakhazine_mahdekoodak_amount})
        hr_letter_items.append({'base': self.komakhazine_varzesh_base, 'amount': self.komakhazine_varzesh_amount})
        hr_letter_items.append({'base': self.komakhazine_mobile_base, 'amount': self.komakhazine_mobile_amount})

        daily, monthly = 0, 0

        for i in range(0, 22):
            if hr_letter_items[i]['base'] and hr_letter_items[i]['amount']:
                if i < 2:
                    daily += int(hr_letter_items[i]['amount'])
                    monthly += int(hr_letter_items[i]['amount'] * 30)
                else:
                    daily += int(hr_letter_items[i]['amount'] / 30)
                    monthly += int(hr_letter_items[i]['amount'])
        month_hourly = monthly / 220
        day_hourly = daily / 7.33
        return daily, monthly, day_hourly, month_hourly

    def save(self, *args, **kwargs):
        if self.pay_done:
            raise ValidationError(message='حکم غیرقابل تفییر است')

        self.daily_pay_base, self.monthly_pay_base, self.day_hourly_pay_base, self.month_hourly_pay_base =\
            self.calculate_pay_bases

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
    def info_for_itams(self):
        personnels = []
        contracts = []
        personnel_normal_worktime = {}
        workshop_personnel = WorkshopPersonnel.objects.filter(workshop=self.workshop)
        workshop_contracts = Contract.objects.filter(workshop_personnel__in=workshop_personnel)
        for personnel in Personnel.objects.filter(workshop_personnel__in=workshop_personnel):
            personnel_normal_worktime[personnel.id] = 0
        for contract in workshop_contracts:
            if not contract.quit_job_date:
                end = contract.contract_to_date
            else:
                end = contract.quit_job_date
            if contract.contract_from_date.__le__(self.start_date) and end.__ge__(self.end_date):
                contracts.append(contract.id)
                personnel_normal_worktime[contract.workshop_personnel.personnel.id] += self.month_days
            if contract.contract_from_date.__ge__(self.start_date) and end.__le__(self.end_date):
                contracts.append(contract.id)
                personnel_normal_worktime[contract.workshop_personnel.personnel.id] += \
                    end.day - contract.contract_from_date.day
            if contract.contract_from_date.__le__(self.start_date) and end.__gt__(self.start_date) and \
                    end.__lt__(self.end_date):
                contracts.append(contract.id)
                personnel_normal_worktime[contract.workshop_personnel.personnel.id] += \
                    end.day
            if contract.contract_from_date.__ge__(self.start_date) and end.__ge__(self.end_date) and \
                    contract.contract_from_date.__lt__(self.end_date):
                contracts.append(contract.id)
                personnel_normal_worktime[contract.workshop_personnel.personnel.id] += \
                    self.month_days - contract.contract_from_date.day + 1

        filtered_contracts = Contract.objects.filter(pk__in=contracts)

        for contract in filtered_contracts:
            personnels.append(contract.workshop_personnel.personnel.id)
        personnels = Personnel.objects.filter(Q(pk__in=personnels) & Q(is_personnel_active=True))
        filtered_workshops = WorkshopPersonnel.objects.filter(Q(personnel__in=personnels) &
                                                              Q(workshop=self.workshop))

        filtered_absence = LeaveOrAbsence.objects.filter(workshop_personnel__in=filtered_workshops)
        filtered_mission = Mission.objects.filter(workshop_personnel__in=filtered_workshops)

        response_data = []
        for personnel in personnels:
            absence_types = {'i': 0, 'w': 0, 'a': 0, 'e': 0}
            mission_day = 0
            workshop_personnel = WorkshopPersonnel.objects.get(personnel=personnel)
            contracts = filtered_contracts.filter(workshop_personnel=workshop_personnel).all()
            is_insurance = contracts.first().insurance
            print(len(contracts))
            for absence in filtered_absence.all():
                if absence.workshop_personnel.personnel == personnel:
                    if absence.from_date.__ge__(self.start_date) and absence.to_date.__le__(self.end_date):
                        absence_types[absence.leave_type] += absence.time_period
                    elif absence.from_date.__lt__(self.start_date) and absence.to_date.__le__(self.end_date) and \
                            absence.to_date.__gt__(self.start_date):
                        absence_types[absence.leave_type] += absence.to_date.day
                    elif absence.from_date.__gt__(self.start_date) and absence.to_date.__gt__(self.end_date) and \
                            absence.from_date.__le__(self.end_date):
                        absence_types[absence.leave_type] += self.month_days - absence.from_date.day
                    elif absence.from_date.__le__(self.start_date) and absence.to_date.__ge__(self.end_date):
                        absence_types[absence.leave_type] += self.month_days



            for mission in filtered_mission.all():
                if mission.workshop_personnel.personnel == personnel and mission.mission_type != 'h' and\
                        mission.is_in_payment:
                    if mission.from_date.__ge__(self.start_date) and mission.to_date.__le__(self.end_date):
                        mission_day += mission.time_period
                    elif mission.from_date.__lt__(self.start_date) and mission.to_date.__le__(self.end_date) and \
                            mission.to_date.__gt__(self.start_date):
                        mission_day += mission.to_date.day
                    elif mission.from_date.__gt__(self.start_date) and mission.to_date.__gt__(self.end_date) and \
                            mission.from_date.__le__(self.end_date):
                        mission_day += self.month_days - mission.from_date.day
                    elif mission.from_date.__le__(self.start_date) and mission.to_date.__ge__(self.end_date):
                        mission_day += self.month_days

            normal = personnel_normal_worktime[personnel.id]
            real_work = normal - absence_types['a'] - int(absence_types['i']) - int(absence_types['w'])
            response_data.append(
                {
                    'pk': personnel.id,
                    'leaves': absence_types,
                    'name': personnel.name + ' ' + personnel.last_name,
                    'normal_work': normal,
                    'real_work': real_work,
                    'mission': mission_day,
                    'insurance': is_insurance,
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

    hoghoogh_roozane = DECIMAL()
    pay_base = models.IntegerField(default=0)
    sanavat_base = DECIMAL(default=0)
    sanavat_month = models.IntegerField(default=0)
    aele_mandi_child = models.IntegerField(default=0)
    total_insurance_month = models.IntegerField(default=0)
    is_insurance = models.CharField(max_length=2, choices=INCURANCE_TYPES, default=NO)

    hourly_pay_base = models.IntegerField(default=0)
    normal_worktime = models.IntegerField(default=0)

    entitlement_leave_day = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=2)

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

    tatil_kari = models.DecimalField(default=0, max_digits=24, decimal_places=2)
    tatil_kari_amount = DECIMAL(default=0)
    tatil_kari_nerkh = models.DecimalField(max_digits=24, default=1.96, decimal_places=2)


    kasre_kar = models.DecimalField(default=0, max_digits=24, decimal_places=2)
    kasre_kar_amount = DECIMAL(default=0)
    kasre_kar_nerkh = models.DecimalField(max_digits=24, default=1.4, decimal_places=2)


    shab_kari = models.DecimalField(default=0, max_digits=24, decimal_places=2)
    shab_kari_amount = DECIMAL(default=0)
    shab_kari_nerkh = models.DecimalField(max_digits=24, default=0.35, decimal_places=2)


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
    calculate_payment = models.BooleanField(default=False)

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
        last_contract = Contract.objects.filter(workshop_personnel=self.workshop_personnel)
        hr = HRLetter.objects.filter(contract__in=last_contract).first()
        return hr

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
            self.aele_mandi = int(Decimal(self.aele_mandi_child) * self.aele_mandi_amount * self.aele_mandi_nerkh *\
                     Decimal(self.real_worktime) / Decimal(month_day))
        total += self.ezafe_kari_amount * Decimal(self.ezafe_kari_nerkh) * Decimal(self.ezafe_kari)
        total += self.tatil_kari_amount * Decimal(self.tatil_kari_nerkh) * Decimal(self.tatil_kari)
        total += self.shab_kari * Decimal(self.shab_kari_nerkh) * Decimal(self.shab_kari_amount)
        total -= self.kasre_kar_amount * Decimal(self.kasre_kar_nerkh) * Decimal(self.kasre_kar)
        total += Decimal(self.mission_day) * self.mission_nerkh * self.mission_amount
        total += Decimal(self.nobat_kari_sob_asr) * self.nobat_kari_sob_asr_nerkh * self.nobat_kari_sob_asr_amount
        total += Decimal(self.nobat_kari_sob_shab) * self.nobat_kari_sob_shab_nerkh * self.nobat_kari_sob_shab_amount
        total += Decimal(self.nobat_kari_asr_shab) * self.nobat_kari_asr_shab_nerkh * self.nobat_kari_asr_shab_amount
        total += Decimal(self.nobat_kari_sob_asr_shab) * self.nobat_kari_sob_asr_shab_nerkh * \
                 self.nobat_kari_sob_asr_shab_amount
        total += Decimal(self.real_worktime) * hr.haghe_sarparasti_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.haghe_modiriyat_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.haghe_jazb_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.fogholade_shoghl_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.haghe_tahsilat_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.fogholade_sakhti_kar_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.haghe_ankal_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.fogholade_badi_abohava_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.mahroomiat_tashilat_zendegi_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.mahroomiat_tashilat_zendegi_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.fogholade_mahal_khedmat_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.fogholade_sharayet_mohit_kar_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.haghe_maskan_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.ayabo_zahab_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.bon_kharo_bar_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.yarane_ghaza_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.haghe_shir_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.haghe_taahol_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.komakhazine_mahdekoodak_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.komakhazine_varzesh_amount / Decimal(month_day)
        total += Decimal(self.real_worktime) * hr.komakhazine_mobile_amount / Decimal(month_day)
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


    def save(self, *args, **kwargs):
        if not self.id:
            self.sanavat_base, self.sanavat_month = self.get_sanavt_info
            self.set_info_from_workshop()
            self.aele_mandi_child = self.get_aele_mandi_info
        if self.calculate_payment:
            self.total_payment = int(self.get_total_payment)
        super().save(*args, **kwargs)
