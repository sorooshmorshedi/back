from django.db import models
from django_jalali.db import models as jmodels
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

from companies.models import Company
from helpers.models import BaseModel, LockableMixin, DefinableMixin, POSTAL_CODE, DECIMAL, \
    is_valid_melli_code
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
    assignor_national_code = models.IntegerField(unique=True, validators=[is_valid_melli_code])
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
    NONE_PROFIT = 'NP'

    university_types = (
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

    personnel_code = models.IntegerField(unique=True, blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDER_TYPE, default=MALE)
    military_service = models.CharField(max_length=1, choices=MILITARY_SERVICE_STATUS, default=NOT_DONE)

    national_code = models.IntegerField(unique=True, blank=True, null=True)

    identity_code = models.IntegerField(unique=True, blank=True, null=True)
    date_of_birth = jmodels.jDateField(blank=True, null=True)
    date_of_exportation = jmodels.jDateField(blank=True, null=True)
    location_of_birth = models.CharField(max_length=50, blank=True, null=True)
    location_of_exportation = models.CharField(max_length=50, blank=True, null=True)
    sector_of_exportation = models.CharField(max_length=50, blank=True, null=True)

    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_TYPES, default=SINGLE)
    number_of_childes = models.IntegerField(default=0)

    city_phone_code = models.IntegerField(blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    mobile_number_1 = models.IntegerField(null=True, blank=True)
    mobile_number_2 = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    postal_code = POSTAL_CODE(null=True, blank=True)

    insurance = models.BooleanField(default=False)
    insurance_code = models.IntegerField(blank=True, null=True)

    degree_of_education = models.CharField(max_length=2, choices=DEGREE_TYPE, default=DIPLOMA)
    field_of_study = models.CharField(max_length=100, null=True, blank=True)
    university_type = models.CharField(max_length=2, choices=university_types, blank=True, null=True)
    university_name = models.CharField(max_length=50, blank=True, null=True)

    account_bank_name = models.CharField(max_length=50, blank=True, null=True)
    account_bank_number = models.IntegerField(blank=True, null=True)
    bank_cart_number = models.IntegerField(blank=True, null=True)
    sheba_number = models.IntegerField(blank=True, null=True)

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


class Contract(BaseModel, LockableMixin, DefinableMixin):
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

    workshop = models.ForeignKey(Workshop, related_name='contract', on_delete=models.CASCADE, blank=True, null=True)
    personnel = models.ForeignKey(Personnel, related_name='contract', on_delete=models.CASCADE, blank=True, null=True)
    contract_row = models.ManyToManyField(ContractRow, related_name='contract')

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

    contract_from_date = jmodels.jDateField()
    contract_to_date = jmodels.jDateField()
    quit_job_date = jmodels.jDateField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'Contact'
        permission_basename = 'contract'
        permissions = (
            ('get.workshop_personnel', 'مشاهده پرسنل کارگاه'),
            ('create.workshop_personnel', 'تعریف پرسنل کارگاه'),
            ('update.workshop_personnel', 'ویرایش پرسنل کارگاه'),
            ('delete.workshop_personnel', 'حذف پرسنل کارگاه'),

            ('getOwn.workshop_personnel', 'مشاهده پرسنل کارگاه خود'),
            ('updateOwn.workshop_personnel', 'ویرایش پرسنل کارگاه خود'),
            ('deleteOwn.workshop_personnel', 'حذف پرسنل کارگاه خود'),
        )


class HRLetter(BaseModel, LockableMixin, DefinableMixin):
    BASE_PAY = 'b'
    PENSION = 'p'
    UN_PENSION = 'u'

    NATURE_TYPES = (
        (BASE_PAY, 'حقوق پایه'),
        (PENSION, 'مستمر'),
        (UN_PENSION, 'غیر مستمر')
    )
    contract = models.ForeignKey(Contract, related_name='hr_letter', on_delete=models.CASCADE,
                                 blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_template = models.BooleanField(default=False)

    hoghooghe_roozane_use_tax = models.BooleanField()
    hoghooghe_roozane_use_insurance = models.BooleanField()
    hoghooghe_roozane_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    hoghooghe_roozane_amount = DECIMAL()

    paye_sanavat_use_tax = models.BooleanField()
    paye_sanavat_use_insurance = models.BooleanField()
    paye_sanavat_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    paye_sanavat_amount = DECIMAL()

    haghe_sarparasti_use_tax = models.BooleanField()
    haghe_sarparasti_use_insurance = models.BooleanField()
    haghe_sarparasti_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_sarparasti_amount = DECIMAL()

    haghe_modiriyat_use_tax = models.BooleanField()
    haghe_modiriyat_use_insurance = models.BooleanField()
    haghe_modiriyat_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_modiriyat_amount = DECIMAL()

    haghe_jazb_use_tax = models.BooleanField()
    haghe_jazb_use_insurance = models.BooleanField()
    haghe_jazb_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_jazb_amount = DECIMAL()

    fogholade_shoghl_use_tax = models.BooleanField()
    fogholade_shoghl_use_insurance = models.BooleanField()
    fogholade_shoghl_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    fogholade_shoghl_amount = DECIMAL()

    haghe_shift_use_tax = models.BooleanField()
    haghe_shift_use_insurance = models.BooleanField()
    haghe_shift_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_shift_amount = DECIMAL()

    fogholade_sakhti_kar_use_tax = models.BooleanField()
    fogholade_sakhti_kar_use_insurance = models.BooleanField()
    fogholade_sakhti_kar_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    fogholade_sakhti_kar_amount = DECIMAL()

    fogholade_nobat_kar_use_tax = models.BooleanField()
    fogholade_nobat_kar_use_insurance = models.BooleanField()
    fogholade_nobat_kar_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    fogholade_nobat_kar_amount = DECIMAL()

    fogholade_shab_kari_use_tax = models.BooleanField()
    fogholade_shab_kari_use_insurance = models.BooleanField()
    fogholade_shab_kari_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    fogholade_shab_kari_amount = DECIMAL()

    haghe_ankal_use_tax = models.BooleanField()
    haghe_ankal_use_insurance = models.BooleanField()
    haghe_ankal_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_ankal_amount = DECIMAL()

    fogholade_badi_abohava_use_tax = models.BooleanField()
    fogholade_badi_abohava_use_insurance = models.BooleanField()
    fogholade_badi_abohava_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    fogholade_badi_abohava_amount = DECIMAL()

    mahroomiat_tashilat_zendegi_use_tax = models.BooleanField()
    mahroomiat_tashilat_zendegi_use_insurance = models.BooleanField()
    mahroomiat_tashilat_zendegi_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    mahroomiat_tashilat_zendegi_amount = DECIMAL()

    fogholade_mahal_khedmat_use_tax = models.BooleanField()
    fogholade_mahal_khedmat_use_insurance = models.BooleanField()
    fogholade_mahal_khedmat_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    fogholade_mahal_khedmat_amount = DECIMAL()

    fogholade_sharayet_mohit_kar_use_tax = models.BooleanField()
    fogholade_sharayet_mohit_kar_use_insurance = models.BooleanField()
    fogholade_sharayet_mohit_kar_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    fogholade_sharayet_mohit_kar_amount = DECIMAL()

    haghe_maskan_use_tax = models.BooleanField()
    haghe_maskan_use_insurance = models.BooleanField()
    haghe_maskan_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_maskan_amount = DECIMAL()

    ayabo_zahab_use_tax = models.BooleanField()
    ayabo_zahab_use_insurance = models.BooleanField()
    ayabo_zahab_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    ayabo_zahab_amount = DECIMAL()

    bon_kharo_bar_use_tax = models.BooleanField()
    bon_kharo_bar_use_insurance = models.BooleanField()
    bon_kharo_bar_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    bon_kharo_bar_amount = DECIMAL()

    yarane_ghaza_use_tax = models.BooleanField()
    yarane_ghaza_use_insurance = models.BooleanField()
    yarane_ghaza_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    yarane_ghaza_amount = DECIMAL()

    haghe_shir_use_tax = models.BooleanField()
    haghe_shir_use_insurance = models.BooleanField()
    haghe_shir_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_shir_amount = DECIMAL()

    haghe_taahol_use_tax = models.BooleanField()
    haghe_taahol_use_insurance = models.BooleanField()
    haghe_taahol_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_taahol_amount = DECIMAL()

    poorsant_foroosh_use_tax = models.BooleanField()
    poorsant_foroosh_use_insurance = models.BooleanField()
    poorsant_foroosh_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    poorsant_foroosh_amount = DECIMAL()

    fogholade_afzayesh_bahrevari_tolid_use_tax = models.BooleanField()
    fogholade_afzayesh_bahrevari_tolid_use_insurance = models.BooleanField()
    fogholade_afzayesh_bahrevari_tolid_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    fogholade_afzayesh_bahrevari_tolid_amount = DECIMAL()

    fogholade_tolid_use_tax = models.BooleanField()
    fogholade_tolid_use_insurance = models.BooleanField()
    fogholade_tolid_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    fogholade_tolid_amount = DECIMAL()

    ezafe_kari_use_tax = models.BooleanField()
    ezafe_kari_use_insurance = models.BooleanField()
    ezafe_kari_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    ezafe_kari_amount = DECIMAL()

    jome_kari_use_tax = models.BooleanField()
    jome_kari_use_insurance = models.BooleanField()
    jome_kari_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    jome_kari_amount = DECIMAL()

    mazaya_gheyr_naqdi_pardakhti_kargaran_use_tax = models.BooleanField()
    mazaya_gheyr_naqdi_pardakhti_kargaran_use_insurance = models.BooleanField()
    mazaya_gheyr_naqdi_pardakhti_kargaran_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    mazaya_gheyr_naqdi_pardakhti_kargaran_amount = DECIMAL()

    haghe_lavazem_tahrir_use_tax = models.BooleanField()
    haghe_lavazem_tahrir_use_insurance = models.BooleanField()
    haghe_lavazem_tahrir_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_lavazem_tahrir_amount = DECIMAL()

    komakhazine_mahdekoodak_use_tax = models.BooleanField()
    komakhazine_mahdekoodak_use_insurance = models.BooleanField()
    komakhazine_mahdekoodak_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    komakhazine_mahdekoodak_amount = DECIMAL()

    komakhazine_varzesh_use_tax = models.BooleanField()
    komakhazine_varzesh_use_insurance = models.BooleanField()
    komakhazine_varzesh_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    komakhazine_varzesh_amount = DECIMAL()

    komakhazine_mobile_use_tax = models.BooleanField()
    komakhazine_mobile_use_insurance = models.BooleanField()
    komakhazine_mobile_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    komakhazine_mobile_amount = DECIMAL()

    haghe_owlad_use_tax = models.BooleanField()
    haghe_owlad_use_insurance = models.BooleanField()
    haghe_owlad_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_owlad_amount = DECIMAL()

    haghe_mamooriat_use_tax = models.BooleanField()
    haghe_mamooriat_use_insurance = models.BooleanField()
    haghe_mamooriat_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_mamooriat_amount = DECIMAL()

    zakhire_ayam_morakhasi_use_tax = models.BooleanField()
    zakhire_ayam_morakhasi_use_insurance = models.BooleanField()
    zakhire_ayam_morakhasi_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    zakhire_ayam_morakhasi_amount = DECIMAL()

    haghe_sanavat_use_tax = models.BooleanField()
    haghe_sanavat_use_insurance = models.BooleanField()
    haghe_sanavat_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    haghe_sanavat_amount = DECIMAL()

    eydi_salane_use_tax = models.BooleanField()
    eydi_salane_use_insurance = models.BooleanField()
    eydi_salane_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    eydi_salane_amount = DECIMAL()

    maskan_ba_asasiye_use_tax = models.BooleanField()
    maskan_ba_asasiye_use_insurance = models.BooleanField()
    maskan_ba_asasiye_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    maskan_ba_asasiye_amount = DECIMAL()

    maskan_bi_asasiye_use_tax = models.BooleanField()
    maskan_bi_asasiye_use_insurance = models.BooleanField()
    maskan_bi_asasiye_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    maskan_bi_asasiye_amount = DECIMAL()

    otomobil_shakhsi_ba_ranande_use_tax = models.BooleanField()
    otomobil_shakhsi_ba_ranande_use_insurance = models.BooleanField()
    otomobil_shakhsi_ba_ranande_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    otomobil_shakhsi_ba_ranande_amount = DECIMAL()

    otomobil_shakhsi_bi_ranande_use_tax = models.BooleanField()
    otomobil_shakhsi_bi_ranande_use_insurance = models.BooleanField()
    otomobil_shakhsi_bi_ranande_nature = models.CharField(max_length=1, choices=NATURE_TYPES)
    otomobil_shakhsi_bi_ranande_amount = DECIMAL()

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

    def save(self, *args, **kwargs):
        if self.is_template:
            self.contract = None
            if not self.name:
                ValidationError(message='برای قالب حکم کارگزینی خود نام وارد کنید')
        else:
            if not self.contract:
                ValidationError(message='قرارداد را وارد کنید')
        super().save(*args, **kwargs)
