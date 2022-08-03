from django.db import models
from django_jalali.db import models as jmodels
from django.core.validators import MinLengthValidator, MaxLengthValidator
from companies.models import Company
from helpers.models import BaseModel, LockableMixin, DefinableMixin, POSTAL_CODE, DECIMAL
from users.models import City


class Workshop(BaseModel, LockableMixin, DefinableMixin):
    code = models.IntegerField()
    name = models.CharField(max_length=100)
    employer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    employer_insurance_contribution = models.IntegerField(max_length=2, validators=[
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
    contract_row = models.IntegerField(blank=True, null=True)
    contract_number = models.IntegerField()
    registration_date = jmodels.jDateField(blank=True, null=True)
    from_date = jmodels.jDateField(blank=True, null=True)
    to_date = jmodels.jDateField(blank=True, null=True)

    is_activate = models.BooleanField(default=False)

    assignor_name = models.CharField(max_length=100, blank=True, null=True)
    assignor_national_code = models.IntegerField(max_length=10, unique=True, validators=[
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

    DEGREE_TYPE = (
        (UNDER_DIPLOMA, 'زیر دیپلم'),
        (DIPLOMA, 'دیپلم'),
        (ASSOCIATES, 'کاردانی'),
        (BACHELOR, 'لیسانس'),
        (MASTER, 'فوق لیسانس'),
        (DOCTORAL, 'دکترا')
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
    workshop = models.ForeignKey(Workshop, related_name='personnel', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    country = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=1, choices=NATIONALITY_TYPE, default=IRANIAN)

    personnel_code = models.IntegerField(max_length=20)

    gender = models.CharField(max_length=1, choices=GENDER_TYPE, default=MALE)
    military_service = models.CharField(max_length=1, choices=MILITARY_SERVICE_STATUS, default=NOT_DONE)

    national_code = models.IntegerField(max_length=10, unique=True, validators=[
        MinLengthValidator(limit_value=9, message='کد ملی باید ده رقم باشد'),
        MaxLengthValidator(limit_value=11, message='کد ملی باید ده رقم باشد')
    ])

    identity_code = models.IntegerField(max_length=10, unique=True)
    date_of_birth = jmodels.jDateField()
    date_of_exportation = jmodels.jDateField()
    location_of_birth = City()
    location_of_exportation = City()
    sector_of_exportation = City()

    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_TYPES, default=SINGLE)
    number_of_childes = models.IntegerField(max_length=2, blank=True, null=True, default=0, editable=False)

    city_phone_code = models.IntegerField(max_length=3)
    phone_number = models.CharField(max_length=10)
    mobile_number_1 = models.IntegerField(max_length=11)
    mobile_number_2 = models.IntegerField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=255)
    postal_code = POSTAL_CODE()

    insurance = models.BooleanField(default=False)
    insurance_code = models.IntegerField(max_length=20, blank=True, null=True)

    degree_of_education = models.CharField(max_length=2, choices=DEGREE_TYPE, default=DIPLOMA)
    field_of_study = models.CharField(max_length=100)
    university_type = models.CharField(max_length=2, choices=university_types, blank=True, null=True)
    university_name = models.CharField(max_length=50, blank=True, null=True)

    account_bank_name = models.CharField(max_length=50, blank=True, null=True)
    account_bank_number = models.IntegerField(max_length=16, blank=True, null=True)

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

    Personnel = models.ForeignKey(Personnel, related_name='personnel_family', on_delete=models.CASCADE)
    row = models.IntegerField()
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    national_code = models.IntegerField(max_length=10, unique=True, validators=[
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


class WorkshopPersonnel(BaseModel, LockableMixin, DefinableMixin):
    PART_TIME = 'p'
    FULL_TIME = 'f'

    CONTRACT_TYPES = (
        (PART_TIME, 'پاره وقت'),
        (FULL_TIME, 'تمام وقت')
    )

    CONTRACTUAL = 'c'
    PERMANENT = 'p'

    EMPLOYMENTS_TYPES = (
        (CONTRACTUAL, 'قراردادی'),
        (PERMANENT, 'رسمی')
    )

    workshop = models.ForeignKey(Workshop, related_name='workshop_personnel', on_delete=models.CASCADE)
    Personnel = models.ForeignKey(Personnel, related_name='workshop_personnel', on_delete=models.CASCADE)

    contract_from_date = jmodels.jDateField(blank=True, null=True)
    contract_to_date = jmodels.jDateField(blank=True, null=True)

    insurance = models.BooleanField(default=False)
    insurance_add_date = jmodels.jDateField(blank=True, null=True)
    work_title = models.CharField(blank=True, null=True)

    previous_insurance_history_out_workshop = models.IntegerField()
    previous_insurance_history_in_workshop = models.IntegerField()
    current_insurance_history_in_workshop = models.IntegerField()
    insurance_history_totality = models.IntegerField()

    job_position = models.CharField(max_length=100)
    job_group = models.CharField(max_length=100)
    job_location = models.CharField(max_length=100)
    job_location_status = models.CharField(max_length=100)

    employment_type = models.CharField(max_length=1, choices=EMPLOYMENTS_TYPES, default=CONTRACTUAL)
    contract_type = models.CharField(max_length=1, choices=CONTRACT_TYPES, default=FULL_TIME)
    employee_status = models.CharField(max_length=100)

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
