from django.db import models
from django_jalali.db import models as jmodels
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from companies.models import Company
from helpers.models import BaseModel, LockableMixin, DefinableMixin, POSTAL_CODE, DECIMAL
from users.models import City


class Workshop(BaseModel, LockableMixin, DefinableMixin):
    company = models.ForeignKey(Company, related_name='workshop', on_delete=models.CASCADE)

    code = models.IntegerField()
    name = models.CharField(max_length=100)
    employer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    employer_insurance_contribution = models.IntegerField(validators=[
        MinLengthValidator(limit_value=0, message='درصد صحیح نبست'),
        MaxLengthValidator(limit_value=3, message='درصد صحیح نبست')
    ])

    branch_code = models.IntegerField(blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)

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


class ContractRow(BaseModel, LockableMixin, DefinableMixin):
    workshop = models.ForeignKey(Workshop, related_name='contract_row', on_delete=models.CASCADE)
    contract_row = models.IntegerField()
    contract_number = models.IntegerField()
    registration_date = jmodels.jDateField(blank=True, null=True)
    from_date = jmodels.jDateField(blank=True, null=True)
    to_date = jmodels.jDateField(blank=True, null=True)

    is_activate = models.BooleanField(default=False)

    assignor_name = models.CharField(max_length=100, blank=True, null=True)
    assignor_national_code = models.IntegerField(unique=True, validators=[
        MinLengthValidator(limit_value=9, message='کد ملی باید ده رقم باشد'),
        MaxLengthValidator(limit_value=11, message='کد ملی باید ده رقم باشد')
    ])
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

    MILITARY_SERVICE_STATUS = (
        (DONE, 'انجام داده'),
        (NOT_DONE, 'انجام نداده'),
        (EXEMPT, 'معاف')
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
    NONE_PROFIT = 'NP'

    university_types = (
        (STATE, 'دولتی'),
        (OPEN, 'آزاد'),
        (NONE_PROFIT, 'غیر انتفاعی')
    )

    company = models.ForeignKey(Company, related_name='personnel', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    country = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=1, choices=NATIONALITY_TYPE, default=IRANIAN)

    personnel_code = models.IntegerField(unique=True)

    gender = models.CharField(max_length=1, choices=GENDER_TYPE, default=MALE)
    military_service = models.CharField(max_length=1, choices=MILITARY_SERVICE_STATUS, default=NOT_DONE)

    national_code = models.IntegerField(unique=True, validators=[
        MinLengthValidator(limit_value=9, message='کد ملی باید ده رقم باشد'),
        MaxLengthValidator(limit_value=11, message='کد ملی باید ده رقم باشد')
    ])

    identity_code = models.IntegerField(unique=True)
    date_of_birth = jmodels.jDateField()
    date_of_exportation = jmodels.jDateField()
    location_of_birth = City()
    location_of_exportation = City()
    sector_of_exportation = City()

    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_TYPES, default=SINGLE)
    number_of_childes = models.IntegerField(default=0)

    city_phone_code = models.IntegerField()
    phone_number = models.IntegerField()
    mobile_number_1 = models.IntegerField(
        validators=[RegexValidator(regex='^(09){1}[0-9]{9}$', message='phone number format: 09*********')])
    mobile_number_2 = models.IntegerField(
        validators=[RegexValidator(regex='^(09){1}[0-9]{9}$', message='phone number format: 09*********')],
        null=True, blank=True)
    address = models.CharField(max_length=255)
    postal_code = POSTAL_CODE()

    insurance = models.BooleanField(default=False)
    insurance_code = models.IntegerField(blank=True, null=True)

    degree_of_education = models.CharField(max_length=2, choices=DEGREE_TYPE, default=DIPLOMA)
    field_of_study = models.CharField(max_length=100)
    university_type = models.CharField(max_length=2, choices=university_types, blank=True, null=True)
    university_name = models.CharField(max_length=50, blank=True, null=True)

    account_bank_name = models.CharField(max_length=50, blank=True, null=True)
    account_bank_number = models.IntegerField(blank=True, null=True)
    sheba_number = models.IntegerField(blank=True, null=True)

    is_personnel_active = models.BooleanField(default=False)

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

    MILITARY_SERVICE_STATUS = (
        (DONE, 'انجام داده'),
        (NOT_DONE, 'انجام نداده'),
        (EXEMPT, 'معاف')
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
    national_code = models.IntegerField(unique=True, validators=[
        MinLengthValidator(limit_value=9, message='کد ملی باید ده رقم باشد'),
        MaxLengthValidator(limit_value=11, message='کد ملی باید ده رقم باشد')
    ])
    date_of_birth = jmodels.jDateField()
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

    def save(self, *args, **kwargs):
        if self.relative == 'c' and not self.id:
            personnel = self.Personnel
            personnel.number_of_childes += 1
            personnel.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.relative == 'c':
            personnel = self.Personnel
            personnel.number_of_childes -= 1
            personnel.save()
        super().delete()



class WorkshopPersonnel(BaseModel, LockableMixin, DefinableMixin):
    PART_TIME = 'p'
    FULL_TIME = 'f'
    CONTRACTUAL = 'c'
    TEMPORARY = 't'
    HOURLY = 'h'

    CONTRACT_TYPES = (
        (PART_TIME, 'پاره وقت'),
        (FULL_TIME, 'تمام وقت'),
        (TEMPORARY, 'موقت'),
        (HOURLY, 'ساعتی'),
        (CONTRACTUAL, 'پیمانی')

    )

    CONVENTIONAL = 'co'
    PERMANENT = 'p'
    CORPORATE = 'cr'
    FUNCTIONARY = 'fu'
    OTHERS = 'or'

    EMPLOYMENTS_TYPES = (
        (CONTRACTUAL, 'پیمانی'),
        (CONVENTIONAL, 'قراردادی'),
        (CORPORATE, 'َشرکتی'),
        (FUNCTIONARY, 'مامور'),
        (OTHERS, 'سایر'),
        (PERMANENT, 'رسمی')
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

    workshop = models.ForeignKey(Workshop, related_name='workshop_personnel', on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, related_name='workshop_personnel', on_delete=models.CASCADE)

    insurance = models.BooleanField(default=False)
    insurance_add_date = jmodels.jDateField(blank=True, null=True)
    work_title = models.CharField(max_length=100, blank=True, null=True)

    previous_insurance_history_out_workshop = models.IntegerField()
    previous_insurance_history_in_workshop = models.IntegerField()
    current_insurance_history_in_workshop = models.IntegerField()
    insurance_history_totality = models.IntegerField()

    job_position = models.CharField(max_length=100)
    job_group = models.CharField(max_length=100)
    job_location = models.CharField(max_length=100)
    job_location_status = models.CharField(max_length=100)

    employment_type = models.CharField(max_length=2, choices=EMPLOYMENTS_TYPES, default=CONVENTIONAL)
    contract_type = models.CharField(max_length=2, choices=CONTRACT_TYPES, default=FULL_TIME)
    employee_status = models.CharField(max_length=2, choices=EMPLOYEE_TYPES, default=NORMAL)

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


class ContractTime(BaseModel, LockableMixin, DefinableMixin):
    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name='contract_time', on_delete=models.CASCADE)
    code = models.IntegerField()
    contract_from_date = jmodels.jDateField()
    contract_to_date = jmodels.jDateField()
    quit_job_date = jmodels.jDateField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'ContractTime'
        permission_basename = 'contract_time'
        permissions = (
            ('get.contract_time', 'مشاهده قرارداد کارگاه'),
            ('create.contract_time', 'تعریف قرارداد کارگاه'),
            ('update.contract_time', 'ویرایش قرارداد کارگاه'),
            ('delete.contract_time', 'حذف قرارداد کارگاه'),

            ('getOwn.contract_time', 'مشاهده قرارداد کارگاه خود'),
            ('updateOwn.contract_time', 'ویرایش قرارداد کارگاه خود'),
            ('deleteOwn.contract_time', 'حذف قرارداد کارگاه خود'),
        )
