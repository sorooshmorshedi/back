from django.db import models
from django.db.models import Q
from django_jalali.db import models as jmodels
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError

from companies.models import Company
from helpers.models import BaseModel, LockableMixin, DefinableMixin, DECIMAL, EXPLANATION
from payroll.verify_model import VerifyMixin
from users.models import City
import datetime
from decimal import Decimal
import jdatetime
import datetime


class WorkTitle(BaseModel):
    code = models.CharField(max_length=25)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' ' + self.code

    class Meta(BaseModel.Meta):
        verbose_name = 'WorkTitle'
        permission_basename = 'work_title'
        permissions = (
            ('create.city', 'تعریف عناوین شغلی'),

            ('get.city', 'مشاهده عناوین شغلی'),
            ('update.city', 'ویرایش عناوین شغلی'),
            ('delete.city', 'حذف عناوین شغلی'),

            ('getOwn.city', 'مشاهده عناوین شغلی های خود'),
            ('updateOwn.city', 'ویرایش شهر عناوین شغلی خود'),
            ('deleteOwn.city', 'حذف شهر عناوین شغلی خود'),
        )


class Workshop(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
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
    TYPE2 = 2
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
    workshop_code = models.CharField(max_length=50, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    employer_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    employer_insurance_contribution = models.IntegerField(default=3, blank=True, null=True)
    branch_code = models.CharField(max_length=100, blank=True, null=True)
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

    ezafe_kari_nerkh = models.DecimalField(max_digits=24, default=0.4, decimal_places=12)
    tatil_kari_nerkh = models.DecimalField(max_digits=24, default=0.96, decimal_places=12)
    kasre_kar_nerkh = models.DecimalField(max_digits=24, default=0.4, decimal_places=12)
    shab_kari_nerkh = models.DecimalField(max_digits=24, default=0.35, decimal_places=12)
    aele_mandi_nerkh = models.DecimalField(max_digits=24, default=3, decimal_places=12)
    nobat_kari_sob_asr_nerkh = models.DecimalField(max_digits=24, default=0.1, decimal_places=12)
    nobat_kari_sob_shab_nerkh = models.DecimalField(max_digits=24, default=0.225, decimal_places=12)
    nobat_kari_asr_shab_nerkh = models.DecimalField(max_digits=24, default=0.225, decimal_places=12)
    nobat_kari_sob_asr_shab_nerkh = models.DecimalField(max_digits=24, default=0.15, decimal_places=12)
    mission_pay_nerkh = models.DecimalField(max_digits=24, default=1, decimal_places=12)

    unemployed_insurance_nerkh = models.DecimalField(max_digits=24, default=0.03, decimal_places=12)
    worker_insurance_nerkh = models.DecimalField(max_digits=24, default=0.07, decimal_places=12)
    employee_insurance_nerkh = models.DecimalField(max_digits=24, default=0.2, decimal_places=12)

    haghe_sanavat_type = models.CharField(max_length=1, choices=HAGHE_SANAVAT_TYPES, default=CERTAIN)
    hade_aghal_hoghoogh = DECIMAL(default=1400000)

    made_86_nerkh = DECIMAL(default=0.1)
    hade_aksar_mashmool_bime = models.BooleanField(default=True)

    tax_employer_type = models.IntegerField(choices=TAX_EMPLOYER_TYPES, default=TYPE1)

    save_absence_limit = models.BooleanField(default=True)
    save_absence_transfer_next_year = models.BooleanField(default=False)

    illness_absence_in_real_work = models.BooleanField(default=False)

    is_active = models.BooleanField(blank=True, null=True)

    is_default = models.BooleanField(default=False)

    save_leave_limit = models.IntegerField(default=26)

    def save(self, *args, **kwargs):
        other = self.company.workshop.all()
        if len(other) == 0:
            self.is_default = True
        if self.is_default:
            for workshop in self.company.workshop.all():
                if workshop.id != self.id:
                    workshop.is_default = False
                    workshop.save()
        super().save(*args, **kwargs)

    @property
    def default_display(self):
        if self.is_default:
            return 'پیشفرض'
        else:
            return ' - '

    @property
    def workshop_title(self):
        if not self.name and not self.workshop_code:
            return 'ثبت اولیه ' + str(self.id)
        elif not self.name and self.workshop_code:
            return self.workshop_code
        elif not self.workshop_code and self.name:
            return self.name
        else:
            return self.name + ' ' + self.workshop_code

    @property
    def get_personnel(self):
        active_personnel = Personnel.objects.filter(Q(company=self.company) & Q(is_personnel_active=True) &
                                                    Q(is_personnel_verified=True))
        personnel = self.workshop_personnel.filter(Q(personnel__in=active_personnel) & Q(is_verified=True))
        if len(personnel) != 0:
            return personnel
        else:
            raise ValidationError('در این کارگاه پرسنلی ثبت نشده')

    @property
    def have_list(self):
        list_of_pays = self.list_of_pay.filter(ultimate=False)
        if len(list_of_pays) == 0:
            return False
        else:
            return True

    def get_tax_row(self, date):
        company_id = self.company.id
        taxs = WorkshopTax.objects.filter(company_id=company_id)
        if len(taxs) == 0:
            raise ValidationError('در این شرکت جدول معافیت مالیات ثبت نشده')
        month_tax = None
        for tax in taxs:
            if tax.from_date.__le__(date) and tax.to_date.__ge__(date):
                month_tax = tax
        if month_tax:
            return month_tax
        else:
            raise ValidationError('جدول معافیت مالیات در این تاریخ موجود نیست')

    @staticmethod
    def month_display(month):
        months = {
            1: 'فروردین',
            2: 'اردیبهشت',
            3: 'خرداد',
            4: 'تیر',
            5: 'مرداد',
            6: 'شهریور',
            7: 'مهر',
            8: 'آبان',
            9: 'آذر',
            10: 'دی',
            11: 'بهمن',
            12: 'اسفند',
        }
        return months[month]

    def absence_report(self, year, months):
        response = {}
        response['months'] = months
        response['year'] = year
        personnel = []
        personnel_ids = []
        for person in self.workshop_personnel.all():
            person_report = person.absence_report(year, months)
            person_report['id'] = person.id
            personnel.append(person_report)
        response['personnel'] = personnel
        response['personnel_ids'] = personnel_ids
        month_display = []
        for month in response['months']:
            month_display.append(self.month_display(month))
        response['months_display'] = month_display

        return response

    def save_leave_report(self, year, months):
        response = {}
        response['months'] = months
        response['year'] = year
        personnel = []
        personnel_ids = []
        for person in self.workshop_personnel.all():
            person_report = person.save_leave_report(year, months)
            person_report['id'] = person.id
            personnel.append(person_report)
        response['personnel'] = personnel
        response['personnel_ids'] = personnel_ids
        month_display = []
        for month in response['months']:
            month_display.append(self.month_display(month))
        response['months_display'] = month_display

        return response

    def eydi_report(self, year, months):
        response = {}
        response['months'] = months
        response['year'] = year
        personnel = []
        personnel_ids = []
        for person in self.workshop_personnel.all():
            personnel_ids.append(person.id)
            person_report = person.eydi_report(year, months)
            person_report['id'] = person.id
            personnel.append(person_report)
        response['personnel'] = personnel
        response['personnel_ids'] = personnel_ids
        month_display = []
        for month in response['months']:
            month_display.append(self.month_display(month))
        response['months_display'] = month_display

        return response

    def hagh_sanavat_report(self, year, months):
        response = {}
        response['months'] = months
        response['year'] = year
        personnel = []
        personnel_ids = []
        for person in self.workshop_personnel.all():
            personnel_ids.append(person.id)
            person_report = person.hagh_sanavat_report(year, months)
            person_report['id'] = person.id
            personnel.append(person_report)
        response['personnel'] = personnel
        response['personnel_ids'] = personnel_ids
        month_display = []
        for month in response['months']:
            month_display.append(self.month_display(month))
        response['months_display'] = month_display

        return response

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

    def __str__(self):
        if self.name:
            return self.name + ' ' + self.company.name
        elif not self.name:
            return str(self.id) + ' ' + self.company.name

    @property
    def active_display(self):
        if self.is_active:
            return 'فعال'
        else:
            return 'غیر فعال'


class WorkshopTax(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
    company = models.ForeignKey(Company, related_name='tax', on_delete=models.CASCADE, blank=True, null=True)

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
    is_last = models.BooleanField(default=False)

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

    @staticmethod
    def with_comma(input_amount):
        amount = str(round(input_amount))[::-1]
        loop = int(len(amount) / 3)
        if len(amount) < 4:
            return str(round(input_amount))
        else:
            counter = 0
            for i in range(1, loop + 1):
                index = (i * 3) + counter
                counter += 1
                amount = amount[:index] + ',' + amount[index:]
        if amount[-1] == ',':
            amount = amount[:-1]
        return amount[::-1]

    @property
    def monthly_from_amount_with_comma(self):
        if self.monthly_from_amount:
            return self.with_comma(self.monthly_from_amount)
        else:
            return 0

    @property
    def monthly_to_amount_with_comma(self):
        if self.monthly_to_amount:
            return self.with_comma(self.monthly_to_amount)
        else:
            return 0

    @property
    def to_amount_with_comma(self):
        if self.to_amount:
            return self.with_comma(self.to_amount)
        else:
            return 0

    @property
    def from_amount_with_comma(self):
        if self.from_amount:
            return self.with_comma(self.from_amount)
        else:
            return 0

    def __str__(self):
        return 'از ' + str(round(self.from_amount)) + ' تا ' + str(round(self.to_amount)) + ' : ' \
               + str(self.ratio) + ' % '

    def save(self, *args, **kwargs):
        query = WorkshopTaxRow.objects.filter(workshop_tax=self.workshop_tax)
        if len(query) < 1:
            self.from_amount = 0
            self.ratio = 0
        super().save(*args, **kwargs)


class ContractRow(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
    workshop = models.ForeignKey(Workshop, related_name='contract_rows', on_delete=models.CASCADE)
    contract_row = models.CharField(max_length=255, blank=True, null=True)
    contract_number = models.CharField(max_length=100, blank=True, null=True)
    registration_date = jmodels.jDateField(blank=True, null=True)
    from_date = jmodels.jDateField(blank=True, null=True)
    to_date = jmodels.jDateField(blank=True, null=True)
    initial_to_date = jmodels.jDateField(blank=True, null=True)
    topic = models.CharField(max_length=255, blank=True, null=True)

    status = models.BooleanField(blank=True, null=True)
    assignor_name = models.CharField(max_length=100, blank=True, null=True)
    assignor_national_code = models.CharField(max_length=20, blank=True, null=True)
    assignor_workshop_code = models.CharField(max_length=20, blank=True, null=True)
    amount = DECIMAL(blank=True, null=True)
    contract_initial_amount = DECIMAL(blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)

    use_in_insurance_list = models.BooleanField(default=False)

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
    def round_amount(self):
        return round(self.contract_initial_amount)

    @property
    def now_amount(self):
        if self.contract_initial_amount:
            if self.have_adjustment:
                adjustments = self.adjustment.all()
                amount = self.contract_initial_amount
                for adjustment in adjustments:
                    if adjustment.status != None:
                        if adjustment.status == True:
                            amount += adjustment.amount
                        else:
                            amount -= adjustment.amount
            else:
                amount = self.contract_initial_amount
        else:
            amount = 0
        return amount

    @property
    def now_date(self):
        date = None
        if self.have_adjustment:
            adjustments = self.adjustment.all()
            for adjustment in adjustments:
                if adjustment.change_date:
                    date = adjustment.change_date
                    break
        if date == None:
            date = self.initial_to_date
        return date

    @property
    def round_now_amount(self):
        if self.amount:
            return round(self.amount)
        else:
            return 0

    @staticmethod
    def with_comma(input_amount):
        amount = str(round(input_amount))[::-1]
        loop = int(len(amount) / 3)
        if len(amount) < 4:
            return str(round(input_amount))
        else:
            counter = 0
            for i in range(1, loop + 1):
                index = (i * 3) + counter
                counter += 1
                amount = amount[:index] + ',' + amount[index:]
        if amount[-1] == ',':
            amount = amount[:-1]
        return amount[::-1]

    @property
    def round_amount_with_comma(self):
        if self.contract_initial_amount:
            return self.with_comma(self.contract_initial_amount)
        else:
            return 0

    @property
    def round_now_amount_with_comma(self):
        if self.now_amount:
            return self.with_comma(self.now_amount)
        else:
            return 0

    @property
    def have_adjustment(self):
        if len(self.adjustment.all()) > 0:
            return True
        else:
            return False

    @property
    def title(self):
        return str(self.contract_row) + ' در کارگاه ' + self.workshop.name

    @property
    def status_display(self):
        if self.status:
            return 'فعال'
        else:
            return 'غیر فعال'

    @property
    def ads_display(self):
        if self.have_adjustment:
            return 'دارد'
        else:
            return 'ندارد'

    def save(self, *args, **kwargs):
        if not self.id:
            self.amount = self.contract_initial_amount
            self.to_date = self.initial_to_date

        super().save(*args, **kwargs)


class Adjustment(BaseModel, LockableMixin, DefinableMixin):
    contract_row = models.ForeignKey(ContractRow, related_name='adjustment', on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)
    date = jmodels.jDateField(blank=True, null=True)
    change_date = jmodels.jDateField(blank=True, null=True)
    explanation = EXPLANATION()
    status = models.BooleanField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'adjustment'
        permission_basename = 'adjustment'
        permissions = (
            ('get.adjustment', 'مشاهده تعدیل'),
            ('create.adjustment', 'تعریف تعدیل'),
            ('update.adjustment', 'ویرایش تعدیل'),
            ('delete.adjustment', 'حذف تعدیل'),

            ('getOwn.adjustment', 'مشاهده تعدیل خود'),
            ('updateOwn.adjustment', 'ویرایش تعدیل خود'),
            ('deleteOwn.adjustment', 'حذف تعدیل خود'),
        )

    def __str__(self):
        return 'تعدیل برای ' + self.contract_row.title

    @property
    def status_display(self):
        if self.status:
            return 'افزایشی'
        if self.status == False:
            return 'کاهشی'
        else:
            return ''

    @property
    def change_date_display(self):
        if self.change_date:
            return self.change_date.__str__()
        else:
            return '-'

    @staticmethod
    def with_comma(input_amount):
        amount = str(round(input_amount))[::-1]
        loop = int(len(amount) / 3)
        if len(amount) < 4:
            return str(round(input_amount))
        else:
            counter = 0
            for i in range(1, loop + 1):
                index = (i * 3) + counter
                counter += 1
                amount = amount[:index] + ',' + amount[index:]
        if amount[-1] == ',':
            amount = amount[:-1]
        return amount[::-1]

    @property
    def amount_with_comma(self):
        if self.amount:
            return self.with_comma(self.amount)
        else:
            return 0

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = jdatetime.date.today()
        if self.amount and self.status == None:
            raise ValidationError('نوع تعدیل را وارد کنید')
        if not self.amount and not self.change_date:
            raise ValidationError('تاریخ تغییر یا مبلغ تغییر را وارد کنید')
        super().save(*args, **kwargs)


class Personnel(BaseModel, LockableMixin, DefinableMixin):
    IRANIAN = 1
    OTHER = 2

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
        (NONE, 'هیچ کدام')

    )
    BANSAR = 'BANSAR'
    BCDEVE = 'BCDEVE'
    BCITY = 'BCITY'
    BDAY = 'BDAY'
    BEDIRA = 'BEDIRA'
    BEGHTE = 'BEGHTE'
    BGHARZ = 'BGHARZ'
    BHEKMA = 'BHEKMA'
    BINDMI = 'BINDMI'
    BKARAF = 'BKARAF'
    BKESHA = 'BKESHA'
    BMASKA = 'BMASKA'
    BMELLA = 'BMELLA'
    BMELLI = 'BMELLI'
    BPARSI = 'BPARSI'
    BPASAR = 'BPASAR'
    BPOST = 'BPOST'
    BREFAH = 'BREFAH'
    BSADER = 'BSADER'
    BSAMAN = 'BSAMAN'
    BSARMA = 'BSARMA'
    BSEPAH = 'BSEPAH'
    BSINA = 'BSINA'
    BTEJAR = 'BTEJAR'
    BTOURI = 'BTOURI'
    BRESALA = 'BRESALA'
    BAYAN = 'BAYAN'
    CHART = 'CHART'
    EURO = 'EURO'
    KHAVA = 'KHAVA'
    VENE = 'VENE'
    ESLA = 'ESLA'
    FUTU = 'FUTU'
    CASP = 'CASP'
    TOSE = 'TOSE'
    MELAL = 'MELAL'
    NOR = 'NOR'
    ZAMIN = 'ZAMIN'

    BANK_NAMES = (
        (BCDEVE, 'بانک توسعه تعاون'),
        (BCITY, 'بانک شهر'),
        (BDAY, 'بانک دی'),
        (BEDIRA, 'بانک توسعه صادرات  ایران'),
        (BEGHTE, 'بانک اقتصاد نوین'),
        (BGHARZ, 'بانک قرض الحسنه مهر ایران'),
        (BINDMI, 'بانک صنعت و معدن'),
        (BKARAF, 'بانک کارآفرین'),
        (BKESHA, 'بانک کشاورزی'),
        (BMASKA, 'بانک مسکن'),
        (BMELLA, 'بانک ملت'),
        (BMELLI, 'بانک  ملی ایران'),
        (BPARSI, 'بانک پارسیان'),
        (BPASAR, 'بانک پاسارگاد'),
        (BPOST, 'پست بانک'),
        (BREFAH, 'بانک  رفاه کارگران'),
        (BSADER, 'بانک صادرات'),
        (BSAMAN, 'بانک سامان'),
        (BSARMA, 'بانک سرمایه'),
        (BSEPAH, 'بانک  سپه'),
        (BSINA, 'بانک سینا'),
        (BTEJAR, 'بانک تجارت'),
        (BTOURI, 'بانک  گردشگری'),
        (BRESALA, 'بانک قرض الحسنه رسالت'),
        (BAYAN, 'بانک آینده'),
        (CHART, 'استاندارد چارترد'),
        (EURO, 'بانک تجاری ایران و اروپا'),
        (KHAVA, 'بانک خاورمیانه'),
        (VENE, 'بانک مشترک ایران - ونزوئلا'),
        (ESLA, 'تعاون اسلامی برای سرمایه‌گذاری'),
        (FUTU, 'فیوچر بانک (المستقبل)'),
        (CASP, 'مؤسسه اعتباری غیربانکی کاسپین '),
        (TOSE, 'مؤسسه اعتباری غیربانکی توسعه '),
        (MELAL, 'مؤسسه اعتباری غیربانکی ملل '),
        (NOR, 'مؤسسه اعتباری غیربانکی نور '),
        (ZAMIN, 'بانک ایران زمین'),

    )

    SINGLE = 's'
    MARRIED = 'm'
    CHILDREN_WARDSHIP = 'c'

    MARITAL_STATUS_TYPES = (
        (SINGLE, 'مجرد'),
        (MARRIED, 'متاهل'),
        (CHILDREN_WARDSHIP, 'سرپرست فرزند')
    )

    NO_EDUCATE = 1
    UNDER_DIPLOMA = 2
    DIPLOMA = 3
    ASSOCIATES = 4
    BACHELOR = 5
    MASTER = 6
    DOCTORAL = 7
    POSTDOCTORAL = 8

    DEGREE_TYPE = (
        (NO_EDUCATE, 'کم سواد'),
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
    ELMI = 'el'
    PAYAM = 'pa'
    PARDIS = 'pr'

    UNIVERSITY_TYPES = (
        (STATE, 'دولتی'),
        (OPEN, 'آزاد'),
        (NONE_PROFIT, 'غیر انتفاعی'),
        (ELMI, 'علمی کاربردی'),
        (PAYAM, 'پیام نور'),
        (PARDIS, 'پردیس خودگردان وابسته به دولت'),
    )

    company = models.ForeignKey(Company, related_name='personnel', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.IntegerField(choices=NATIONALITY_TYPE, blank=True, null=True)

    personnel_code = models.CharField(max_length=10, blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDER_TYPE, blank=True, null=True)
    military_service = models.CharField(max_length=1, choices=MILITARY_SERVICE_STATUS, blank=True, null=True)

    national_code = models.CharField(max_length=15, blank=True, null=True)

    identity_code = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = jmodels.jDateField(blank=True, null=True)
    date_of_exportation = jmodels.jDateField(blank=True, null=True)

    location_of_birth = models.CharField(max_length=100, null=True, blank=True)
    location_of_birth_code = models.CharField(max_length=100, null=True, blank=True)
    location_of_foreign_birth = models.CharField(max_length=255, null=True, blank=True)
    location_of_exportation = models.CharField(max_length=100, blank=True, null=True)
    location_of_exportation_code = models.CharField(max_length=100, blank=True, null=True)
    sector_of_exportation = models.CharField(max_length=100, blank=True, null=True)
    sector_of_exportation_code = models.CharField(max_length=100, blank=True, null=True)

    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_TYPES, blank=True, null=True)
    number_of_childes = models.IntegerField(default=0)

    city_phone_code = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    mobile_number_1 = models.CharField(max_length=50, blank=True, null=True)
    mobile_number_2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    city_code = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)

    insurance = models.BooleanField(default=False)
    insurance_code = models.CharField(max_length=255, blank=True, null=True)

    degree_education = models.IntegerField(choices=DEGREE_TYPE, blank=True, null=True)
    field_of_study = models.CharField(max_length=100, null=True, blank=True)
    university_type = models.CharField(max_length=2, choices=UNIVERSITY_TYPES, blank=True, null=True)
    university_name = models.CharField(max_length=50, blank=True, null=True)

    account_bank_name = models.CharField(max_length=10, choices=BANK_NAMES, blank=True, null=True)
    account_bank_number = models.CharField(max_length=50, blank=True, null=True)
    bank_cart_number = models.CharField(max_length=50, blank=True, null=True)
    sheba_number = models.CharField(max_length=50, blank=True, null=True)

    is_personnel_active = models.BooleanField(null=True, blank=True)
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

    @staticmethod
    def with_comma(input_amount, no_minus=False):
        if input_amount != 0:
            amount = str(round(input_amount))[::-1]
            loop = int(len(amount) / 3)
            if len(amount) < 4:
                return str(round(input_amount))
            else:
                counter = 0
                for i in range(1, loop + 1):
                    index = (i * 3) + counter
                    counter += 1
                    amount = amount[:index] + ',' + amount[index:]
            if amount[-1] == ',':
                amount = amount[:-1]
            if no_minus:
                return amount[::-1].replace('-', '')
            return amount[::-1]
        else:
            return 0

    def is_in_workshop(self, pk):
        workshop_personnel = WorkshopPersonnel.objects.filter(Q(personnel_id=self.id) & Q(is_verified=True)
                                                              & Q(workshop=pk))
        if len(workshop_personnel) > 0:
            return True
        else:
            return False

    @property
    def child_number(self):

        childes = PersonnelFamily.objects.filter(
            Q(personnel_id=self.id) &
            Q(relative='c') &
            Q(is_active=True) &
            Q(is_verified=True)
        )
        return len(childes)

    @property
    def childs(self):

        childes = PersonnelFamily.objects.filter(
            Q(personnel_id=self.id) &
            Q(relative='c') &
            Q(is_active=True) &
            Q(is_verified=True)
        )
        return childes

    @property
    def full_name(self):
        if self.name and self.last_name:
            return self.name + ' ' + self.last_name
        elif self.name:
            return self.name
        elif self.last_name:
            return self.last_name
        else:
            return str(self.id)

    @property
    def insurance_for_tax(self):
        if self.insurance:
            return 2
        else:
            return 5

    @property
    def insurance_display(self):
        if self.insurance:
            return 'دارد'
        else:
            return 'ندارد'

    @property
    def verify_display(self):
        if self.is_personnel_verified:
            return 'نهایی'
        else:
            return 'اولیه'

    @property
    def active_display(self):
        if self.is_personnel_active:
            return 'فعال'
        else:
            return 'غیر فعال'

    @property
    def system_code(self):
        try:
            company_personnel = Personnel.objects.filter(company=self.company).first()
            personnel_code = int(company_personnel.personnel_code)
            code = str(personnel_code + 1)
        except:
            code = '100'
        return code

    def save(self, *args, **kwargs):
        if not self.id and not self.personnel_code:
            self.personnel_code = self.system_code
        if self.gender == 'f':
            self.military_service == 'x'
        if self.degree_education == 1 or self.degree_education == 2 or self.degree_education == 3:
            self.university_type = None
            self.university_name = None
        super().save(*args, **kwargs)


class PersonnelFamily(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
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
        (MAIM, 'نقص عضو')
    )

    personnel = models.ForeignKey(Personnel, related_name='personnel_family', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    national_code = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = jmodels.jDateField(blank=True, null=True)
    relative = models.CharField(max_length=1, choices=RELATIVE_TYPE, blank=True, null=True)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_TYPES, blank=True, null=True)
    military_service = models.CharField(max_length=1, choices=MILITARY_SERVICE_STATUS, blank=True, null=True)
    study_status = models.CharField(max_length=1, choices=STUDY_TYPE, blank=True, null=True)
    physical_condition = models.CharField(max_length=1, choices=PHYSICAL_TYPE, blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDER_TYPE, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)

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
    def active_display(self):
        if self.is_active:
            return 'فعال'
        else:
            return 'غیر فعال'

    @property
    def full_name(self):
        if self.name and self.last_name:
            return self.name + ' ' + self.last_name
        elif self.name:
            return self.name
        elif self.last_name:
            return self.last_name
        else:
            return str(self.id)


class WorkshopPersonnel(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
    PART_TIME = 2
    FULL_TIME = 1
    TEMPORARY = 3
    HOURLY = 5
    CONTRACTUAL = 4

    CONTRACT_TYPES = (
        (PART_TIME, 'پاره وقت'),
        (FULL_TIME, 'تمام وقت'),
        (TEMPORARY, 'موقت'),
        (HOURLY, 'ساعتی'),
        (CONTRACTUAL, 'پیمانی')
    )

    CONVENTIONAL = 1
    CORPORATE = 2
    PERMANENT = 3
    CONTRACTUAL = 4
    FUNCTIONARY = 5
    OTHERS = 6

    EMPLOYMENTS_TYPES = (
        (CONTRACTUAL, 'پیمانی'),
        (CONVENTIONAL, 'قراردادی'),
        (CORPORATE, 'َشرکتی'),
        (FUNCTIONARY, 'مامور'),
        (PERMANENT, 'رسمی'),
        (OTHERS, 'سایر')

    )

    NORMAL = 1
    STUNTMAN = 2
    FALLEN_CHILD = 3
    FREEDMAN = 4
    ARM = 5
    BAND_14 = 6
    FOREIGN = 7

    EMPLOYEE_TYPES = (
        (NORMAL, 'عادی'),
        (STUNTMAN, 'جانباز'),
        (FALLEN_CHILD, 'فرزند شهید'),
        (FREEDMAN, 'آزاده'),
        (ARM, 'نیروهای مسلح'),
        (BAND_14, 'سایر مشمولین بند14ماده91'),
        (FOREIGN, ' قانون اجتناب از اخذ مالیات مضاعف اتباع خارجی مشمول')
    )

    NORMAL = 1
    UN_DEVOLOPED = 2
    FREE_ZONE = 3

    JOB_LOCATION_STATUSES = (
        (NORMAL, 'عادی'),
        (UN_DEVOLOPED, 'مناطق کمتر توسعه یافته'),
        (FREE_ZONE, 'مناطق آزاد تجاری'),
    )

    STUDY = 2
    FINANCIAL = 1
    SOCIAL = 3
    IT = 4
    HEALTH = 5
    ENGINEER = 6
    SERVICES = 7
    ARGI = 8
    SALE = 9
    SECURITY = 10
    WORKER = 11
    TRANSFORM = 12
    PRODUCT = 13
    CONTROL = 14
    SEARCH = 15
    WAREHOUSE = 16
    JUDGE = 17
    MASTER = 18
    OTHER = 0

    JOB_GROUP_TYPES = (
        (STUDY, 'آموزشی و فرهنگی'),
        (FINANCIAL, 'اداری و مالی'),
        (SOCIAL, 'اموراجتماعی'),
        (HEALTH, 'درمانی و بهداشتی'),
        (IT, 'اطلاعات فناوری'),
        (SERVICES, 'خدمات'),
        (ENGINEER, 'فنی و مهندسي'),
        (ARGI, 'كشاورزی ومحيط زيست'),
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

    workshop = models.ForeignKey(Workshop, related_name='workshop_personnel', on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, related_name='workshop_personnel', on_delete=models.CASCADE)

    employment_date = jmodels.jDateField(blank=True, null=True)
    insurance_add_date = jmodels.jDateField(blank=True, null=True)

    title = models.ForeignKey(WorkTitle, related_name='workshop_personnel', on_delete=models.SET_NULL,
                              blank=True, null=True)
    previous_insurance_history_out_workshop = models.IntegerField(blank=True, null=True)
    previous_insurance_history_in_workshop = models.IntegerField(blank=True, null=True)

    job_position = models.CharField(max_length=100, blank=True, null=True)
    job_group = models.IntegerField(choices=JOB_GROUP_TYPES, blank=True, null=True)
    job_location = models.CharField(max_length=100, blank=True, null=True)
    job_location_status = models.IntegerField(choices=JOB_LOCATION_STATUSES, blank=True, null=True)

    employment_type = models.IntegerField(choices=EMPLOYMENTS_TYPES, blank=True, null=True)
    contract_type = models.IntegerField(choices=CONTRACT_TYPES, blank=True, null=True)
    employee_status = models.IntegerField(choices=EMPLOYEE_TYPES, blank=True, null=True)

    save_leaave = models.IntegerField(default=0)

    sanavat_btn = models.BooleanField(default=False)
    sanavat_previuos_days = models.CharField(max_length=100, blank=True, null=True)
    sanavat_previous_amount = models.CharField(max_length=100, blank=True, null=True)

    save_leave_limit = models.IntegerField(default=26)

    @property
    def current_insurance(self):
        if self.personnel.insurance:
            lists = self.workshop.list_of_pay.filter(Q(ultimate=True) & Q(use_in_calculate=True))
            items = self.list_of_pay_item.filter(list_of_pay__in=lists)
            total = 0
            for item in items:
                is_insurance, worktime = item.check_insurance
                if is_insurance:
                    total += (item.real_worktime + item.illness_leave_day) / item.list_of_pay.month_days
            return round(total, 2)
        else:
            return 0

    @property
    def total_insurance(self):
        if self.personnel.insurance and self.previous_insurance_history_in_workshop:
            return self.current_insurance + self.previous_insurance_history_in_workshop
        elif self.personnel.insurance and not self.previous_insurance_history_in_workshop:
            return self.current_insurance
        else:
            return 0

    @property
    def insurance_history_total(self):
        if self.personnel.insurance and self.previous_insurance_history_out_workshop:
            return self.total_insurance + self.previous_insurance_history_out_workshop
        elif self.personnel.insurance and not self.previous_insurance_history_out_workshop:
            return self.total_insurance
        else:
            return 0

    @property
    def quit_job_date(self):
        for contract in self.contract.filter(is_verified=True):
            if contract.quit_job_date:
                return True
        return False

    @property
    def un_verifiable(self):
        contracts = self.contract.filter(is_verified=True)
        if len(contracts) == 0:
            return False
        else:
            return True

    @property
    def payment_balance(self):
        response = []
        for item in self.list_of_pay_item.filter(list_of_pay__ultimate=True):
            if item.list_of_pay.pay_done and item.paid_amount > 0:
                month = {}
                month['amount'] = 0
                month['amount_comma'] = 0
                month['paid'] = item.paid_amount
                month['paid_comma'] = self.with_comma(item.paid_amount, True)
                month['upaid'] = item.unpaid
                month['unpaid_comma'] = self.with_comma(item.unpaid, True)
                month['date'] = item.list_of_pay.bank_pay_date
                month['bank_date'] = item.list_of_pay.bank_pay_date
                month['total'] = item.total_unpaid
                month['total_comma'] = self.with_comma((item.total_unpaid - item.paid_amount), True)
                month['explanation'] = 'پرداخت حقوق'
                response.append(month)
            month = {}
            month['amount'] = item.payable
            month['amount_comma'] = self.with_comma(item.payable, True)
            month['paid'] = 0
            month['paid_comma'] = 0
            month['upaid'] = item.payable
            month['upaid_comma'] = self.with_comma(item.payable, True)
            month['date'] = item.list_of_pay.end_date
            month['bank_date'] = ' ---- '
            month['total'] = item.total_unpaid
            month['total_comma'] = self.with_comma(item.total_unpaid, True)

            month['explanation'] = 'شناسایی حقوق پرداختنی {} سال {}'.format(item.list_of_pay.month_display,
                                                                            item.list_of_pay.year)
            response.append(month)
        print(response.reverse())
        return response

    @property
    def balance_total(self):
        paid = 0
        amount = 0
        for item in self.payment_balance:
            paid += item['paid']
            amount += item['amount']
        mande = round(amount - paid)
        total = {
            'paid_total': self.with_comma(paid),
            'amount_total': self.with_comma(amount),
            'mande': self.with_comma(mande),
        }
        return total

    @property
    def real_work(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.real_worktime
        return total

    @property
    def my_title(self):
        return self.personnel.full_name + ' در کارگاه ' + self.workshop.name

    @property
    def last_haghe_owlad(self):
        return self.list_of_pay_item.first().aele_mandi

    @property
    def quit_job(self):
        response = False
        contracts = self.contract.all()
        for contract in contracts:
            if contract.quit_job_date:
                response = contract.quit_job_date
        return response

    @property
    def absence_total(self):
        return len(self.leave.all())

    @property
    def get_save_leave(self):
        item = ListOfPayItem.objects.filter(workshop_personnel=self.id).first()
        day_amount = item.get_save_leave_day_amount
        day = item.get_save_leave_day
        amount = item.get_save_leave_amount
        day += self.save_leaave
        return round((day * day_amount) + amount)

    @property
    def get_eydi(self):
        item = ListOfPayItem.objects.filter(workshop_personnel=self.id).first()
        eydi = item.calculate_yearly_eydi - item.calculate_yearly_eydi_tax
        return round(eydi)

    @property
    def get_haghe_sanavat(self):
        item = ListOfPayItem.objects.filter(workshop_personnel=self.id).first()
        return round(item.calculate_yearly_haghe_sanavat)

    @property
    def settlement(self):
        response = {}
        bes = {}
        bed = {}
        total_hoghoogh = 0
        for item in self.list_of_pay_item.all():
            total_hoghoogh += item.payable
            total_hoghoogh -= item.paid_amount
        bes['hoghoogh'] = total_hoghoogh
        bes['total_save_leave'] = self.get_save_leave
        bes['total'] = total_hoghoogh + self.get_save_leave + self.get_eydi + self.get_haghe_sanavat
        if self.workshop.haghe_sanavat_identification == 'y':
            response['identification'] = True
            bes['eydi'] = self.get_eydi
            bes['haghe_sanavat'] = self.get_haghe_sanavat

        else:
            response['identification'] = False

        loans = self.loan.all()
        deductions = self.deduction.all()
        bed['loan'] = 0
        bed['dept'] = 0
        bed['deduction'] = 0
        for loan in loans:
            if not loan.pay_done and loan.loan_type == 'l':
                bed['loan'] += loan.settlement
            elif not loan.pay_done and loan.loan_type == 'd':
                bed['dept'] += loan.settlement
        for deduction in deductions:
            bed['deduction'] += deduction.settlement
        bed['total'] = bed['deduction'] + bed['dept'] + bed['loan']
        contract = self.contract.first()
        hr_letter = HRLetter.objects.filter(contract=contract.id).first()
        hr = {}
        hr['base_pay'] = hr_letter.hoghooghe_roozane_amount
        hr['bon_kargari'] = hr_letter.bon_kharo_bar_amount
        hr['fogholade'] = hr_letter.fogholade_sakhti_kar_amount
        hr['hagh_maskan'] = hr_letter.haghe_maskan_amount
        hr['ayab_zahab'] = hr_letter.ayabo_zahab_amount
        hr['hagh_owlad'] = hr_letter.get_aele_mandi_amount

        response['hr'] = hr_letter
        response['bed'] = bed
        response['bes'] = bes
        response['total'] = bes['total'] - bed['total']
        return response

    def absence_report(self, year, months_list):
        response = {}
        months = {}
        by_month = []

        for month in months_list:
            item = ListOfPayItem.objects.filter(Q(workshop_personnel__id=self.id) & Q(list_of_pay__year=year)
                                                & Q(list_of_pay__month=month) & Q(list_of_pay__ultimate=True)).first()
            report = {}
            if item:
                report['display'] = item.list_of_pay.month_display
                report['limit'] = Decimal(26 / 12 * len(months_list))
                report['matter_73_limit'] = Decimal(item.matter_47_leave_day)
                report['total_limit'] = report['limit'] + report['matter_73_limit']
                report['save_limit'] = Decimal(9 / 12 * len(months_list))
                report['entitlement'] = Decimal(item.entitlement_leave_day)
                report['matter_73'] = Decimal(item.matter_47_leave_day)
                report['without_salary'] = Decimal(item.without_salary_leave_day)
                report['illness'] = Decimal(item.illness_leave_day)
                report['absence'] = Decimal(item.absence_day)
            else:
                report['display'] = 0
                report['limit'] = Decimal(26 / 12 * len(months_list))
                report['matter_73_limit'] = Decimal(0)
                report['total_limit'] = Decimal(26 / 12 * len(months_list))
                report['save_limit'] = Decimal(9 / 12 * len(months_list))
                report['entitlement'] = Decimal(0)
                report['matter_73'] = Decimal(0)
                report['without_salary'] = Decimal(0)
                report['illness'] = Decimal(0)
                report['absence'] = Decimal(0)
                report['remaining'] = Decimal(26 / 12 * len(months_list))
            by_month.append(report)

        response['total'] = {
            'name': self.personnel.full_name,
            'limit': 0,
            'matter_73_limit': 0,
            'total_limit': 0,
            'save_limit': 0,
            'entitlement': 0,
            'matter_73': 0,
            'without_salary': 0,
            'illness': 0,
            'absence': 0,
            'remaining': 0,
        }

        for month in by_month:
            response['total']['limit'] = round((response['total']['limit'] + month['limit']), 2)
            response['total']['matter_73_limit'] = round((response['total']['matter_73_limit'] +
                                                          month['matter_73_limit']), 2)
            response['total']['total_limit'] = round((response['total']['total_limit'] +
                                                      month['total_limit']), 2)
            response['total']['save_limit'] = round((response['total']['save_limit'] +
                                                     month['save_limit']), 2)
            response['total']['entitlement'] = round((response['total']['entitlement'] +
                                                      month['entitlement']), 2)
            response['total']['matter_73'] = round((response['total']['matter_73'] + month['matter_73']), 2)
            response['total']['without_salary'] = round((response['total']['without_salary'] +
                                                         month['without_salary']), 2)
            response['total']['illness'] = round((response['total']['illness'] + month['illness']), 2)
            response['total']['absence'] = round((response['total']['absence'] + month['absence']), 2)
            response['total']['remaining'] = response['total']['total_limit'] - \
                                             response['total']['entitlement'] - response['total']['matter_73']
        response['months'] = by_month

        return response

    def save_leave_report(self, year, months_list):
        response = {}
        months = {}
        by_month = []
        day_amount = 0
        for month in months_list:
            item = ListOfPayItem.objects.filter(Q(workshop_personnel__id=self.id) & Q(list_of_pay__year=year)
                                                & Q(list_of_pay__month=month) & Q(list_of_pay__ultimate=True)).first()
            report = {}
            if item:
                report['display'] = item.list_of_pay.month_display
                report['limit'] = Decimal(26 / 12 * len(months_list))
                report['matter_73_limit'] = Decimal(item.matter_47_leave_day)
                report['total_limit'] = report['limit'] + report['matter_73_limit']
                report['save_limit'] = Decimal(9 / 12 * len(months_list))
                report['entitlement'] = Decimal(item.entitlement_leave_day)
                report['matter_73'] = Decimal(item.matter_47_leave_day)
                report['total_leave'] = report['entitlement'] + report['matter_73']
                report['remaining'] = Decimal(26 / 12 * len(months_list))
                day_amount = item.get_save_leave_day_amount

            else:
                report['display'] = 0
                report['limit'] = Decimal(26 / 12 * len(months_list))
                report['matter_73_limit'] = Decimal(0)
                report['total_limit'] = Decimal(26 / 12 * len(months_list))
                report['save_limit'] = Decimal(9 / 12 * len(months_list))
                report['entitlement'] = Decimal(0)
                report['matter_73'] = Decimal(0)
                report['total_leave'] = Decimal(0)
                report['remaining'] = Decimal(26 / 12 * len(months_list))

            by_month.append(report)

        response['total'] = {
            'name': self.personnel.full_name,
            'limit': 0,
            'matter_73_limit': 0,
            'total_limit': 0,
            'save_limit': 0,
            'entitlement': 0,
            'matter_73': 0,
            'total_leave': 0,
            'remaining': 0,
            'day_amount': 0,
            'amount': 0,
        }

        for month in by_month:
            response['total']['limit'] = round((response['total']['limit'] + month['limit']), 2)
            response['total']['matter_73_limit'] = round((response['total']['matter_73_limit'] +
                                                          month['matter_73_limit']), 2)
            response['total']['total_limit'] = round((response['total']['total_limit'] +
                                                      month['total_limit']), 2)
            response['total']['save_limit'] = round((response['total']['save_limit'] +
                                                     month['save_limit']), 2)
            response['total']['entitlement'] = round((response['total']['entitlement'] +
                                                      month['entitlement']), 2)
            response['total']['matter_73'] = round((response['total']['matter_73'] + month['matter_73']), 2)
            response['total']['total_leave'] = round((response['total']['total_leave'] + month['total_leave']), 2)
            response['total']['remaining'] = response['total']['total_limit'] - \
                                             response['total']['entitlement'] - response['total']['matter_73']

        response['months'] = by_month
        response['total']['day_amount'] = day_amount
        response['total']['amount'] = day_amount * response['total']['remaining']

        return response

    def eydi_report(self, year, months_list):
        response = {}
        by_month = []
        for month in months_list:
            item = ListOfPayItem.objects.filter(Q(workshop_personnel__id=self.id) & Q(list_of_pay__year=year)
                                                & Q(list_of_pay__month=month) & Q(list_of_pay__ultimate=True)).first()
            report = {}
            if item:
                report['display'] = item.list_of_pay.month_display
                report['eydi'] = item.padash_total

            else:
                report['display'] = 0
                report['eydi'] = 0

            by_month.append(report)

        response['total'] = {
            'name': self.personnel.full_name,
            'total': 0,
        }

        for month in by_month:
            response['total']['total'] = round((response['total']['total'] + month['eydi']), 2)

        response['months'] = by_month
        return response

    def hagh_sanavat_report(self, year, months_list):
        response = {}
        by_month = []
        for month in months_list:
            item = ListOfPayItem.objects.filter(Q(workshop_personnel__id=self.id) & Q(list_of_pay__year=year)
                                                & Q(list_of_pay__month=month) & Q(list_of_pay__ultimate=True)).first()
            report = {}
            if item:
                report['display'] = item.list_of_pay.month_display
                report['sanavat'] = item.haghe_sanavat_total

            else:
                report['display'] = 0
                report['sanavat'] = 0

            by_month.append(report)

        response['total'] = {
            'name': self.personnel.full_name,
            'total': 0,
        }

        for month in by_month:
            response['total']['total'] = round((response['total']['total'] + month['sanavat']), 2)

        response['months'] = by_month
        return response

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

    @property
    def get_insurance_in_workshop(self):
        return self.total_insurance

    def save(self, *args, **kwargs):
        if self.sanavat_btn == False:
            self.sanavat_previous_amount = None
            self.sanavat_previuos_days = None
        if not self.id:
            self.current_insurance_history_in_workshop = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.my_title


class Contract(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name='contract',
                                           on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    insurance = models.BooleanField(default=False)
    insurance_add_date = jmodels.jDateField(blank=True, null=True)
    insurance_number = models.CharField(max_length=100, blank=True, null=True)
    contract_from_date = jmodels.jDateField(blank=True, null=True)
    contract_to_date = jmodels.jDateField(blank=True, null=True)
    quit_job_date = jmodels.jDateField(blank=True, null=True)

    tax = models.BooleanField(default=False)
    tax_add_date = jmodels.jDateField(blank=True, null=True)

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
        if self.is_verified and self.insurance != None and self.insurance:
            if not self.insurance_add_date:
                raise ValidationError('تاریخ اضافه شدن به لیست بیمه را وارد کنید')
            if not self.insurance_number:
                raise ValidationError('شماره بیمه را وارد کنید')

        if self.is_verified and self.tax != None and self.tax:
            if not self.tax_add_date:
                raise ValidationError('تاریخ اضافه شدن به لیست مالیات را وارد کنید')

        if self.is_verified and self.quit_job_date and self.quit_job_date.__le__(self.contract_from_date):
            raise ValidationError('تاریخ ترک کار باید بعد از تاریخ شروع قرارداد باشد')

        if self.is_verified and self.insurance_add_date and self.insurance_add_date.__lt__(self.contract_from_date):
            raise ValidationError('تاریخ اضافه شدن به لیست بیمه باید بعد از تاریخ شروع قرارداد باشد')
        if self.is_verified and self.tax_add_date and self.tax_add_date.__lt__(self.contract_from_date):
            raise ValidationError('تاریخ اضافه شدن به لیست مالیات باید بعد از تاریخ شروع قرارداد باشد')
        if self.is_verified:
            self.workshop_personnel.personnel.insurance = self.insurance
            self.workshop_personnel.personnel.insurance_code = self.insurance_number
            self.workshop_personnel.personnel.save()
        super().save(*args, **kwargs)

    @property
    def workshop_personnel_display(self):
        if self.workshop_personnel:
            return self.workshop_personnel.my_title
        else:
            return ''

    @property
    def quit_job_editable(self):
        if self.quit_job_date:
            lists = self.list_of_pay_item.filter(Q(list_of_pay__ultimate=True) &
                                                 Q(list_of_pay__month=self.quit_job_date.month))
            if len(lists) == 0:
                return True
            else:
                return False
        else:
            return True

    @property
    def is_insurance_editable(self):
        list_of_pays = self.list_of_pay_item.filter(Q(list_of_pay__ultimate=True) & Q(list_of_pay__use_in_calculate=True))
        is_in = []
        for list_of_pay in list_of_pays:
            check, day = list_of_pay.check_insurance
            if check:
                is_in.append(list_of_pay.id)
        if len(is_in) > 0:
            return False
        else:
            return True

    @property
    def is_tax_editable(self):
        lists = self.list_of_pay_item.filter(Q(list_of_pay__ultimate=True) & Q(list_of_pay__use_in_calculate=True))
        is_in = []
        for list in lists:
            check, day = list.check_tax
            if check:
                is_in.append(list.id)
        if len(is_in) > 0:
            return False
        else:
            return True

    @property
    def un_verifiable(self):
        lists = self.list_of_pay_item.all()
        if len(lists) > 0:
            return False
        else:
            return True

    @property
    def check_with_same(self):
        validate_status = False
        contracts = Contract.objects.filter(Q(is_verified=True) & Q(workshop_personnel=self.workshop_personnel))
        for contract in contracts:
            end = contract.contract_to_date
            if contract.quit_job_date:
                end = contract.quit_job_date
            if self.contract_from_date.__ge__(contract.contract_from_date) and \
                    self.contract_from_date.__le__(end):
                validate_status = True
            elif self.contract_to_date.__ge__(contract.contract_from_date) and \
                    self.contract_to_date.__le__(end):
                validate_status = True
            elif self.contract_from_date.__le__(contract.contract_from_date) and \
                    self.contract_to_date.__ge__(end):
                validate_status = True
        return validate_status

    @property
    def find_hr(self):
        return self.hr_letter.first()

    @property
    def is_insurance_display(self):
        if self.insurance:
            return 'بیمه شده'
        else:
            return 'بیمه نشده'

    def __str__(self):
        if self.code:
            return str(self.code) + ' برای ' + self.workshop_personnel_display
        else:
            return str(self.id) + ' برای ' + self.workshop_personnel_display

    @property
    def check_hr_letter(self):
        hr = self.hr_letter.all()
        hr = hr.filter(Q(is_verified=True) & Q(is_active=True))
        hr = hr.first()
        if not hr:
            return False
        return True


class Loan(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
    LOAN = 'l'
    DEPT = 'd'

    LOAN_TYPES = (
        (LOAN, 'وام'),
        (DEPT, 'مساعده'),
    )
    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name='loan', on_delete=models.CASCADE,
                                           blank=True, null=True)
    amount = DECIMAL(blank=True, null=True)
    episode = models.IntegerField(blank=True, null=True)
    pay_date = jmodels.jDateField(blank=True, null=True)
    loan_type = models.CharField(max_length=1, choices=LOAN_TYPES, blank=True)
    explanation = EXPLANATION()
    episode_payed = models.IntegerField(default=0)
    pay_done = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        verbose_name = 'Loan'
        permission_basename = 'loan'
        permissions = (
            ('get.contract', 'مشاهده وام'),
            ('create.contract', 'تعریف وام'),
            ('update.contract', 'ویرایش وام'),
            ('delete.contract', 'حذف وام'),

            ('getOwn.contract', 'مشاهده وام خود'),
            ('updateOwn.contract', 'ویرایش وام خود'),
            ('deleteOwn.contract', 'حذف وام خود'),
        )

    def __str__(self):
        if self.amount and self.workshop_personnel:
            return str(self.amount) + ' به ' + self.workshop_personnel.my_title
        else:
            return str(self.id)

    @property
    def is_editable(self):
        pays = ListOfPayItem.objects.filter(
            Q(workshop_personnel=self.workshop_personnel) &
            Q(list_of_pay__ultimate=True)
        )
        for pay in pays:
            if pay.list_of_pay.start_date in self.get_pay_month['months']:
                return False
        return True

    @property
    def get_pay_episode(self):
        if self.amount and self.episode:
            return self.amount / Decimal(self.episode)
        else:
            return 0

    @property
    def settlement(self):
        if self.amount:
            total = self.amount
            for item in self.item.all():
                total -= item.payed_amount
            return total
        else:
            return 0

    @property
    def get_pay_month(self):
        if self.pay_date and self.episode:
            months = []
            month_base = 1
            for i in range(0, self.episode):
                if self.pay_date.month + i > 12:
                    pay_date = jdatetime.date(self.pay_date.year + int((self.pay_date.month + i) / 12), month_base, 1)
                    month_base += 1
                    if month_base > 12:
                        month_base = 1
                else:
                    pay_date = jdatetime.date(self.pay_date.year, self.pay_date.month + i, self.pay_date.day)
                months.append(pay_date)
            return {'months': months}
        else:
            return {'months': []}

    @property
    def end_date(self):
        if self.get_pay_month['months']:
            end = self.get_pay_month['months'][-1]
            if end.month <= 6:
                return str(end.year) + '-' + str(end.month) + '-31'
            elif end.month == 12:
                return str(end.year) + '-' + str(end.month) + '-29'
            elif end.month > 6 and end.month != 12:
                return str(end.year) + '-' + str(end.month) + '-30'
        else:
            return ''

    @staticmethod
    def with_comma(input_amount):
        amount = str(round(input_amount))[::-1]
        loop = int(len(amount) / 3)
        if len(amount) < 4:
            return str(round(input_amount))
        else:
            counter = 0
            for i in range(1, loop + 1):
                index = (i * 3) + counter
                counter += 1
                amount = amount[:index] + ',' + amount[index:]
        if amount[-1] == ',':
            amount = amount[:-1]
        return amount[::-1]

    @property
    def round_amount_with_comma(self):
        if self.amount:
            return self.with_comma(self.amount)
        else:
            return 0

    @property
    def check_with_contract(self):
        contracts = Contract.objects.filter(Q(workshop_personnel=self.workshop_personnel) & Q(is_verified=True))
        is_in_contract = False
        for contract in contracts:
            if self.pay_date.__ge__(contract.contract_from_date) and self.pay_date.__le__(contract.contract_to_date):
                is_in_contract = True
        return is_in_contract

    def save(self, *args, **kwargs):
        if not self.workshop_personnel:
            raise ValidationError('برای ثبت اولیه انتخاب پرسنل اجباری است')
        if self.is_verified:
            if self.loan_type == 'd':
                self.episode = 1
            super().save(*args, **kwargs)

            for date in self.get_pay_month['months']:
                LoanItem.objects.create(
                    loan=self,
                    amount=self.get_pay_episode,
                    date=date,
                )
        elif not self.is_verified:
            for item in self.item.all():
                item.delete()
            super().save(*args, **kwargs)

        else:
            super().save(*args, **kwargs)


class LoanItem(BaseModel, LockableMixin, DefinableMixin):
    loan = models.ForeignKey(Loan, related_name='item', on_delete=models.CASCADE, blank=True, null=True)
    amount = DECIMAL(default=0)
    payed_amount = DECIMAL(default=0)
    date = jmodels.jDateField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'LoanItem'
        permission_basename = 'loan_item'
        permissions = (
            ('get.loan_item', 'مشاهده قسط وام'),
            ('create.loan_item', 'تعریف قسط وام'),
            ('update.loan_item', 'ویرایش قسط وام'),
            ('delete.loan_item', 'حذف قسط وام'),

            ('getOwn.loan_item', 'مشاهده قسط وام خود'),
            ('updateOwn.loan_item', 'ویرایش وام قسط خود'),
            ('deleteOwn.loan_item', 'حذف وام قسط خود'),
        )

    @staticmethod
    def with_comma(input_amount):
        amount = str(round(input_amount))[::-1]
        loop = int(len(amount) / 3)
        if len(amount) < 4:
            return str(round(input_amount))
        else:
            counter = 0
            for i in range(1, loop + 1):
                index = (i * 3) + counter
                counter += 1
                amount = amount[:index] + ',' + amount[index:]
        if amount[-1] == ',':
            amount = amount[:-1]
        return amount[::-1]

    @property
    def round_amount_with_comma(self):
        previous_unpaid = 0
        for item in self.loan.item.all():
            if item.date.__lt__(self.date):
                unpaid = item.amount - item.payed_amount
                previous_unpaid += unpaid
        if self.amount:
            return self.with_comma(self.amount + previous_unpaid)
        else:
            return 0

    @property
    def round_bed_or_bes_with_comma(self):
        if self.amount:
            return self.with_comma(self.bed_or_bes)
        else:
            return 0

    @property
    def round_balance_with_comma(self):
        if self.amount:
            return self.with_comma(self.cumulative_balance)
        else:
            return 0

    @property
    def round_payed_with_comma(self):
        if self.amount:
            return self.with_comma(self.payed_amount)
        else:
            return 0

    @property
    def un_paid(self):
        return self.amount - self.payed_amount

    @property
    def pay_done(self):
        return self.amount - self.payed_amount == 0

    @property
    def bed_or_bes(self):
        return self.amount - self.payed_amount

    @property
    def is_last(self):
        for item in self.loan.item.all():
            if item.date.__gt__(self.date):
                return False
        return True

    @property
    def cumulative_balance(self):
        items = LoanItem.objects.filter(
            Q(loan=self.loan) & Q(date__lte=self.date)
        )
        amount = self.loan.amount
        for item in items:
            amount -= item.payed_amount
        return amount

    @property
    def month_display(self):
        months = {
            1: 'فروردین',
            2: 'اردیبهشت',
            3: 'خرداد',
            4: 'تیر',
            5: 'مرداد',
            6: 'شهریور',
            7: 'مهر',
            8: 'آبان',
            9: 'آذر',
            10: 'دی',
            11: 'بهمن',
            12: 'اسفند',
        }
        return months[self.date.month]


class OptionalDeduction(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
    company = models.ForeignKey(Company, related_name='deduction', on_delete=models.CASCADE,
                                blank=True, null=True)
    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name='deduction',
                                           on_delete=models.CASCADE, blank=True, null=True)
    is_template = models.BooleanField(default=False, blank=True, null=True)
    template_name = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    amount = DECIMAL(blank=True, null=True)
    episode = models.IntegerField(default=1)
    start_date = jmodels.jDateField(blank=True, null=True)
    explanation = EXPLANATION()
    pay_done = models.BooleanField(default=False)
    episode_payed = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'Deductions'
        permission_basename = 'deductions'
        permissions = (
            ('get.contract', 'مشاهده کسورات اختیاری'),
            ('create.contract', 'تعریف کسورات اختیاری'),
            ('update.contract', 'ویرایش کسورات اختیاری'),
            ('delete.contract', 'حذف کسورات اختیاری'),

            ('getOwn.contract', 'مشاهده کسورات اختیاری خود'),
            ('updateOwn.contract', 'ویرایش وام کسورات اختیاری'),
            ('deleteOwn.contract', 'حذف وام کسورات اختیاری'),
        )

    @property
    def is_editable(self):
        if self.is_template:
            return True
        else:
            pays = ListOfPayItem.objects.filter(
                Q(workshop_personnel=self.workshop_personnel) &
                Q(list_of_pay__ultimate=True)
            )
            for pay in pays:
                if pay.list_of_pay.start_date in self.get_pay_month['months']:
                    return False
            return True

    @property
    def check_with_contract(self):
        contracts = Contract.objects.filter(Q(workshop_personnel=self.workshop_personnel) & Q(is_verified=True))
        is_in_contract = False
        for contract in contracts:
            if self.start_date.__ge__(contract.contract_from_date) and self.start_date.__le__(
                    contract.contract_to_date):
                is_in_contract = True
        return is_in_contract

    def __str__(self):
        if self.amount and self.workshop_personnel:
            return str(self.amount) + ' به ' + self.workshop_personnel.my_title
        else:
            return str(self.id)

    @property
    def get_pay_episode(self):
        if self.amount and self.episode:
            return self.amount / Decimal(self.episode)
        else:
            return 0

    @property
    def settlement(self):
        if self.amount and self.episode_payed and self.get_pay_episode:
            return round(self.amount) - (round(self.episode_payed) * self.get_pay_episode)
        else:
            return 0

    @property
    def get_pay_month(self):
        if self.start_date and self.episode:
            months = []
            month_base = 1
            for i in range(0, self.episode):
                if self.start_date.month + i > 12:
                    pay_date = jdatetime.date(self.start_date.year + int((self.start_date.month + i) / 12),
                                              month_base, self.start_date.day)
                    month_base += 1
                    if month_base > 12:
                        month_base = 1
                else:
                    pay_date = jdatetime.date(self.start_date.year, self.start_date.month + i, self.start_date.day)
                months.append(pay_date)
            return {'months': months}
        else:
            return {'months': []}

    @property
    def end_date(self):
        if self.get_pay_month['months']:
            end = self.get_pay_month['months'][-1]
            return str(end.year) + '-' + str(end.month) + '-1'
        else:
            return ''

    @staticmethod
    def with_comma(input_amount):
        amount = str(round(input_amount))[::-1]
        loop = int(len(amount) / 3)
        if len(amount) < 4:
            return str(round(input_amount))
        else:
            counter = 0
            for i in range(1, loop + 1):
                index = (i * 3) + counter
                counter += 1
                amount = amount[:index] + ',' + amount[index:]
        if amount[-1] == ',':
            amount = amount[:-1]
        return amount[::-1]

    @property
    def round_amount_with_comma(self):
        if self.amount:
            return self.with_comma(self.amount)
        else:
            return 0

    @property
    def round_pay_episode_with_comma(self):
        if self.amount:
            return self.with_comma(self.get_pay_episode)
        else:
            return 0

    @property
    def is_template_display(self):
        if self.is_template == None:
            return ' - '
        elif self.is_template:
            return 'قالب'
        else:
            return 'شخصی'

    def save(self, *args, **kwargs):
        if not self.episode:
            self.episode = 0
        if self.is_template == None:
            raise ValidationError('برای ثبت اولیه انتخاب نوع الزامی است')
        super().save(*args, **kwargs)


class LeaveOrAbsence(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
    ENTITLEMENT = 'e'
    ILLNESS = 'i'
    WITHOUT_SALARY = 'w'
    ABSENCE = 'a'
    MATTER_73 = 'm'
    CHILD_BORN = 'c'

    LEAVE_TYPES = (
        (ENTITLEMENT, 'استحقاقی'),
        (ILLNESS, 'استعلاجی'),
        (WITHOUT_SALARY, 'بدون حقوق'),
        (ABSENCE, 'غیبت'),
        (MATTER_73, 'ماده 73'),
        (CHILD_BORN, 'زایمان'),
    )

    HOURLY = 'h'
    DAILY = 'd'

    ENTITLEMENT_LEAVE_TYPES = (
        (HOURLY, 'ساعتی'),
        (DAILY, 'روزانه'),

    )

    MARRIAGE = 'm'
    SPOUSAL_DEATH = 's'
    CHILD_DEATH = 'd'
    PARENT_DEATH = 'p'

    MATTER_73_LEAVE_TYPES = (
        (MARRIAGE, 'ازدواج'),
        (SPOUSAL_DEATH, 'مرگ همسر'),
        (CHILD_DEATH, 'مرگ فرزند'),
        (PARENT_DEATH, 'مرگ پدر یا مادر'),

    )

    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name='leave', on_delete=models.CASCADE,
                                           blank=True, null=True)
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPES, blank=True, null=True)
    entitlement_leave_type = models.CharField(max_length=2, choices=ENTITLEMENT_LEAVE_TYPES, blank=True, null=True)
    matter73_leave_type = models.CharField(max_length=2, choices=MATTER_73_LEAVE_TYPES, blank=True, null=True)
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
        if self.leave_type == 'e' and self.entitlement_leave_type == 'h' and \
                self.to_hour and self.from_hour:
            duration = datetime.timedelta(hours=self.to_hour.hour - self.from_hour.hour,
                                          minutes=self.to_hour.minute - self.from_hour.minute)
            final_by_day = (duration.seconds / 60) / 440
        elif self.from_date and self.to_date:
            difference = self.to_date - self.from_date
            final_by_day = difference.days + 1
            if self.leave_type == 'm' and final_by_day > 3:
                final_by_day = 3
        else:
            final_by_day = 0
        return final_by_day

    @property
    def hour(self):
        hour = 0
        if self.leave_type == 'e' and self.entitlement_leave_type == 'h':
            duration = datetime.timedelta(hours=self.to_hour.hour - self.from_hour.hour,
                                          minutes=self.to_hour.minute - self.from_hour.minute)
            hour = (duration.seconds / 60) / 60
            minute = (duration.seconds / 60) % 60
            minute = str(round(minute))
            if minute == '0':
                minute = '00'
            elif len(str(minute)) == 1:
                minute = '0' + minute
            hour = str(round(hour))
            if len(hour) < 2:
                hour = '0' + hour
            return hour + ':' + minute
        elif self.final_by_day > 0:
            hour = self.final_by_day * 24
        else:
            hour = 0
        return str(round(hour))

    @property
    def check_with_contract(self):
        contracts = Contract.objects.filter(Q(workshop_personnel=self.workshop_personnel) & Q(is_verified=True))
        is_in_contract = False
        if self.entitlement_leave_type != 'h':
            for contract in contracts:
                if self.from_date.__ge__(contract.contract_from_date) and self.to_date.__le__(
                        contract.contract_to_date):
                    is_in_contract = True
        elif self.leave_type == 'e' and self.entitlement_leave_type == 'h':
            for contract in contracts:
                if self.date.__ge__(contract.contract_from_date) and self.date.__le__(contract.contract_to_date):
                    is_in_contract = True
        return is_in_contract

    @property
    def check_with_same(self):
        leaves = LeaveOrAbsence.objects.filter(Q(workshop_personnel=self.workshop_personnel) & Q(is_verified=True))
        is_in_same = False
        if self.entitlement_leave_type == 'h':
            for leave in leaves:
                if leave.entitlement_leave_type == 'h' and leave.date == self.date:
                    if self.from_hour.__ge__(leave.from_hour) and self.from_hour.__le__(leave.to_hour):
                        is_in_same = True
                    if self.to_hour.__ge__(leave.from_hour) and self.to_hour.__le__(leave.to_hour):
                        is_in_same = True
                    if self.from_hour.__le__(leave.from_hour) and self.to_hour.__ge__(leave.to_hour):
                        is_in_same = True
                    if self.from_hour.__ge__(leave.from_hour) and self.to_hour.__le__(leave.to_hour):
                        is_in_same = True
                elif leave.entitlement_leave_type != 'h':
                    if self.date.__ge__(leave.from_date) and self.date.__le__(leave.to_date):
                        is_in_same = True
        elif self.entitlement_leave_type != 'h' or self.leave_type != 'e':
            for leave in leaves:
                if leave.entitlement_leave_type == 'h':
                    if leave.date.__ge__(self.from_date) and leave.date.__le__(self.to_date):
                        is_in_same = True
                elif leave.entitlement_leave_type != 'h' or leave.leave_type != 'e':
                    if self.from_date.__ge__(leave.from_date) and self.from_date.__le__(leave.to_date):
                        is_in_same = True
                    if self.to_date.__ge__(leave.from_date) and self.to_date.__le__(leave.to_date):
                        is_in_same = True
                    if self.from_date.__le__(leave.from_date) and self.to_date.__ge__(leave.to_date):
                        is_in_same = True
                    if self.from_date.__ge__(leave.from_date) and self.to_date.__le__(leave.to_date):
                        is_in_same = True

        return is_in_same

    @property
    def check_with_same_mission(self):
        missions = Mission.objects.filter(Q(workshop_personnel=self.workshop_personnel) & Q(is_verified=True))
        is_in_same = False
        if self.entitlement_leave_type == 'h':
            for mission in missions:
                if mission.mission_type == 'h' and mission.date == self.date:
                    if self.from_hour.__ge__(mission.from_hour) and self.from_hour.__le__(mission.to_hour):
                        is_in_same = True
                    if self.to_hour.__ge__(mission.from_hour) and self.to_hour.__le__(mission.to_hour):
                        is_in_same = True
                    if self.from_hour.__le__(mission.from_hour) and self.to_hour.__ge__(mission.to_hour):
                        is_in_same = True
                    if self.from_hour.__ge__(mission.from_hour) and self.to_hour.__le__(mission.to_hour):
                        is_in_same = True
                elif mission.mission_type == 'd':
                    if self.date.__ge__(mission.from_date) and self.date.__le__(mission.to_date):
                        is_in_same = True
        elif self.entitlement_leave_type == 'd' or self.leave_type != 'e':
            for mission in missions:
                if mission.mission_type == 'h':
                    if mission.date.__ge__(self.from_date) and mission.date.__le__(self.to_date):
                        is_in_same = True
                elif mission.mission_type == 'd':
                    if self.from_date.__ge__(mission.from_date) and self.from_date.__le__(mission.to_date):
                        is_in_same = True
                    if self.to_date.__ge__(mission.from_date) and self.to_date.__le__(mission.to_date):
                        is_in_same = True
                    if self.from_date.__le__(mission.from_date) and self.to_date.__ge__(mission.to_date):
                        is_in_same = True
                    if self.from_date.__ge__(mission.from_date) and self.to_date.__le__(mission.to_date):
                        is_in_same = True

        return is_in_same

    def save(self, *args, **kwargs):
        if not self.workshop_personnel:
            raise ValidationError('انتخاب پرسنل در کارگاه برای ثبت اولیه الزامیست')
        self.time_period = self.final_by_day
        if self.leave_type == 'm' and self.from_date and self.to_date:
            duration = datetime.timedelta(days=2)
            if (self.to_date - self.from_date).days > 2:
                self.to_date = self.from_date + duration
        if self.entitlement_leave_type == 'h' and self.leave_type == 'e':
            self.from_date, self.to_date, self.cause_of_incident = None, None, ' '
        elif self.entitlement_leave_type == 'd' and self.leave_type == 'e':
            self.from_hour, self.to_hour, self.date, self.cause_of_incident = None, None, None, ' '
        else:
            self.from_hour, self.to_hour, self.date = None, None, None
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


class HRLetter(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
    DAILY_PAY = 'd'
    BASE_PAY = 'b'

    PAY_TYPES = (
        (DAILY_PAY, 'حداقل حقوق روزانه'),
        (BASE_PAY, 'مزد مبنا')
    )

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

    company = models.ForeignKey(Company, related_name='hr_letter', on_delete=models.CASCADE, blank=True, null=True)

    contract = models.ForeignKey(Contract, related_name='hr_letter', on_delete=models.CASCADE,
                                 blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_template = models.CharField(max_length=1, choices=HRLETTER_TYPES, blank=True, null=True)

    pay_done = models.BooleanField(default=False)
    daily_pay_base = DECIMAL(default=0)
    monthly_pay_base = DECIMAL(default=0)
    day_hourly_pay_base = DECIMAL(default=0)
    month_hourly_pay_base = DECIMAL(default=0)
    insurance_pay_day = DECIMAL(default=0)
    insurance_benefit = DECIMAL(default=0)
    insurance_not_included = DECIMAL(default=0)

    hoghooghe_roozane_use_tax = models.BooleanField(default=True)
    hoghooghe_roozane_use_insurance = models.BooleanField(default=True)
    hoghooghe_roozane_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    hoghooghe_roozane_amount = DECIMAL(default=0, blank=True, null=True)
    hoghooghe_roozane_base = models.BooleanField(default=False)

    paye_sanavat_use_tax = models.BooleanField(default=True)
    paye_sanavat_use_insurance = models.BooleanField(default=True)
    paye_sanavat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    paye_sanavat_amount = DECIMAL(default=None, blank=True, null=True)
    paye_sanavat_base = models.BooleanField(default=False)

    haghe_sarparasti_use_tax = models.BooleanField(default=True)
    haghe_sarparasti_use_insurance = models.BooleanField(default=True)
    haghe_sarparasti_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    haghe_sarparasti_amount = DECIMAL(default=0, blank=True, null=True)
    haghe_sarparasti_base = models.BooleanField(default=False)

    haghe_modiriyat_use_tax = models.BooleanField(default=True)
    haghe_modiriyat_use_insurance = models.BooleanField(default=True)
    haghe_modiriyat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    haghe_modiriyat_amount = DECIMAL(default=0, blank=True, null=True)
    haghe_modiriyat_base = models.BooleanField(default=False)

    haghe_jazb_use_tax = models.BooleanField(default=True)
    haghe_jazb_use_insurance = models.BooleanField(default=True)
    haghe_jazb_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    haghe_jazb_amount = DECIMAL(default=0, blank=True, null=True)
    haghe_jazb_base = models.BooleanField(default=False)

    fogholade_shoghl_use_tax = models.BooleanField(default=True)
    fogholade_shoghl_use_insurance = models.BooleanField(default=True)
    fogholade_shoghl_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    fogholade_shoghl_amount = DECIMAL(default=0, blank=True, null=True)
    fogholade_shoghl_base = models.BooleanField(default=False)

    haghe_tahsilat_use_tax = models.BooleanField(default=True)
    haghe_tahsilat_use_insurance = models.BooleanField(default=True)
    haghe_tahsilat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    haghe_tahsilat_amount = DECIMAL(default=0, blank=True, null=True)
    haghe_tahsilat_base = models.BooleanField(default=False)

    fogholade_sakhti_kar_use_tax = models.BooleanField(default=True)
    fogholade_sakhti_kar_use_insurance = models.BooleanField(default=True)
    fogholade_sakhti_kar_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    fogholade_sakhti_kar_amount = DECIMAL(default=0, blank=True, null=True)
    fogholade_sakhti_kar_base = models.BooleanField(default=False)

    haghe_ankal_use_tax = models.BooleanField(default=True)
    haghe_ankal_use_insurance = models.BooleanField(default=True)
    haghe_ankal_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    haghe_ankal_amount = DECIMAL(default=0, blank=True, null=True)
    haghe_ankal_base = models.BooleanField(default=False)

    fogholade_badi_abohava_use_tax = models.BooleanField(default=True)
    fogholade_badi_abohava_use_insurance = models.BooleanField(default=True)
    fogholade_badi_abohava_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    fogholade_badi_abohava_amount = DECIMAL(default=0, blank=True, null=True)
    fogholade_badi_abohava_base = models.BooleanField(default=False)

    mahroomiat_tashilat_zendegi_use_tax = models.BooleanField(default=True)
    mahroomiat_tashilat_zendegi_use_insurance = models.BooleanField(default=True)
    mahroomiat_tashilat_zendegi_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    mahroomiat_tashilat_zendegi_amount = DECIMAL(default=0, blank=True, null=True)
    mahroomiat_tashilat_zendegi_base = models.BooleanField(default=False)

    fogholade_mahal_khedmat_use_tax = models.BooleanField(default=True)
    fogholade_mahal_khedmat_use_insurance = models.BooleanField(default=True)
    fogholade_mahal_khedmat_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    fogholade_mahal_khedmat_amount = DECIMAL(default=0, blank=True, null=True)
    fogholade_mahal_khedmat_base = models.BooleanField(default=False)

    fogholade_sharayet_mohit_kar_use_tax = models.BooleanField(default=True)
    fogholade_sharayet_mohit_kar_use_insurance = models.BooleanField(default=True)
    fogholade_sharayet_mohit_kar_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    fogholade_sharayet_mohit_kar_amount = DECIMAL(default=0, blank=True, null=True)
    fogholade_sharayet_mohit_kar_base = models.BooleanField(default=False)

    haghe_maskan_use_tax = models.BooleanField(default=True)
    haghe_maskan_use_insurance = models.BooleanField(default=True)
    haghe_maskan_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    haghe_maskan_amount = DECIMAL(default=0, blank=True, null=True)
    haghe_maskan_base = models.BooleanField(default=False)

    ayabo_zahab_use_tax = models.BooleanField(default=True)
    ayabo_zahab_use_insurance = models.BooleanField(default=True)
    ayabo_zahab_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    ayabo_zahab_amount = DECIMAL(default=0, blank=True, null=True)
    ayabo_zahab_base = models.BooleanField(default=False)

    bon_kharo_bar_use_tax = models.BooleanField(default=True)
    bon_kharo_bar_use_insurance = models.BooleanField(default=True)
    bon_kharo_bar_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    bon_kharo_bar_amount = DECIMAL(default=0, blank=True, null=True)
    bon_kharo_bar_base = models.BooleanField(default=False)

    yarane_ghaza_use_tax = models.BooleanField(default=True)
    yarane_ghaza_use_insurance = models.BooleanField(default=True)
    yarane_ghaza_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    yarane_ghaza_amount = DECIMAL(default=0, blank=True, null=True)
    yarane_ghaza_base = models.BooleanField(default=False)

    haghe_shir_use_tax = models.BooleanField(default=True)
    haghe_shir_use_insurance = models.BooleanField(default=True)
    haghe_shir_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    haghe_shir_amount = DECIMAL(default=0, blank=True, null=True)
    haghe_shir_base = models.BooleanField(default=False)

    haghe_taahol_use_tax = models.BooleanField(default=True)
    haghe_taahol_use_insurance = models.BooleanField(default=True)
    haghe_taahol_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    haghe_taahol_amount = DECIMAL(default=0, blank=True, null=True)
    haghe_taahol_base = models.BooleanField(default=False)

    komakhazine_mahdekoodak_use_tax = models.BooleanField(default=True)
    komakhazine_mahdekoodak_use_insurance = models.BooleanField(default=True)
    komakhazine_mahdekoodak_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    komakhazine_mahdekoodak_amount = DECIMAL(default=0, blank=True, null=True)
    komakhazine_mahdekoodak_base = models.BooleanField(default=False)

    komakhazine_varzesh_use_tax = models.BooleanField(default=True)
    komakhazine_varzesh_use_insurance = models.BooleanField(default=True)
    komakhazine_varzesh_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    komakhazine_varzesh_amount = DECIMAL(default=0, blank=True, null=True)
    komakhazine_varzesh_base = models.BooleanField(default=False)

    komakhazine_mobile_use_tax = models.BooleanField(default=True)
    komakhazine_mobile_use_insurance = models.BooleanField(default=True)
    komakhazine_mobile_nature = models.CharField(max_length=1, choices=NATURE_TYPES, blank=True, null=True)
    komakhazine_mobile_amount = DECIMAL(default=0, blank=True, null=True)
    komakhazine_mobile_base = models.BooleanField(default=False)

    mazaya_mostamar_gheyre_naghdi_use_tax = models.BooleanField(default=True)
    mazaya_mostamar_gheyre_naghdi_use_insurance = models.BooleanField(default=True)
    mazaya_mostamar_gheyre_naghdi_nature = models.CharField(max_length=1, choices=NATURE_TYPES, default=PENSION)
    mazaya_mostamar_gheyre_naghdi_amount = DECIMAL(default=0, blank=True, null=True)
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

    unemployed_insurance_nerkh = models.DecimalField(max_digits=24, default=0.03, decimal_places=12)
    worker_insurance_nerkh = models.DecimalField(max_digits=24, default=0.07, decimal_places=12)
    employer_insurance_nerkh = models.DecimalField(max_digits=24, default=0.2, decimal_places=12)

    is_calculated = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    haghe_sanavat_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
    eydi_padash_pay_type = models.CharField(max_length=1, choices=PAY_TYPES, default=BASE_PAY)
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

    def save(self, *args, **kwargs):
        if self.is_template == 'p' and not self.name:
            self.name = 'شخصی'
        if self.is_template == 'p' and self.contract:
            if self.contract.workshop_personnel.total_insurance < 12:
                self.paye_sanavat_amount, self.paye_sanavat_base = None, False
        self.daily_pay_base, self.monthly_pay_base, self.day_hourly_pay_base, self.month_hourly_pay_base = \
            self.calculate_pay_bases
        self.insurance_pay_day = self.calculate_insurance_pay_base
        self.insurance_benefit = self.calculate_insurance_benefit
        self.insurance_not_included = self.calculate_insurance_not_included

        if not self.id and self.is_template == 'p' and not self.contract:
            raise ValidationError('برای ثبت اولیه حکم شخصی وارد کردن قرارداد الزامی است')
        if not self.id and self.is_template == 'p' and self.contract:
            self.set_default_pay_types()
        super().save(*args, **kwargs)

    def set_default_pay_types(self):
        self.haghe_sanavat_pay_type = self.contract.workshop_personnel.workshop.haghe_sanavat_pay_type
        self.eydi_padash_pay_type = self.contract.workshop_personnel.workshop.eydi_padash_pay_type
        self.ezafe_kari_pay_type = self.contract.workshop_personnel.workshop.ezafe_kari_pay_type
        self.tatil_kari_pay_type = self.contract.workshop_personnel.workshop.tatil_kari_pay_type
        self.kasre_kar_pay_type = self.contract.workshop_personnel.workshop.kasre_kar_pay_type
        self.shab_kari_pay_type = self.contract.workshop_personnel.workshop.shab_kari_pay_type
        self.aele_mandi_pay_type = self.contract.workshop_personnel.workshop.aele_mandi_pay_type
        self.nobat_kari_sob_asr_pay_type = self.contract.workshop_personnel.workshop.nobat_kari_sob_asr_pay_type
        self.nobat_kari_sob_shab_pay_type = self.contract.workshop_personnel.workshop.nobat_kari_sob_shab_pay_type
        self.nobat_kari_asr_shab_pay_type = self.contract.workshop_personnel.workshop.nobat_kari_asr_shab_pay_type
        self.nobat_kari_sob_asr_shab_pay_type = self.contract.workshop_personnel.workshop.nobat_kari_sob_asr_shab_pay_type
        self.mission_pay_type = self.contract.workshop_personnel.workshop.mission_pay_type

    @property
    def get_aele_mandi_amount(self):
        if self.contract.workshop_personnel.workshop.aele_mandi_pay_type == 'd':
            return self.contract.workshop_personnel.workshop.aele_mandi_nerkh * self.hoghooghe_roozane_amount
        else:
            return self.contract.workshop_personnel.workshop.aele_mandi_nerkh * self.daily_pay_base

    @property
    def calculated(self):
        if self.is_calculated:
            return 'غیرقابل تغییر'
        else:
            return ' - '

    @property
    def active_display(self):
        if self.is_active:
            return 'فعال'
        else:
            return ' - '

    @property
    def contract_info(self):
        response = {}
        response['personnel_name'] = self.contract.workshop_personnel.personnel.full_name
        response['workshop_name'] = self.contract.workshop_personnel.workshop.workshop_title
        return response

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
            'amount': self.hoghooghe_roozane_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.paye_sanavat_use_insurance,
            'nature': self.paye_sanavat_nature,
            'base': self.paye_sanavat_base,
            'amount': self.paye_sanavat_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.haghe_sarparasti_use_insurance,
            'nature': self.haghe_sarparasti_nature,
            'base': self.haghe_sarparasti_base,
            'amount': self.haghe_sarparasti_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.haghe_modiriyat_use_insurance,
            'nature': self.haghe_modiriyat_nature,
            'base': self.haghe_modiriyat_base,
            'amount': self.haghe_modiriyat_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.haghe_jazb_use_insurance,
            'nature': self.haghe_jazb_nature,
            'base': self.haghe_jazb_base,
            'amount': self.haghe_jazb_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.fogholade_shoghl_use_insurance,
            'nature': self.fogholade_shoghl_nature,
            'base': self.fogholade_shoghl_base,
            'amount': self.fogholade_shoghl_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.haghe_tahsilat_use_insurance,
            'nature': self.haghe_tahsilat_nature,
            'base': self.haghe_tahsilat_base,
            'amount': self.haghe_tahsilat_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.fogholade_sakhti_kar_use_insurance,
            'nature': self.fogholade_sakhti_kar_nature,
            'base': self.fogholade_sakhti_kar_base,
            'amount': self.fogholade_sakhti_kar_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.haghe_ankal_use_insurance,
            'nature': self.haghe_ankal_nature,
            'base': self.haghe_ankal_base,
            'amount': self.haghe_ankal_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.fogholade_badi_abohava_use_insurance,
            'nature': self.fogholade_badi_abohava_nature,
            'base': self.fogholade_badi_abohava_base,
            'amount': self.fogholade_badi_abohava_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.mahroomiat_tashilat_zendegi_use_insurance,
            'nature': self.mahroomiat_tashilat_zendegi_nature,
            'base': self.mahroomiat_tashilat_zendegi_base,
            'amount': self.mahroomiat_tashilat_zendegi_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.fogholade_mahal_khedmat_use_insurance,
            'nature': self.fogholade_mahal_khedmat_nature,
            'base': self.fogholade_mahal_khedmat_base,
            'amount': self.fogholade_mahal_khedmat_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.fogholade_sharayet_mohit_kar_use_insurance,
            'nature': self.fogholade_sharayet_mohit_kar_nature,
            'base': self.fogholade_sharayet_mohit_kar_base,
            'amount': self.fogholade_sharayet_mohit_kar_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.haghe_maskan_use_insurance,
            'nature': self.haghe_maskan_nature,
            'base': self.haghe_maskan_base,
            'amount': self.haghe_maskan_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.ayabo_zahab_use_insurance,
            'nature': self.ayabo_zahab_nature,
            'base': self.ayabo_zahab_base,
            'amount': self.ayabo_zahab_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.bon_kharo_bar_use_insurance,
            'nature': self.bon_kharo_bar_nature,
            'base': self.bon_kharo_bar_base,
            'amount': self.bon_kharo_bar_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.yarane_ghaza_use_insurance,
            'nature': self.yarane_ghaza_nature,
            'base': self.yarane_ghaza_base,
            'amount': self.yarane_ghaza_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.haghe_shir_use_insurance,
            'nature': self.haghe_shir_nature,
            'base': self.haghe_shir_base,
            'amount': self.haghe_shir_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.haghe_taahol_use_insurance,
            'nature': self.haghe_taahol_nature,
            'base': self.haghe_taahol_base,
            'amount': self.haghe_taahol_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.komakhazine_mahdekoodak_use_insurance,
            'nature': self.komakhazine_mahdekoodak_nature,
            'base': self.komakhazine_mahdekoodak_base,
            'amount': self.komakhazine_mahdekoodak_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.komakhazine_varzesh_use_insurance,
            'nature': self.komakhazine_varzesh_nature,
            'base': self.komakhazine_varzesh_base,
            'amount': self.komakhazine_varzesh_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.komakhazine_mobile_use_insurance,
            'nature': self.komakhazine_mobile_nature,
            'base': self.komakhazine_mobile_base,
            'amount': self.komakhazine_mobile_amount or 0
        })
        hr_letter_items.append({
            'insurance': self.mazaya_mostamar_gheyre_naghdi_use_insurance,
            'nature': self.mazaya_mostamar_gheyre_naghdi_nature,
            'base': self.mazaya_mostamar_gheyre_naghdi_base,
            'amount': self.mazaya_mostamar_gheyre_naghdi_amount or 0
        })

        return hr_letter_items

    @property
    def aele_mandi_sum(self):
        if self.contract and self.contract.workshop_personnel.insurance_history_total:
            if self.contract.workshop_personnel.insurance_history_total >= 24:
                personnel_family = self.contract.workshop_personnel.personnel.childs
                aele_mandi_child = 0
                for person in personnel_family:
                    if person.marital_status == 's':
                        person_age = self.contract.contract_to_date.year - person.date_of_birth.year
                        if person_age <= 18:
                            aele_mandi_child += 1
                        elif person.physical_condition != 'h':
                            aele_mandi_child += 1
                return aele_mandi_child
            else:
                return 0
        else:
            return 0

    @property
    def calculate_pay_bases(self):
        daily, monthly = 0, 0
        hr_letter_items = self.get_hr_items
        for i in range(0, 23):
            if hr_letter_items[i]['base'] and hr_letter_items[i]['amount']:
                if i < 2:
                    daily += hr_letter_items[i]['amount']
                    monthly += hr_letter_items[i]['amount'] * Decimal(30)
                else:
                    daily += hr_letter_items[i]['amount'] / Decimal(30)
                    monthly += hr_letter_items[i]['amount']
        month_hourly = monthly / Decimal(220)
        day_hourly = daily / Decimal(7.33)
        return daily, monthly, day_hourly, month_hourly

    @property
    def hoghoogh_mahanae(self):
        return self.hoghooghe_roozane_amount * Decimal(30)

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
        for i in range(0, 23):
            if hr_letter_items[i]['insurance'] and hr_letter_items[i]['nature'] == 'b':
                if i < 2:
                    insurance_pay_base += round(hr_letter_items[i]['amount'])
                else:
                    insurance_pay_base += round(hr_letter_items[i]['amount'] / 30)
        return insurance_pay_base

    @property
    def calculate_insurance_benefit(self):
        insurance_benefit = 0
        hr_letter_items = self.get_hr_items
        for i in range(0, 23):
            if hr_letter_items[i]['insurance'] and hr_letter_items[i]['nature'] != 'b':
                if i < 2:
                    insurance_benefit += hr_letter_items[i]['amount'] * 30
                else:
                    insurance_benefit += hr_letter_items[i]['amount']

        return insurance_benefit

    @property
    def calculate_insurance_not_included(self):
        insurance_not_included = 0
        hr_letter_items = self.get_hr_items
        for i in range(0, 23):
            if not hr_letter_items[i]['insurance']:
                if i < 2:
                    insurance_not_included += round(hr_letter_items[i]['amount'] * 30)
                else:
                    insurance_not_included += round(hr_letter_items[i]['amount'])
        return insurance_not_included

    @staticmethod
    def with_comma(input_amount):
        amount = str(round(input_amount))[::-1]
        loop = int(len(amount) / 3)
        if len(amount) < 4:
            return str(round(input_amount))
        else:
            counter = 0
            for i in range(1, loop + 1):
                index = (i * 3) + counter
                counter += 1
                amount = amount[:index] + ',' + amount[index:]
        if amount[-1] == ',':
            amount = amount[:-1]
        return amount[::-1]

    @property
    def hoghooghe_roozane_amount_with_comma(self):
        return self.with_comma(self.hoghooghe_roozane_amount)

    @property
    def paye_sanavat_amount_with_comma(self):
        return self.with_comma(self.paye_sanavat_amount)

    @property
    def haghe_maskan_amount_with_comma(self):
        return self.with_comma(self.haghe_maskan_amount)

    @property
    def bon_kharo_bar_amount_with_comma(self):
        return self.with_comma(self.bon_kharo_bar_amount)

    @property
    def haghe_sarparasti_amount_with_comma(self):
        return self.with_comma(self.haghe_sarparasti_amount)

    @property
    def haghe_modiriyat_amount_with_comma(self):
        return self.with_comma(self.haghe_modiriyat_amount)

    @property
    def haghe_jazb_amount_with_comma(self):
        return self.with_comma(self.haghe_jazb_amount)

    @property
    def fogholade_shoghl_amount_with_comma(self):
        return self.with_comma(self.fogholade_shoghl_amount)

    @property
    def haghe_tahsilat_amount_with_comma(self):
        return self.with_comma(self.haghe_tahsilat_amount)

    @property
    def fogholade_sakhti_kar_amount_with_comma(self):
        return self.with_comma(self.fogholade_sakhti_kar_amount)

    @property
    def haghe_ankal_amount_with_comma(self):
        return self.with_comma(self.haghe_ankal_amount)

    @property
    def fogholade_badi_abohava_amount_with_comma(self):
        return self.with_comma(self.fogholade_badi_abohava_amount)

    @property
    def mahroomiat_tashilat_zendegi_amount_with_comma(self):
        return self.with_comma(self.mahroomiat_tashilat_zendegi_amount)

    @property
    def fogholade_mahal_khedmat_amount_with_comma(self):
        return self.with_comma(self.fogholade_mahal_khedmat_amount)

    @property
    def fogholade_sharayet_mohit_kar_amount_with_comma(self):
        return self.with_comma(self.fogholade_sharayet_mohit_kar_amount)

    @property
    def ayabo_zahab_amount_with_comma(self):
        return self.with_comma(self.ayabo_zahab_amount)

    @property
    def yarane_ghaza_amount_with_comma(self):
        return self.with_comma(self.yarane_ghaza_amount)

    @property
    def haghe_shir_amount_with_comma(self):
        return self.with_comma(self.haghe_shir_amount)

    @property
    def haghe_taahol_amount_with_comma(self):
        return self.with_comma(self.haghe_taahol_amount)

    @property
    def komakhazine_mahdekoodak_amount_with_comma(self):
        return self.with_comma(self.komakhazine_mahdekoodak_amount)

    @property
    def komakhazine_varzesh_amount_with_comma(self):
        return self.with_comma(self.komakhazine_varzesh_amount)

    @property
    def komakhazine_mobile_amount_with_comma(self):
        return self.with_comma(self.komakhazine_mobile_amount)

    @property
    def mazaya_mostamar_gheyre_naghdi_amount_with_comma(self):
        return self.with_comma(self.mazaya_mostamar_gheyre_naghdi_amount)


class Mission(BaseModel, LockableMixin, DefinableMixin, VerifyMixin):
    HOURLY = 'h'
    DAILY = 'd'

    MISSION_TYPES = (
        (HOURLY, 'ساعتی'),
        (DAILY, 'روزانه'),

    )

    workshop_personnel = models.ForeignKey(WorkshopPersonnel, related_name='mission', on_delete=models.CASCADE)
    mission_type = models.CharField(max_length=2, choices=MISSION_TYPES, blank=True, null=True)
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
        if self.mission_type == 'h' and self.to_hour and self.from_hour:
            duration = datetime.timedelta(hours=self.to_hour.hour - self.from_hour.hour,
                                          minutes=self.to_hour.minute - self.from_hour.minute)
            final_by_day = (duration.seconds / 60) / 440
        elif self.to_date and self.from_date:
            difference = self.to_date - self.from_date
            final_by_day = difference.days + 1
        else:
            final_by_day = 0
        return final_by_day

    @property
    def hour(self):
        hour = 0
        if self.mission_type == 'h':
            duration = datetime.timedelta(hours=self.to_hour.hour - self.from_hour.hour,
                                          minutes=self.to_hour.minute - self.from_hour.minute)
            hour = (duration.seconds / 60) / 60
            minute = (duration.seconds / 60) % 60
            minute = round(minute)
            if minute == 0:
                minute = '00'
            elif len(str(minute)) == 1:
                minute = '0' + str(minute)
            return '0' + str(round(hour)) + ':' + str(minute)
        elif self.final_by_day > 0:
            hour = self.final_by_day * 24
        else:
            hour = 0
        return str(round(hour))

    @property
    def check_with_contract(self):
        contracts = Contract.objects.filter(Q(workshop_personnel=self.workshop_personnel) & Q(is_verified=True))
        is_in_contract = False
        if self.mission_type == 'd':
            for contract in contracts:
                if self.from_date.__ge__(contract.contract_from_date) and self.to_date.__le__(
                        contract.contract_to_date):
                    is_in_contract = True
        elif self.mission_type == 'h':
            for contract in contracts:
                if self.date.__ge__(contract.contract_from_date) and self.date.__le__(contract.contract_to_date):
                    is_in_contract = True
        return is_in_contract

    @property
    def check_with_same(self):
        missions = Mission.objects.filter(Q(workshop_personnel=self.workshop_personnel) & Q(is_verified=True))
        is_in_same = False
        if self.mission_type == 'h':
            for mission in missions:
                if mission.mission_type == 'h' and mission.date == self.date:
                    if self.from_hour.__ge__(mission.from_hour) and self.from_hour.__le__(mission.to_hour):
                        is_in_same = True
                    if self.to_hour.__ge__(mission.from_hour) and self.to_hour.__le__(mission.to_hour):
                        is_in_same = True
                    if self.from_hour.__le__(mission.from_hour) and self.to_hour.__ge__(mission.to_hour):
                        is_in_same = True
                    if self.from_hour.__ge__(mission.from_hour) and self.to_hour.__le__(mission.to_hour):
                        is_in_same = True
                elif mission.mission_type == 'd':
                    if self.date.__ge__(mission.from_date) and self.date.__le__(mission.to_date):
                        is_in_same = True
        elif self.mission_type == 'd':
            for mission in missions:
                if mission.mission_type == 'h':
                    if mission.date.__ge__(self.from_date) and mission.date.__le__(self.to_date):
                        is_in_same = True
                elif mission.mission_type == 'd':
                    if self.from_date.__ge__(mission.from_date) and self.from_date.__le__(mission.to_date):
                        is_in_same = True
                    if self.to_date.__ge__(mission.from_date) and self.to_date.__le__(mission.to_date):
                        is_in_same = True
                    if self.from_date.__le__(mission.from_date) and self.to_date.__ge__(mission.to_date):
                        is_in_same = True
                    if self.from_date.__ge__(mission.from_date) and self.to_date.__le__(mission.to_date):
                        is_in_same = True

        return is_in_same

    @property
    def check_with_same_leave(self):

        leaves = LeaveOrAbsence.objects.filter(Q(workshop_personnel=self.workshop_personnel) & Q(is_verified=True))
        is_in_same = False

        if self.mission_type == 'h':
            for leave in leaves:
                if leave.entitlement_leave_type == 'h' and leave.date == self.date:
                    if self.from_hour.__ge__(leave.from_hour) and self.from_hour.__le__(leave.to_hour):
                        is_in_same = True
                    if self.to_hour.__ge__(leave.from_hour) and self.to_hour.__le__(leave.to_hour):
                        is_in_same = True
                    if self.from_hour.__le__(leave.from_hour) and self.to_hour.__ge__(leave.to_hour):
                        is_in_same = True
                    if self.from_hour.__ge__(leave.from_hour) and self.to_hour.__le__(leave.to_hour):
                        is_in_same = True
                elif leave.entitlement_leave_type == 'd' or leave.leave_type != 'e':
                    if self.date.__ge__(leave.from_date) and self.date.__le__(leave.to_date):
                        is_in_same = True
        elif self.mission_type == 'd':
            for leave in leaves:
                if leave.entitlement_leave_type == 'h':
                    if leave.date.__ge__(self.from_date) and leave.date.__le__(self.to_date):
                        is_in_same = True
                elif leave.entitlement_leave_type == 'd' or leave.leave_type != 'e':
                    if self.from_date.__ge__(leave.from_date) and self.from_date.__le__(leave.to_date):
                        is_in_same = True
                    if self.to_date.__ge__(leave.from_date) and self.to_date.__le__(leave.to_date):
                        is_in_same = True
                    if self.from_date.__le__(leave.from_date) and self.to_date.__ge__(leave.to_date):
                        is_in_same = True
                    if self.to_date.__ge__(leave.from_date) and self.to_date.__le__(leave.to_date):
                        is_in_same = True

        return is_in_same

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
        self.time_period = self.final_by_day
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.time_period) + ' برای ' + self.workshop_personnel.personnel.full_name


class ListOfPay(BaseModel, LockableMixin, DefinableMixin):
    workshop = models.ForeignKey(Workshop, related_name="list_of_pay", on_delete=models.CASCADE,
                                 null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    month_days = models.IntegerField(default=30)
    start_date = jmodels.jDateField()
    end_date = jmodels.jDateField()
    ultimate = models.BooleanField(default=False)
    use_in_calculate = models.BooleanField(default=False)
    use_in_bime = models.BooleanField(default=False)

    '''for payment'''
    pay_done = models.BooleanField(default=False)
    pay_form_create_date = jmodels.jDateField(blank=True, null=True)
    bank_pay_date = jmodels.jDateField(blank=True, null=True)
    bank_pay_code = models.CharField(max_length=50, blank=True, null=True)
    bank_pay_explanation = EXPLANATION()
    bank_pay_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'ListOfPay'
        permission_basename = 'list_of_pay'
        ordering = ('-id',)
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
    def contract_rows(self):
        contract_row_ids = []
        for item in self.list_of_pay_item.all():
            if item.contract_row:
                contract_row_ids.append(item.contract_row.id)
        return contract_row_ids

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @staticmethod
    def with_comma(input_amount):
        if input_amount != 0:
            amount = str(round(input_amount))[::-1]
            loop = int(len(amount) / 3)
            if len(amount) < 4:
                return str(round(input_amount))
            else:
                counter = 0
                for i in range(1, loop + 1):
                    index = (i * 3) + counter
                    counter += 1
                    amount = amount[:index] + ',' + amount[index:]
            if amount[-1] == ',':
                amount = amount[:-1]
            res = amount[::-1]
            res = res.replace('-', '')
            return res
        else:
            return 0

    @property
    def pay_verify(self):
        if self.bank_pay_date and self.ultimate:
            return True
        else:
            return False

    @property
    def total_paid(self):
        total = 0
        list_items = self.list_of_pay_item.all()
        for item in list_items:
            total += item.paid_amount
        return total

    @property
    def total_paid_with_comma(self):
        return self.with_comma(self.total_paid)

    @property
    def total_un_paid_of_year_with_comma(self):
        return self.with_comma(self.total_un_paid_of_year)

    @property
    def total_payable_with_comma(self):
        return self.with_comma(self.total_payable)

    @property
    def total_un_paid_with_comma(self):
        return self.with_comma(self.total_un_paid)

    @property
    def un_paid_with_comma(self):
        return self.with_comma(self.un_paid)

    @property
    def total_payable(self):
        total = 0
        list_items = self.list_of_pay_item.all()
        for item in list_items:
            total += item.payable
        return total

    @property
    def total_un_paid_of_year(self):
        total = 0
        list_items = self.list_of_pay_item.all()
        for item in list_items:
            total += item.get_unpaid_of_year
        return total

    @property
    def total_un_paid(self):
        total = 0
        list_items = self.list_of_pay_item.all()
        for item in list_items:
            total += item.total_unpaid
        return total

    @property
    def un_paid(self):
        total = 0
        list_items = self.list_of_pay_item.all()
        for item in list_items:
            total += item.unpaid
        return total

    @property
    def is_editable(self):
        future_lists = ListOfPay.objects.filter(
            Q(workshop=self.workshop) &
            Q(use_in_calculate=self.use_in_calculate) &
            Q(year=self.year) &
            Q(month__gt=self.month) &
            Q(ultimate=True)
        )
        if len(future_lists) > 0 or self.bank_pay_date:
            return False
        else:
            return True

    @property
    def is_pay_editable(self):
        future_lists = ListOfPay.objects.filter(
            Q(workshop=self.workshop) &
            Q(use_in_calculate=self.use_in_calculate) &
            Q(year=self.year) &
            Q(month__gt=self.month) &
            Q(ultimate=True) &
            Q(pay_done=True)
        )
        if len(future_lists) > 0:
            return False
        return True

    @property
    def not_done_pay(self):
        previous_lists = ListOfPay.objects.filter(
            Q(workshop=self.workshop) &
            Q(use_in_calculate=self.use_in_calculate) &
            Q(ultimate=True) &
            Q(pay_done=True)
        )
        for item in previous_lists:
            if not item.bank_pay_date and item.id != self.id:
                return False
        return True

    @property
    def month_display(self):
        months = {
            1: 'فروردین',
            2: 'اردیبهشت',
            3: 'خرداد',
            4: 'تیر',
            5: 'مرداد',
            6: 'شهریور',
            7: 'مهر',
            8: 'آبان',
            9: 'آذر',
            10: 'دی',
            11: 'بهمن',
            12: 'اسفند',
        }
        return months[self.month]

    @property
    def is_ultimate(self):
        if self.ultimate:
            return 'قطعی'
        else:
            return 'غیر قطعی'

    def row_list(self, pk):
        return self.list_of_pay_item.filter(contract_row__id=pk)

    @property
    def is_use_in_calculate(self):
        if self.use_in_calculate:
            return 'محاسبه شده'
        else:
            return 'محاسبه نمی شود'

    @property
    def get_contracts(self):
        contracts = []
        workshop_personnel = self.workshop.get_personnel
        workshop_contracts_id = []
        for person in workshop_personnel:
            for contract in Contract.objects.filter(Q(is_verified=True) & Q(workshop_personnel_id=person.id)):
                workshop_contracts_id.append(contract.id)
        workshop_contracts = Contract.objects.filter(id__in=workshop_contracts_id)
        for contract in workshop_contracts:

            if not contract.quit_job_date:
                end = contract.contract_to_date
            else:
                end = contract.quit_job_date

            if contract.contract_from_date.__le__(self.start_date) and end.__ge__(self.end_date):
                contracts.append(contract.id)
            if contract.contract_from_date.__ge__(self.start_date) and end.__le__(self.end_date):
                contracts.append(contract.id)
            if contract.contract_from_date.__le__(self.start_date) and end.__ge__(self.start_date) and \
                    end.__le__(self.end_date):
                contracts.append(contract.id)
            if contract.contract_from_date.__ge__(self.start_date) and end.__ge__(self.end_date) and \
                    contract.contract_from_date.__lt__(self.end_date):
                contracts.append(contract.id)
        filtered_contracts = Contract.objects.filter(pk__in=contracts)
        if len(filtered_contracts) == 0:
            return 0
        else:
            return filtered_contracts

    @property
    def data_for_insurance(self):
        personnel_count = 0
        items = self.list_of_pay_item
        total_worktime = 0
        total_day_pay = 0
        total_month_pay = 0
        total_benefit = 0
        total_base = 0
        total_insurance = 0
        for item in items.all():
            if item.is_month_insurance:
                total_worktime += item.insurance_worktime
                total_day_pay += item.insurance_daily_payment
                total_month_pay += item.insurance_monthly_payment
                total_benefit += item.insurance_monthly_benefit
                total_base += item.total_payment
                total_insurance += item.haghe_bime_bime_shavande
                personnel_count += 1
        DSKKAR = {
            'DSK_ID': str(self.workshop.workshop_code),
            'DSK_NAME': self.workshop.name,
            'DSK_FARM': self.workshop.employer_name,
            'DSK_ADRS': self.workshop.address[:100],
            'DSK_KIND': 0,
            'DSK_YY': int(str(self.year)[2:]),
            'DSK_MM': self.month,
            'DSK_LISTNO': '0000',
            'DSK_DISC': '',
            'DSK_NUM': personnel_count,
            'DSK_TDD': total_worktime,
            'DSK_TROOZ': round(total_day_pay),
            'DSK_TMAH': round(total_month_pay),
            'DSK_TMAZ': round(total_benefit),
            'DSK_TMASH': round(total_benefit + total_month_pay),
            'DSK_TTOTL': round(total_base),
            'DSK_TBIME': round(total_insurance),
            'DSK_TKOSO': round((total_benefit + total_month_pay) * self.workshop.employee_insurance_nerkh),
            'DSK_TBIC': round((total_benefit + total_month_pay) * self.workshop.unemployed_insurance_nerkh),
            'DSK_RATE': self.workshop.employer_insurance_contribution,
            'DSK_PRATE': 0,
            'DSK_BIMH': 0,
            'DSK_PYM': '000',
        }
        return DSKKAR

    def data_for_insurance_row(self, pk):
        contract_row = ContractRow.objects.get(pk=pk)
        personnel_count = 0
        items = self.list_of_pay_item
        total_worktime = 0
        total_day_pay = 0
        total_month_pay = 0
        total_benefit = 0
        total_base = 0
        total_insurance = 0
        for item in items.filter(contract_row=contract_row):
            if item.is_month_insurance:
                total_worktime += item.insurance_worktime
                total_day_pay += item.insurance_daily_payment
                total_month_pay += item.insurance_monthly_payment
                total_benefit += item.insurance_monthly_benefit
                total_base += item.total_payment
                total_insurance += item.haghe_bime_bime_shavande
                personnel_count += 1
        DSKKAR = {
            'list_of_pays': self.list_of_pay_item.filter(contract_row=contract_row),
            'workshop': self.workshop,
            'DSK_ID': str(self.workshop.workshop_code),
            'DSK_NAME': self.workshop.name,
            'DSK_FARM': self.workshop.employer_name,
            'DSK_ADRS': self.workshop.address[:100],
            'DSK_KIND': 0,
            'DSK_YY': int(str(self.year)[2:]),
            'DSK_MM': self.month,
            'DSK_LISTNO': '0000',
            'DSK_DISC': '',
            'DSK_NUM': personnel_count,
            'DSK_TDD': total_worktime,
            'DSK_TROOZ': round(total_day_pay),
            'DSK_TMAH': round(total_month_pay),
            'DSK_TMAZ': round(total_benefit),
            'DSK_TMASH': round(total_benefit + total_month_pay),
            'DSK_TTOTL': round(total_base),
            'DSK_TBIME': round(total_insurance),
            'DSK_TKOSO': round((total_benefit + total_month_pay) * self.workshop.employee_insurance_nerkh),
            'DSK_TBIC': round((total_benefit + total_month_pay) * self.workshop.unemployed_insurance_nerkh),
            'DSK_RATE': self.workshop.employer_insurance_contribution,
            'DSK_PRATE': 0,
            'DSK_BIMH': 0,
            'DSK_PYM': contract_row.contract_row,
        }
        return DSKKAR

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
        contract_personnel = {}

        filtered_contracts = self.get_contracts
        for contract in filtered_contracts:
            if contract.workshop_personnel.personnel.is_personnel_active:
                contract_personnel[contract.id] = contract.workshop_personnel.personnel.id
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
                    if contract.quit_job_date:
                        personnel_normal_worktime[contract.id] = personnel_normal_worktime[contract.id] - 1
                    contract_start[contract.id] = contract.contract_from_date
                    contract_end[contract.id] = end
                if contract.contract_from_date.__le__(self.start_date) and end.__ge__(self.start_date) and \
                        end.__le__(self.end_date):
                    personnel_normal_worktime[contract.id] = end.day
                    if contract.quit_job_date:
                        personnel_normal_worktime[contract.id] = personnel_normal_worktime[contract.id] - 1
                    contract_start[contract.id] = self.start_date
                    contract_end[contract.id] = end
                if contract.contract_from_date.__ge__(self.start_date) and end.__ge__(self.end_date) and \
                        contract.contract_from_date.__lt__(self.end_date):
                    personnel_normal_worktime[contract.id] = self.month_days - contract.contract_from_date.day + 1
                    contract_start[contract.id] = contract.contract_from_date
                    contract_end[contract.id] = self.end_date
        response_data = []
        for contract in contract_personnel:
            absence_types = {'i': 0, 'w': 0, 'a': 0, 'e': 0, 'm': 0, 'eh': 0, 'ed': 0, 'c': 0}
            mission_day = 0
            contract = Contract.objects.get(pk=contract)
            workshop_personnel = contract.workshop_personnel
            is_insurance = contract.insurance
            filtered_absence = LeaveOrAbsence.objects.filter(Q(workshop_personnel=workshop_personnel) &
                                                             Q(is_verified=True))
            filtered_mission = Mission.objects.filter(Q(workshop_personnel=workshop_personnel) &
                                                      Q(is_in_payment=True) & Q(is_verified=True))
            for absence in filtered_absence.all():
                if absence.workshop_personnel == workshop_personnel:
                    if absence.leave_type == 'e' and absence.entitlement_leave_type == 'h' and \
                            absence.date.__ge__(contract_start[contract.id]) and \
                            absence.date.__le__(contract_end[contract.id]):
                        absence_types['eh'] += absence.to_hour.hour - absence.from_hour.hour
                    if absence.leave_type == 'e' and absence.entitlement_leave_type != 'h':
                        if absence.from_date.__ge__(contract_start[contract.id]) and absence.to_date.__le__(
                                contract_end[contract.id]):
                            absence_types['ed'] += absence.time_period
                        elif absence.from_date.__lt__(contract_start[contract.id]) and absence.to_date.__le__(
                                contract_end[contract.id]) and \
                                absence.to_date.__gt__(contract_start[contract.id]):
                            absence_types['ed'] += absence.to_date.day
                        elif absence.from_date.__gt__(contract_start[contract.id]) and absence.to_date.__gt__(
                                contract_end[contract.id]) and \
                                absence.from_date.__le__(contract_end[contract.id]):
                            absence_types['ed'] += contract_end[contract.id].day - absence.from_date.day
                        elif absence.from_date.__le__(contract_start[contract.id]) and absence.to_date.__ge__(
                                contract_end[contract.id]):
                            absence_types['ed'] += contract_end[contract.id].day - contract_start[contract.id].day
                    if absence.from_date.__ge__(contract_start[contract.id]) and absence.to_date.__le__(
                            contract_end[contract.id]):
                        absence_types[absence.leave_type] += absence.time_period
                    elif absence.from_date.__lt__(contract_start[contract.id]) and absence.to_date.__le__(
                            contract_end[contract.id]) and \
                            absence.to_date.__gt__(contract_start[contract.id]):
                        absence_types[absence.leave_type] += absence.to_date.day
                    elif absence.from_date.__gt__(contract_start[contract.id]) and absence.to_date.__gt__(
                            contract_end[contract.id]) and \
                            absence.from_date.__le__(contract_end[contract.id]):
                        absence_types[absence.leave_type] += contract_end[contract.id].day - absence.from_date.day + 1
                    elif absence.from_date.__le__(contract_start[contract.id]) and absence.to_date.__ge__(
                            contract_end[contract.id]):
                        absence_types[absence.leave_type] += contract_end[contract.id].day - contract_start[
                            contract.id].day
                    absence_types['e'] = absence_types['ed'] + Decimal(round(absence_types['eh'] / 7.33, 2))

            for mission in filtered_mission.all():
                if mission.workshop_personnel.personnel == workshop_personnel.personnel and mission.mission_type != 'h' \
                        and mission.is_in_payment:
                    if mission.from_date.__ge__(contract_start[contract.id]) and mission.to_date.__le__(
                            contract_end[contract.id]):
                        mission_day += mission.time_period
                    elif mission.from_date.__lt__(contract_start[contract.id]) and mission.to_date.__le__(
                            contract_end[contract.id]) and \
                            mission.to_date.__gt__(contract_start[contract.id]):
                        mission_day += mission.to_date.day
                    elif mission.from_date.__gt__(contract_start[contract.id]) and mission.to_date.__gt__(
                            contract_end[contract.id]) and \
                            mission.from_date.__le__(contract_end[contract.id]):
                        mission_day += contract_end[contract.id].day - mission.from_date.day
                    elif mission.from_date.__le__(contract_start[contract.id]) and mission.to_date.__ge__(
                            contract_end[contract.id]):
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

    @property
    def bank_report(self):
        response = []
        for item in self.list_of_pay_item.all():
            if item.payable > 0:
                response.append(item.bank_report)
        return response

    @property
    def form_bank_report(self):
        response = []
        for item in self.list_of_pay_item.all():
            response.append(item.bank_report)
        return response

    @property
    def bank_report_with_comma(self):
        response = []
        for item in self.list_of_pay_item.all():
            response.append(item.bank_report_with_comma)
        return response

    @property
    def get_items(self):
        return self.list_of_pay_item.all()

    @property
    def month_tax(self):
        tax = 0
        for item in self.list_of_pay_item.all():
            tax += item.total_tax
        return round(tax)

    @property
    def total(self):
        response = {
            'normal_worktime': 0,
            'real_worktime': 0,
            'hoghoogh_mahane': 0,
            'sanavat_mahane': 0,
            'ezafe_kari_total': 0,
            'tatil_kari_total': 0,
            'shab_kari_total': 0,
            'mission_total': 0,
            'aele_mandi': 0,
            'haghe_maskan': 0,
            'haghe_jazb': 0,
            'kharo_bar': 0,
            'sayer_hr': 0,
            'haghe_sanavat_total': 0,
            'padash_total': 0,
            'sayer_ezafat': 0,
            'total_payment': 0,
            'haghe_bime_bime_shavande': 0,
            'total_tax': 0,
            'dept_amount': 0,
            'loan_amount': 0,
            'check_and_get_optional_deduction_episode': 0,
            'kasre_kar_total': 0,
            'sayer_kosoorat': 0,
            'payable': 0,
                    }
        for item in self.list_of_pay_item.all():
            response['normal_worktime'] += item.normal_worktime
            response['real_worktime'] += item.real_worktime
            response['hoghoogh_mahane'] += item.hoghoogh_mahane
            response['sanavat_mahane'] += item.sanavat_mahane
            response['ezafe_kari_total'] += item.ezafe_kari_total
            response['tatil_kari_total'] += item.tatil_kari_total
            response['shab_kari_total'] += item.shab_kari_total
            response['mission_total'] += item.mission_total
            response['aele_mandi'] += item.aele_mandi
            response['haghe_maskan'] += item.haghe_maskan
            response['haghe_jazb'] += item.haghe_jazb
            response['kharo_bar'] += item.kharo_bar
            response['sayer_hr'] += item.sayer_hr
            response['haghe_sanavat_total'] += item.haghe_sanavat_total
            response['padash_total'] += item.padash_total
            response['sayer_ezafat'] += item.sayer_ezafat
            response['total_payment'] += item.total_payment
            response['haghe_bime_bime_shavande'] += item.haghe_bime_bime_shavande
            response['total_tax'] += item.total_tax
            response['dept_amount'] += item.dept_amount
            response['loan_amount'] += item.loan_amount
            response['check_and_get_optional_deduction_episode'] += item.check_and_get_optional_deduction_episode
            response['kasre_kar_total'] += item.kasre_kar_total
            response['sayer_kosoorat'] += item.sayer_kosoorat
            response['payable'] += item.payable
        return response

    @property
    def total_tax_naghdi_pension(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.tax_naghdi_pension
        return round(total)

    @property
    def total_gheyre_naghdi_tax_pension(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.gheyre_naghdi_tax_pension
        return round(total)

    @property
    def total_hazine_made_137(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.hazine_made_137
        return round(total)

    @property
    def total_haghe_bime_moafiat(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.haghe_bime_moafiat
        return round(total)

    @property
    def total_sayer_moafiat(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.total_sayer_moafiat
        return round(total)

    @property
    def total_ezafe_kari_nakhales(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.ezafe_kari_nakhales
        return round(total)

    @property
    def total_tax_naghdi_un_pension(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.tax_naghdi_un_pension
        return round(total)

    @property
    def mission_total(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.mission_total
        return round(total)

    @property
    def padash_total(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.padash_total
        return round(total)

    @property
    def total_mazaya_gheyr_mostamar(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.mazaya_gheyr_mostamar
        return round(total)

    @property
    def total_hagh_sanavat_and_save_leaves(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.get_hagh_sanavat_and_save_leaves
        return round(total)

    @property
    def total_manategh_tejari_moafiat(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.manategh_tejari_moafiat
        return round(total)

    @property
    def total_ejtenab_maliat_mozaaf(self):
        total = 0
        for item in self.list_of_pay_item.all():
            total += item.ejtenab_maliat_mozaaf
        return round(total)

    @property
    def sign_date(self):
        date = jdatetime.date(self.year, self.month, self.month_days)
        return str(date.__str__().replace('-', ''))

    def __str__(self):
        return 'حقوق و دستمزد ' + ' ' + str(self.year) + '/' + str(self.month) + ' کارگاه ' + \
               self.workshop.workshop_title

    def delete(self, *args, **kwargs):
        for my_list in self.list_of_pay_item.all():
            for loan in my_list.workshop_personnel.loan.all():
                for item in loan.item.all():
                    if item.date == self.start_date:
                        item.payed_amount = 0
                        item.save()
        super().delete()




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
    hr_letter = models.ForeignKey(HRLetter, related_name='list_of_pay_item', on_delete=models.CASCADE, blank=True,
                                  null=True)
    contract_row = models.ForeignKey(ContractRow, related_name="list_of_pay_item", on_delete=models.CASCADE,
                                     blank=True, null=True)
    cumulative_absence = models.IntegerField(default=0)
    cumulative_mission = models.IntegerField(default=0)
    cumulative_entitlement = models.IntegerField(default=0)
    cumulative_illness = models.IntegerField(default=0)
    cumulative_without_salary = models.IntegerField(default=0)

    hoghoogh_roozane = DECIMAL()
    pay_base = DECIMAL(default=0)
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
    mission_nerkh = models.DecimalField(max_digits=24, default=1, decimal_places=4)

    ezafe_kari = models.DecimalField(default=0, max_digits=24, decimal_places=6)
    ezafe_kari_amount = DECIMAL(default=0)
    ezafe_kari_nerkh = models.DecimalField(max_digits=24, default=1.96, decimal_places=4)
    ezafe_kari_total = models.IntegerField(default=0)

    tatil_kari = models.DecimalField(default=0, max_digits=24, decimal_places=6)
    tatil_kari_amount = DECIMAL(default=0)
    tatil_kari_nerkh = models.DecimalField(max_digits=24, default=1.96, decimal_places=4)
    tatil_kari_total = models.IntegerField(default=0)

    kasre_kar = models.DecimalField(default=0, max_digits=24, decimal_places=6)
    kasre_kar_amount = DECIMAL(default=0)
    kasre_kar_nerkh = models.DecimalField(max_digits=24, default=1.4, decimal_places=4)
    kasre_kar_total = models.IntegerField(default=0)

    shab_kari = models.DecimalField(default=0, max_digits=24, decimal_places=6)
    shab_kari_amount = DECIMAL(default=0)
    shab_kari_nerkh = models.DecimalField(max_digits=24, default=0.35, decimal_places=4)
    shab_kari_total = models.IntegerField(default=0)

    nobat_kari_sob_asr = models.DecimalField(default=0, max_digits=24, decimal_places=6)
    nobat_kari_sob_asr_amount = DECIMAL(default=0)
    nobat_kari_sob_asr_nerkh = models.DecimalField(max_digits=24, default=0.1, decimal_places=4)

    nobat_kari_sob_shab = models.DecimalField(default=0, max_digits=24, decimal_places=6)
    nobat_kari_sob_shab_amount = DECIMAL(default=0)
    nobat_kari_sob_shab_nerkh = models.DecimalField(max_digits=24, default=0.225, decimal_places=4)

    nobat_kari_asr_shab = models.DecimalField(default=0, max_digits=24, decimal_places=6)
    nobat_kari_asr_shab_amount = DECIMAL(default=0)
    nobat_kari_asr_shab_nerkh = models.DecimalField(max_digits=24, default=0.025, decimal_places=4)

    nobat_kari_sob_asr_shab = models.DecimalField(default=0, max_digits=24, decimal_places=6)
    nobat_kari_sob_asr_shab_amount = DECIMAL(default=0)
    nobat_kari_sob_asr_shab_nerkh = models.DecimalField(max_digits=24, default=0.15, decimal_places=4)

    aele_mandi_amount = DECIMAL(default=0)
    aele_mandi_nerkh = models.DecimalField(max_digits=24, default=3, decimal_places=4)
    aele_mandi = models.IntegerField(default=0)

    haghe_sanavat_total = models.IntegerField(default=0)
    saved_leaves_total = DECIMAL(default=0)

    sayer_ezafat = DECIMAL(default=0)
    sayer_kosoorat = DECIMAL(default=0)
    padash_total = models.IntegerField(default=0)
    mazaya_gheyr_mostamar = DECIMAL(default=0)
    calculate_payment = models.BooleanField(default=False)

    # tax kosoorat
    hazine_made_137 = models.IntegerField(default=0)
    kosoorat_insurance = models.IntegerField(default=0)
    sayer_moafiat = models.IntegerField(default=0)
    manategh_tejari_moafiat = models.IntegerField(default=0)
    ejtenab_maliat_mozaaf = models.IntegerField(default=0)
    naghdi_gheye_naghdi_tax = models.IntegerField(default=0)

    total_payment = models.IntegerField(default=0)

    '''for payment'''
    payment_done = models.BooleanField(default=False)
    paid_amount = models.IntegerField(default=0)

    total_tax = DECIMAL(default=0)
    save_leave = DECIMAL(default=0)
    loan_amount = DECIMAL(default=0)
    dept_amount = DECIMAL(default=0)

    insurance = models.BooleanField(default=False)
    insurance_day = models.IntegerField(default=0)

    taamin_ejtemaee = DECIMAL(default=0)

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
    def year_real_work_month(self):
        items = ListOfPayItem.objects.filter(
            Q(list_of_pay__year=self.list_of_pay.year) &
            Q(list_of_pay__month__lte=self.list_of_pay.month) &
            Q(list_of_pay__ultimate=True) &
            Q(workshop_personnel=self.workshop_personnel)
        )
        total = 0
        for item in items:
            is_tax, tax_day = item.check_tax
            total += tax_day
        return round(total, 2)

    @property
    def sanavat_notice(self):
        if not self.get_hr_letter.paye_sanavat_amount and self.workshop_personnel.total_insurance >= 12:
            return True
        else:
            return False

    @property
    def sanavat_verify(self):
        if not self.get_hr_letter.paye_sanavat_amount and self.workshop_personnel.total_insurance >= 12:
            return 'حکم جدید صادرشود'
        else:
            return 'تایید'

    @staticmethod
    def with_comma(input_amount, no_minus=False):
        if input_amount != 0:
            amount = str(round(input_amount))[::-1]
            loop = int(len(amount) / 3)
            if len(amount) < 4:
                return str(round(input_amount))
            else:
                counter = 0
                for i in range(1, loop + 1):
                    index = (i * 3) + counter
                    counter += 1
                    amount = amount[:index] + ',' + amount[index:]
            if amount[-1] == ',':
                amount = amount[:-1]
            if no_minus:
                return amount[::-1].replace('-', '')
            return amount[::-1]
        else:
            return 0

    @staticmethod
    def decimal_to_time(number):
        hour = int(number)
        minute = (number - Decimal(hour)) * Decimal(60)
        return str(hour) + ':' + str(round(minute))

    @property
    def quit_job(self):
        if self.contract.quit_job_date:
            return self.contract.quit_job_date
        else:
            return ''

    @property
    def absence_sum(self):
        return int(self.absence_day) + int(self.cumulative_absence)

    @property
    def illness_sum(self):
        return int(self.illness_leave_day) + int(self.cumulative_illness)

    @property
    def without_salary_sum(self):
        return int(self.without_salary_leave_day) + int(self.cumulative_without_salary)

    @property
    def entitlement_sum(self):
        return round(self.entitlement_leave_day, 2) + round(self.cumulative_entitlement, 2)

    @property
    def mission_sum(self):
        return int(self.mission_day) + int(self.cumulative_mission)

    @property
    def kasre_kar_time(self):
        return self.decimal_to_time(self.kasre_kar)

    @property
    def ezafe_kari_time(self):
        return self.decimal_to_time(self.ezafe_kari)

    @property
    def tatil_kari_time(self):
        return self.decimal_to_time(self.tatil_kari)

    @property
    def shab_kari_time(self):
        return self.decimal_to_time(self.shab_kari)

    @property
    def hoghoogh_mahane_with_comma(self):
        return self.with_comma(self.hoghoogh_mahane)

    @property
    def mazaya_gheyr_mostamar_with_comma(self):
        return self.with_comma(self.mazaya_gheyr_mostamar)

    @property
    def sayer_kosoorat_with_comma(self):
        return self.with_comma(self.sayer_kosoorat)

    @property
    def haghe_maskan(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.haghe_maskan_amount))

    @property
    def haghe_jazb(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.haghe_jazb_amount))

    @property
    def kharo_bar(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.bon_kharo_bar_amount))

    @property
    def haghe_sarparasti(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.haghe_sarparasti_amount))

    @property
    def haghe_modiriyat(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.haghe_modiriyat_amount))

    @property
    def fogholade_shoghl(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.fogholade_shoghl_amount))

    @property
    def haghe_tahsilat(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.haghe_tahsilat_amount))

    @property
    def fogholade_sakhti_kar(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.fogholade_sakhti_kar_amount))

    @property
    def haghe_ankal(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.haghe_ankal_amount))

    @property
    def fogholade_badi(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.fogholade_badi_abohava_amount))

    @property
    def mahroomiat_tashilat_zendegi(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.mahroomiat_tashilat_zendegi_amount))

    @property
    def fogholade_mahal_khedmat(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.fogholade_mahal_khedmat_amount))

    @property
    def fogholade_sharayet_mohit_kar(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.fogholade_sharayet_mohit_kar_amount))

    @property
    def ayabo_zahab(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.ayabo_zahab_amount))

    @property
    def yarane_ghaza(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.yarane_ghaza_amount))

    @property
    def haghe_shir(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.haghe_shir_amount))

    @property
    def haghe_taahol(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.haghe_taahol_amount))

    @property
    def komakhazine_mahdekoodak(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.komakhazine_mahdekoodak_amount))

    @property
    def komakhazine_varzesh(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.komakhazine_varzesh_amount))

    @property
    def komakhazine_mobile(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.komakhazine_mobile_amount))

    @property
    def mazaya_mostamar_gheyre_naghdi(self):
        hr = self.get_hr_letter
        return round(self.calculate_hr_item_in_real_work_time(hr.mazaya_mostamar_gheyre_naghdi_amount))

    @property
    def sayer_hr(self):
        hr = self.get_hr_letter
        total = 0
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_sarparasti_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_modiriyat_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.fogholade_shoghl_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_tahsilat_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.fogholade_sakhti_kar_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_ankal_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.fogholade_badi_abohava_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.mahroomiat_tashilat_zendegi_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.fogholade_mahal_khedmat_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.fogholade_sharayet_mohit_kar_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.ayabo_zahab_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.yarane_ghaza_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_shir_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.haghe_taahol_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_mahdekoodak_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_varzesh_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.komakhazine_mobile_amount)
        total += self.calculate_hr_item_in_real_work_time(hr.mazaya_mostamar_gheyre_naghdi_amount)
        return total

    @property
    def sayer_ezafat_with_comma(self):
        return self.with_comma(self.sayer_ezafat)

    @property
    def hoghoogh_roozane_with_comma(self):
        return self.with_comma(self.hoghoogh_roozane)

    @property
    def sanavat_base_with_comma(self):
        return self.with_comma(self.sanavat_base)

    @property
    def sanavat_mahane_with_comma(self):
        return self.with_comma(self.sanavat_mahane)

    @property
    def kasre_kar_total_with_comma(self):
        return self.with_comma(self.kasre_kar_total)

    @property
    def ezafe_kari_total_with_comma(self):
        return self.with_comma(self.ezafe_kari_total)

    @property
    def tatil_kari_total_with_comma(self):
        return self.with_comma(self.tatil_kari_total)

    @property
    def shab_kari_total_with_comma(self):
        return self.with_comma(self.shab_kari_total)

    @property
    def mission_total_with_comma(self):
        return self.with_comma(self.mission_total)

    @property
    def nobat_kari_sob_shab_total_with_comma(self):
        return self.with_comma(self.nobat_kari_sob_shab_total)

    @property
    def nobat_kari_sob_asr_total_with_comma(self):
        return self.with_comma(self.nobat_kari_sob_asr_total)

    @property
    def nobat_kari_asr_shab_total_with_comma(self):
        return self.with_comma(self.nobat_kari_asr_shab_total)

    @property
    def nobat_kari_sob_asr_shab_total_with_comma(self):
        return self.with_comma(self.nobat_kari_sob_asr_shab_total)

    @property
    def padash_total_with_comma(self):
        return self.with_comma(self.padash_total)

    @property
    def haghe_sanavat_total_with_comma(self):
        return self.with_comma(self.haghe_sanavat_total)

    @property
    def aele_mandi_with_comma(self):
        return self.with_comma(self.aele_mandi)

    @property
    def total_payment_with_comma(self):
        return self.with_comma(self.total_payment)

    @property
    def sayer_ezafat_with_comma(self):
        return self.with_comma(self.sayer_ezafat)

    @property
    def DSW_MAH_with_comma(self):
        return self.with_comma(self.data_for_insurance['DSW_MAH'])

    @property
    def DSW_MAZ_with_comma(self):
        return self.with_comma(self.data_for_insurance['DSW_MAZ'])

    @property
    def DSW_MASH_with_comma(self):
        return self.with_comma(self.data_for_insurance['DSW_MASH'])

    @property
    def DSW_TOTL_with_comma(self):
        return self.with_comma(self.data_for_insurance['DSW_TOTL'])

    @property
    def DSW_BIME_with_comma(self):
        return self.with_comma(self.data_for_insurance['DSW_BIME'])

    @property
    def moaf_sum_with_comma(self):
        return self.with_comma(self.moaf_sum)

    @property
    def haghe_bime_bime_shavande_with_comma(self):
        return self.with_comma(self.haghe_bime_bime_shavande)

    @property
    def calculate_month_tax_with_comma(self):
        return self.with_comma(self.total_tax)

    @property
    def payable_with_comma(self):
        return self.with_comma(self.payable)

    @property
    def employer_insurance_with_comma(self):
        return self.with_comma(self.employer_insurance)

    @property
    def un_employer_insurance_with_comma(self):
        return self.with_comma(self.un_employer_insurance)

    @property
    def tax_included_payment_with_comma(self):
        return self.with_comma(self.tax_included_payment)

    @property
    def calculate_month_tax_with_comma(self):
        return self.with_comma(self.calculate_month_tax)

    @property
    def check_and_get_dept_episode_with_comma(self):
        return self.with_comma(self.check_and_get_dept_episode)

    @property
    def check_and_get_loan_episode_with_comma(self):
        return self.with_comma(self.check_and_get_loan_episode)

    @property
    def check_and_get_optional_deduction_episode_with_comma(self):
        return self.with_comma(self.check_and_get_optional_deduction_episode)

    def set_info_from_workshop(self):
        hr = self.get_hr_letter
        self.hoghoogh_roozane = hr.hoghooghe_roozane_amount
        hourly_pay = round((self.hoghoogh_roozane / Decimal(7.33)), 6)

        if self.workshop_personnel.workshop.tax_employer_type == 1:
            self.taamin_ejtemaee = 1
        elif self.workshop_personnel.workshop.tax_employer_type == 2:
            self.taamin_ejtemaee = 2 / 7
        if self.workshop_personnel.workshop.base_pay_type == 'd':
            self.pay_base = hr.daily_pay_base
            self.hourly_pay_base = hr.day_hourly_pay_base
        elif self.workshop_personnel.workshop.base_pay_type == 'm':
            self.pay_base = hr.monthly_pay_base
            self.hourly_pay_base = hr.month_hourly_pay_base

        self.ezafe_kari_nerkh = self.workshop_personnel.workshop.ezafe_kari_nerkh + Decimal(1)
        if self.get_hr_letter.ezafe_kari_pay_type == 'd':
            self.ezafe_kari_amount = hourly_pay
        elif self.get_hr_letter.ezafe_kari_pay_type == 'b':
            self.ezafe_kari_amount = self.hourly_pay_base

        self.tatil_kari_nerkh = self.workshop_personnel.workshop.tatil_kari_nerkh + Decimal(1)
        if self.get_hr_letter.tatil_kari_pay_type == 'd':
            self.tatil_kari_amount = hourly_pay
        elif self.get_hr_letter.tatil_kari_pay_type == 'b':
            self.tatil_kari_amount = self.hourly_pay_base

        self.kasre_kar_nerkh = self.workshop_personnel.workshop.kasre_kar_nerkh + Decimal(1)
        if self.get_hr_letter.kasre_kar_pay_type == 'd':
            self.kasre_kar_amount = hourly_pay
        elif self.get_hr_letter.kasre_kar_pay_type == 'b':
            self.kasre_kar_amount = self.hourly_pay_base

        self.shab_kari_nerkh = self.workshop_personnel.workshop.shab_kari_nerkh + Decimal(1)
        if self.get_hr_letter.shab_kari_pay_type == 'd':
            self.shab_kari_amount = hourly_pay
        elif self.get_hr_letter.shab_kari_pay_type == 'b':
            self.shab_kari_amount = self.hourly_pay_base

        self.nobat_kari_sob_asr_nerkh = self.workshop_personnel.workshop.nobat_kari_sob_asr_nerkh + Decimal(1)
        if self.get_hr_letter.nobat_kari_sob_asr_pay_type == 'd':
            self.nobat_kari_sob_asr_amount = self.hoghoogh_roozane
        elif self.get_hr_letter.nobat_kari_sob_asr_pay_type == 'b':
            self.nobat_kari_sob_asr_amount = self.pay_base

        self.nobat_kari_sob_shab_nerkh = self.workshop_personnel.workshop.nobat_kari_sob_shab_nerkh + Decimal(1)
        if self.get_hr_letter.nobat_kari_sob_shab_pay_type == 'd':
            self.nobat_kari_sob_shab_amount = self.hoghoogh_roozane
        elif self.get_hr_letter.nobat_kari_sob_shab_pay_type == 'b':
            self.nobat_kari_sob_shab_amount = self.pay_base

        self.nobat_kari_asr_shab_nerkh = self.workshop_personnel.workshop.nobat_kari_asr_shab_nerkh + Decimal(1)
        if self.get_hr_letter.nobat_kari_asr_shab_pay_type == 'd':
            self.nobat_kari_asr_shab_amount = self.hoghoogh_roozane
        elif self.get_hr_letter.nobat_kari_asr_shab_pay_type == 'b':
            self.nobat_kari_asr_shab_amount = self.pay_base

        self.nobat_kari_sob_asr_shab_nerkh = self.workshop_personnel.workshop.nobat_kari_sob_asr_shab_nerkh + Decimal(1)
        if self.get_hr_letter.nobat_kari_sob_asr_shab_pay_type == 'd':
            self.nobat_kari_sob_asr_shab_amount = self.hoghoogh_roozane
        elif self.get_hr_letter.nobat_kari_sob_asr_shab_pay_type == 'b':
            self.nobat_kari_sob_asr_shab_amount = self.pay_base

        self.aele_mandi_nerkh = self.workshop_personnel.workshop.aele_mandi_nerkh
        if self.get_hr_letter.aele_mandi_pay_type == 'd':
            self.aele_mandi_amount = self.hoghoogh_roozane
        elif self.get_hr_letter.aele_mandi_pay_type == 'b':
            self.aele_mandi_amount = self.pay_base

        self.mission_nerkh = self.workshop_personnel.workshop.mission_pay_nerkh + Decimal(1)
        if self.get_hr_letter.mission_pay_type == 'd':
            self.mission_amount = self.hoghoogh_roozane
        elif self.get_hr_letter.mission_pay_type == 'b':
            self.mission_amount = self.pay_base

    @property
    def get_hr_letter(self):
        if self.hr_letter:
            return self.hr_letter
        else:
            hr = self.contract.hr_letter.all()
            hr = hr.filter(Q(is_verified=True) & Q(is_active=True))
            hr = hr.first()
            if not hr:
                raise ValidationError('حکم کارگزینی فعال موجود نیست')
            return hr

    def calculate_hr_item_in_real_work_time(self, item):
        if item:
            total = Decimal(self.real_worktime) * item / Decimal(self.list_of_pay.month_days)
            return total
        else:
            return 0

    def calculate_hr_item_in_insurance_time(self, item):
        is_insurance, insurance_worktime = self.check_insurance
        if item and is_insurance:
            total = Decimal(insurance_worktime) * item / Decimal(self.list_of_pay.month_days)
            return total
        else:
            return 0

    def calculate_hr_item_in_tax_time(self, item):
        is_tax, tax_day = self.check_tax
        if item and is_tax:
            total = Decimal(tax_day) * item / Decimal(self.list_of_pay.month_days)
            return total
        else:
            return 0

    @property
    def get_aele_mandi_info(self):
        self.total_insurance_month = self.workshop_personnel.insurance_history_total
        if self.total_insurance_month >= 24 and self.workshop_personnel.personnel.insurance:
            children = self.workshop_personnel.personnel.childs
            aele_mandi_child = 0
            for child in children:
                if child.marital_status == 's':
                    person_age = self.list_of_pay.year - child.date_of_birth.year
                    if person_age <= 18 or child.physical_condition != 'h':
                        aele_mandi_child += 1
            self.aele_mandi_child = aele_mandi_child
            return aele_mandi_child
        else:
            self.aele_mandi_child = 0
            self.total_insurance_month = 0
            return 0

    @property
    def is_insurance_display(self):
        is_tax, work_time = self.check_tax
        if is_tax:
            return 'بیمه شده'
        else:
            return 'بیمه نشده'

    @property
    def get_sanavt_info(self):
        hr = self.get_hr_letter
        sanavat_month = 0
        if self.workshop_personnel.workshop.sanavat_type == 'c':
            sanavat_month = self.workshop_personnel.total_insurance
        elif self.workshop_personnel.workshop.sanavat_type == 'n':
            sanavat_month = self.workshop_personnel.insurance_history_total
        return hr.paye_sanavat_amount or 0, sanavat_month

    @property
    def hoghoogh_mahane(self):
        return round(self.hoghoogh_roozane * self.real_worktime)

    @property
    def sanavat_mahane(self):
        if self.sanavat_month >= 12:
            return round(self.sanavat_base * self.real_worktime)
        else:
            return 0

    @property
    def mission_total(self):
        return round(Decimal(self.mission_sum) * self.mission_nerkh * self.mission_amount)

    @property
    def get_aele_mandi(self):
        work_time = self.real_worktime
        if self.workshop_personnel.workshop.illness_absence_in_real_work:
            work_time += self.illness_leave_day
        if self.aele_mandi_child != 0:
            month_day = self.list_of_pay.month_days
            aele_mandi = Decimal(self.aele_mandi_child) * self.aele_mandi_amount * self.aele_mandi_nerkh * \
                         Decimal(work_time) / Decimal(month_day)
            self.aele_mandi = aele_mandi
            return aele_mandi
        else:
            self.aele_mandi = 0
            return 0

    @property
    def aele_mandi_in_tax(self):
        is_tax, work_time = self.check_tax
        if self.aele_mandi_child != 0:
            month_day = self.list_of_pay.month_days
            aele_mandi = Decimal(self.aele_mandi_child) * self.aele_mandi_amount * self.aele_mandi_nerkh * \
                         Decimal(work_time) / Decimal(month_day)
            return aele_mandi
        else:
            return 0

    @property
    def aele_mandi_in_insurance(self):
        is_insurance, work_time = self.check_insurance
        if self.aele_mandi_child != 0:
            month_day = self.list_of_pay.month_days
            aele_mandi = Decimal(self.aele_mandi_child) * self.aele_mandi_amount * self.aele_mandi_nerkh * \
                         Decimal(work_time) / Decimal(month_day)
            return aele_mandi
        else:
            return 0

    @property
    def get_ezafe_kari(self):
        return self.ezafe_kari_amount * Decimal(self.ezafe_kari_nerkh) * Decimal(self.ezafe_kari)

    @property
    def get_tatil_kari(self):
        return self.tatil_kari_amount * Decimal(self.tatil_kari_nerkh) * Decimal(self.tatil_kari)

    @property
    def get_shab_kari(self):
        return self.shab_kari * Decimal(self.shab_kari_nerkh) * Decimal(self.shab_kari_amount)

    @property
    def get_kasre_kar(self):
        return self.kasre_kar_amount * Decimal(self.kasre_kar_nerkh) * Decimal(self.kasre_kar)

    @property
    def nobat_kari_sob_shab_total(self):
        return round(Decimal(self.nobat_kari_sob_shab) *
                     self.nobat_kari_sob_shab_nerkh * self.nobat_kari_sob_shab_amount)

    @property
    def nobat_kari_sob_asr_total(self):
        return round(Decimal(self.nobat_kari_sob_asr) *
                     self.nobat_kari_sob_asr_nerkh * self.nobat_kari_sob_asr_amount)

    @property
    def nobat_kari_asr_shab_total(self):
        return round(Decimal(self.nobat_kari_asr_shab) *
                     self.nobat_kari_asr_shab_nerkh * self.nobat_kari_asr_shab_amount)

    @property
    def nobat_kari_sob_asr_shab_total(self):
        return round(Decimal(self.nobat_kari_sob_asr_shab) *
                     self.nobat_kari_sob_asr_shab_nerkh * self.nobat_kari_sob_asr_shab_amount)

    @property
    def get_total_payment(self):
        self.hr_letter = self.get_hr_letter
        self.hr_letter.is_calculated = False
        self.hr_letter.save()
        total = Decimal(0)

        total += self.hoghoogh_mahane
        total += self.sanavat_mahane
        total += self.mission_total

        total += self.get_aele_mandi
        self.aele_mandi = round(self.get_aele_mandi)

        total += self.get_ezafe_kari
        self.ezafe_kari_total = self.get_ezafe_kari

        total += self.get_tatil_kari
        self.tatil_kari_total = round(self.get_tatil_kari)

        total += self.get_shab_kari
        self.shab_kari_total = round(self.get_shab_kari)

        total += self.nobat_kari_sob_asr_total
        total += self.nobat_kari_sob_shab_total
        total += self.nobat_kari_asr_shab_total
        total += self.nobat_kari_sob_asr_shab_total

        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.haghe_sarparasti_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.haghe_modiriyat_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.haghe_jazb_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.fogholade_shoghl_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.haghe_tahsilat_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.fogholade_sakhti_kar_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.haghe_ankal_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.fogholade_badi_abohava_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.mahroomiat_tashilat_zendegi_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.fogholade_mahal_khedmat_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.fogholade_sharayet_mohit_kar_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.haghe_maskan_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.ayabo_zahab_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.bon_kharo_bar_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.yarane_ghaza_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.haghe_taahol_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.haghe_shir_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.komakhazine_mahdekoodak_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.komakhazine_varzesh_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.komakhazine_mobile_amount)
        total += self.calculate_hr_item_in_real_work_time(self.hr_letter.mazaya_mostamar_gheyre_naghdi_amount)

        total += self.mazaya_gheyr_mostamar
        total += self.sayer_ezafat

        self.padash_total = round(self.get_padash)
        total += Decimal(self.padash_total)

        self.haghe_sanavat_total = round(self.get_hagh_sanavat)
        total += Decimal(self.haghe_sanavat_total)

        self.saved_leaves_total = round(self.get_save_leave)
        total += Decimal(self.saved_leaves_total)

        self.kasre_kar_total = round(self.get_kasre_kar)

        self.loan_amount = self.check_and_get_loan_episode
        self.dept_amount = self.check_and_get_dept_episode

        return total

    @property
    def gheyre_naghdi_tax_pension(self):
        hr = self.get_hr_letter
        return self.calculate_hr_item_in_tax_time(hr.mazaya_mostamar_gheyre_naghdi_amount)

    @property
    def gheyre_naghdi_pension_whit_comma(self):
        return self.with_comma(self.gheyre_naghdi_tax_pension)

    @property
    def payable(self):
        payable_amount = Decimal(round(self.total_payment) - round(self.total_tax) - round(self.dept_amount) - \
                                 round(self.check_and_get_optional_deduction_episode) - round(
            self.haghe_bime_bime_shavande) - \
                                 round(self.loan_amount)) - round(self.kasre_kar_total) - round(self.sayer_kosoorat)
        return round(payable_amount)

    '''calculate'''

    @property
    def calculate_yearly_haghe_sanavat(self):
        hr = self.get_hr_letter
        year_worktime = 0
        if self.workshop_personnel.workshop.haghe_sanavat_pay_type == 'b':
            base_pay = hr.daily_pay_base
        else:
            base_pay = self.list_of_pay.workshop.hade_aghal_hoghoogh

        previous_items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                                      & Q(list_of_pay__year__lt=self.list_of_pay.year)
                                                      & Q(list_of_pay__ultimate=True))
        if self.workshop_personnel.workshop.haghe_sanavat_type == 'o':
            work_years = []
            for item in previous_items:
                if item.list_of_pay.year not in work_years:
                    work_years.append(item.list_of_pay.year)
            total_worktime = 0
            list_of_pay_items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                                             & Q(list_of_pay__year__lte=self.list_of_pay.year)
                                                             & Q(list_of_pay__ultimate=True))
            for pay_list in list_of_pay_items:
                total_worktime += pay_list.real_worktime
                total_worktime += pay_list.illness_leave_day

            until_this_year = round(base_pay) * 30 * total_worktime / (len(work_years) + 1)
            list_of_pay_item = ListOfPayItem.objects.filter(list_of_pay__year=work_years[0]).first()
            return until_this_year - list_of_pay_item.calculate_yearly_haghe_sanavat

        elif self.workshop_personnel.workshop.haghe_sanavat_type == 'c':
            items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                                 & Q(list_of_pay__year=self.list_of_pay.year)
                                                 & Q(list_of_pay__ultimate=True))
            for item in items:
                year_worktime += item.real_worktime
                year_worktime += item.illness_leave_day
            return round(base_pay) * 30 * year_worktime / 365

    @property
    def calculate_monthly_haghe_sanavat(self):
        hr = self.get_hr_letter
        if self.workshop_personnel.workshop.haghe_sanavat_pay_type == 'b':
            base_pay = hr.daily_pay_base
        else:
            base_pay = self.list_of_pay.workshop.hade_aghal_hoghoogh
        return round(base_pay) * 30 * (self.real_worktime + self.illness_leave_day) / 365

    @property
    def get_hagh_sanavat(self):
        sanavat = 0
        if self.list_of_pay.workshop.haghe_sanavat_identification == 'm':
            sanavat += self.calculate_monthly_haghe_sanavat

        elif self.list_of_pay.workshop.haghe_sanavat_identification == 'y' and self.list_of_pay.month == 12:
            sanavat += self.calculate_yearly_haghe_sanavat
        return sanavat

    @property
    def calculate_save_leave(self):
        hr = self.get_hr_letter
        year_worktime = 0
        save_leave_days = 0
        items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                             & Q(list_of_pay__year=self.list_of_pay.year)
                                             & Q(list_of_pay__ultimate=True))

        for item in items:
            year_worktime += item.real_worktime
            year_worktime -= item.matter_47_leave_day

        year_worktime += self.real_worktime
        year_worktime -= self.matter_47_leave_day

        leave_available = self.workshop_personnel.save_leave_limit * year_worktime / 365
        leave_limit_available = 9 * year_worktime / 365

        leave_available += self.workshop_personnel.save_leaave

        for item in items:
            leave_available -= item.entitlement_leave_day

        if self.workshop_personnel.workshop.save_absence_limit:
            if leave_available > leave_limit_available:
                save_leave_days = leave_limit_available
            elif leave_available <= leave_limit_available:
                save_leave_days = leave_available
        else:
            save_leave_days = leave_available

        if self.workshop_personnel.workshop.leave_save_pay_type == 'h':
            pay_base = hr.calculate_save_leave_base
        else:
            pay_base = self.workshop_personnel.workshop.hade_aghal_hoghoogh

        save_leave_amount = save_leave_days * pay_base

        return save_leave_days, round(save_leave_amount), round(pay_base)

    @property
    def get_save_leave_day(self):
        day, amount, day_amount = self.calculate_save_leave
        return day

    @property
    def get_save_leave_day_amount(self):
        day, amount, day_amount = self.calculate_save_leave
        return day_amount

    @property
    def get_save_leave_amount(self):
        day, amount, day_amount = self.calculate_save_leave
        return amount

    @property
    def get_save_leave(self):
        if self.list_of_pay.month == 12 and not self.workshop_personnel.workshop.save_absence_transfer_next_year:
            self.save_leave = self.get_save_leave_amount
            return self.get_save_leave_amount
        elif self.list_of_pay.month == 12 and self.workshop_personnel.workshop.save_absence_transfer_next_year:
            self.workshop_personnel.save_leaave += self.get_save_leave_day
            self.workshop_personnel.save()
            return 0
        else:
            return 0

    @property
    def get_hagh_sanavat_and_save_leaves(self):
        return self.haghe_sanavat_total + self.saved_leaves_total

    @property
    def unpaid(self):
        return round(self.payable - self.paid_amount) + self.get_unpaid_of_year

    @property
    def get_unpaid_of_year(self):
        items = ListOfPayItem.objects.filter(Q(list_of_pay__year=self.list_of_pay.year) &
                                             Q(list_of_pay__month__lt=self.list_of_pay.month) &
                                             Q(workshop_personnel=self.workshop_personnel) &
                                             Q(list_of_pay__ultimate=True)).all()
        unpaid = 0
        for item in items:
            unpaid += (item.payable - item.paid_amount)
        return round(unpaid)

    @property
    def total_unpaid(self):
        return round(self.get_unpaid_of_year) + round(self.payable)

    @property
    def unpaid_till_this_month(self):
        return round(self.get_unpaid_of_year) + round(self.payable) - self.paid_amount

    @property
    def calculate_yearly_eydi(self):
        hr = self.get_hr_letter
        year_worktime = 0
        if self.workshop_personnel.workshop.eydi_padash_pay_type == 'b':
            base_pay = hr.daily_pay_base
        else:
            base_pay = self.list_of_pay.workshop.hade_aghal_hoghoogh

        items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                             & Q(list_of_pay__year=self.list_of_pay.year)
                                             & Q(list_of_pay__ultimate=True))
        for item in items:
            year_worktime += item.real_worktime
            year_worktime += item.illness_leave_day
        padash = round(base_pay) * 60 * year_worktime / 365
        padash_limit = round(self.list_of_pay.workshop.hade_aghal_hoghoogh) * 90 * year_worktime / 365

        if padash > padash_limit:
            return padash_limit
        else:
            return padash

    @property
    def calculate_monthly_eydi(self):
        hr = self.get_hr_letter
        if self.workshop_personnel.workshop.eydi_padash_pay_type == 'b':
            base_pay = hr.daily_pay_base
        else:
            base_pay = self.list_of_pay.workshop.hade_aghal_hoghoogh
        padash = round(base_pay) * 60 * (self.real_worktime + self.illness_leave_day) / 365
        padash_limit = round(self.list_of_pay.workshop.hade_aghal_hoghoogh) * 90 * (
                self.real_worktime + self.illness_leave_day) / 365

        if padash > padash_limit:
            return padash_limit
        else:
            return padash

    @property
    def get_padash(self):
        if self.list_of_pay.workshop.eydi_padash_identification == 'm':
            padash = self.calculate_monthly_eydi
        elif self.list_of_pay.workshop.eydi_padash_identification == 'y' and self.list_of_pay.month == 12:
            padash = self.calculate_yearly_eydi
        else:
            padash = 0
        return padash

    '''report'''

    @property
    def bank_report(self):
        response = {}
        response['name'] = self.workshop_personnel.personnel.full_name
        response['previous'] = self.get_unpaid_of_year
        response['payable'] = self.payable
        response['unpaid'] = self.unpaid
        response['total'] = self.total_unpaid
        response['paid'] = self.paid_amount
        response['card'] = self.workshop_personnel.personnel.bank_cart_number
        response['account'] = self.workshop_personnel.personnel.account_bank_number
        response['sheba'] = self.workshop_personnel.personnel.sheba_number
        return response

    @property
    def bank_report_with_comma(self):
        response = {}
        response['name'] = self.workshop_personnel.personnel.full_name
        response['previous'] = self.with_comma(self.get_unpaid_of_year, True)
        response['payable'] = self.with_comma(self.payable, True)
        response['unpaid'] = self.with_comma(self.unpaid, True)
        response['total'] = self.with_comma(self.total_unpaid, True)
        response['paid'] = self.with_comma(self.paid_amount, True)
        response['card'] = self.workshop_personnel.personnel.bank_cart_number
        response['account'] = self.workshop_personnel.personnel.account_bank_number
        response['sheba'] = self.workshop_personnel.personnel.sheba_number
        response['previous_amount'] = self.get_unpaid_of_year
        response['payable_amount'] = self.payable
        response['unpaid_amount'] = self.unpaid
        response['total_amount'] = self.total_unpaid
        response['paid_amount'] = self.paid_amount

        return response

    @property
    def check_and_get_loan_episode(self):
        personnel_loans = Loan.objects.filter(Q(workshop_personnel=self.workshop_personnel) &
                                              Q(pay_date__lte=self.list_of_pay.end_date) &
                                              Q(is_verified=True) &
                                              Q(pay_done=False) &
                                              Q(loan_type='l'))
        month_episode = 0
        for loan in personnel_loans:
            for episode in loan.item.all():
                if episode.date.__ge__(self.list_of_pay.start_date) and episode.date.__le__(self.list_of_pay.end_date):
                    if episode.is_last:
                        month_episode += episode.cumulative_balance
                        episode.payed_amount = episode.cumulative_balance
                        episode.save()
                    else:
                        month_episode += loan.get_pay_episode
                        episode.payed_amount = episode.amount
                        episode.save()

        return round(month_episode)

    @property
    def check_and_get_dept_episode(self):
        month_episode = 0
        personnel_loans = Loan.objects.filter(Q(workshop_personnel=self.workshop_personnel) &
                                              Q(pay_date__lte=self.list_of_pay.end_date) &
                                              Q(is_verified=True) &
                                              Q(pay_done=False) &
                                              Q(loan_type='d'))
        month_episode = 0
        for loan in personnel_loans:
            for episode_date in loan.get_pay_month['months']:
                if episode_date.__ge__(self.list_of_pay.start_date) and episode_date.__le__(self.list_of_pay.end_date):
                    month_episode += loan.get_pay_episode
                    items = loan.item.all()
                    for item in items:
                        if item.date.month == self.list_of_pay.month:
                            item.payed_amount = item.amount
                            item.save()
        return round(month_episode)

    @property
    def check_and_get_optional_deduction_episode(self):
        month_episode = 0
        personnel_deductions = OptionalDeduction.objects.filter(Q(workshop_personnel=self.workshop_personnel) &
                                                                Q(is_verified=True) &
                                                                Q(is_active=True) &
                                                                Q(start_date__lte=self.list_of_pay.end_date) &
                                                                Q(pay_done=False))
        for deduction in personnel_deductions:
            for episode_date in deduction.get_pay_month['months']:
                if episode_date.__ge__(self.list_of_pay.start_date) and episode_date.__le__(self.list_of_pay.end_date):
                    month_episode += deduction.get_pay_episode

        return round(month_episode)

    @property
    def get_payslip(self):
        hr = self.get_hr_letter
        payslip = {}
        deduction = {}
        additions = {}
        additions['hagh_maskan'] = self.with_comma(self.calculate_hr_item_in_real_work_time(hr.haghe_maskan_amount))
        additions['kharo_bar'] = self.with_comma(self.calculate_hr_item_in_real_work_time(hr.bon_kharo_bar_amount))

        additions['hagh_sarparasti'] = self.with_comma(
            self.calculate_hr_item_in_real_work_time(hr.haghe_sarparasti_amount))
        additions['hagh_modiriat'] = self.with_comma(
            self.calculate_hr_item_in_real_work_time(hr.haghe_modiriyat_amount))
        additions['hagh_jazb'] = self.with_comma(self.calculate_hr_item_in_real_work_time(hr.haghe_jazb_amount))
        additions['fogholade_shoghl'] = self.with_comma(
            self.calculate_hr_item_in_real_work_time(hr.fogholade_shoghl_amount))
        additions['haghe_tahsilat'] = self.with_comma(
            self.calculate_hr_item_in_real_work_time(hr.haghe_tahsilat_amount))
        additions['fogholade_sakhti_kar'] = \
            self.with_comma(self.calculate_hr_item_in_real_work_time(hr.fogholade_sakhti_kar_amount))
        additions['haghe_ankal'] = self.with_comma(self.calculate_hr_item_in_real_work_time(hr.haghe_ankal_amount))
        additions['fogholade_badi_abohava'] = \
            self.with_comma(self.calculate_hr_item_in_real_work_time(hr.fogholade_badi_abohava_amount))
        additions['mahroomiat_tashilat_zendegi'] = \
            self.with_comma(self.calculate_hr_item_in_real_work_time(hr.mahroomiat_tashilat_zendegi_amount))
        additions['fogholade_mahal_khedmat'] = \
            self.with_comma(self.calculate_hr_item_in_real_work_time(hr.fogholade_mahal_khedmat_amount))
        additions['fogholade_sharayet_mohit_kar'] = \
            self.with_comma(self.calculate_hr_item_in_real_work_time(hr.fogholade_sharayet_mohit_kar_amount))
        additions['ayabo_zahab'] = self.with_comma(self.calculate_hr_item_in_real_work_time(hr.ayabo_zahab_amount))
        additions['yarane_ghaza'] = self.with_comma(self.calculate_hr_item_in_real_work_time(hr.yarane_ghaza_amount))
        additions['haghe_shir'] = self.with_comma(self.calculate_hr_item_in_real_work_time(hr.haghe_shir_amount))
        additions['haghe_taahol'] = self.with_comma(self.calculate_hr_item_in_real_work_time(hr.haghe_taahol_amount))
        additions['komakhazine_mahdekoodak'] = \
            self.with_comma(self.calculate_hr_item_in_real_work_time(hr.komakhazine_mahdekoodak_amount))
        additions['komakhazine_varzesh'] = self.with_comma(
            self.calculate_hr_item_in_real_work_time(hr.komakhazine_varzesh_amount))
        additions['komakhazine_mobile'] = self.with_comma(
            self.calculate_hr_item_in_real_work_time(hr.komakhazine_mobile_amount))
        additions['mazaya_mostamar_gheyre_naghdi'] = \
            self.with_comma(self.calculate_hr_item_in_real_work_time(hr.mazaya_mostamar_gheyre_naghdi_amount))

        payslip['additions'] = additions
        payslip['deduction'] = deduction
        return payslip

    '''insurance'''

    @property
    def get_insurance_total_payment(self):
        self.hr_letter = self.get_hr_letter
        total = Decimal(0)
        is_insurance, insurance_worktime = self.check_insurance
        if is_insurance:
            total += self.hoghoogh_roozane * insurance_worktime
            total += self.sanavat_base * insurance_worktime
            total += self.mission_total

            total += self.aele_mandi_in_insurance
            total += self.get_ezafe_kari
            total += self.get_tatil_kari
            total += self.get_shab_kari
            total += self.nobat_kari_sob_asr_total
            total += self.nobat_kari_sob_shab_total
            total += self.nobat_kari_asr_shab_total
            total += self.nobat_kari_sob_asr_shab_total

            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.haghe_sarparasti_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.haghe_modiriyat_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.haghe_jazb_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.fogholade_shoghl_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.haghe_tahsilat_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.fogholade_sakhti_kar_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.haghe_ankal_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.fogholade_badi_abohava_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.mahroomiat_tashilat_zendegi_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.fogholade_mahal_khedmat_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.fogholade_sharayet_mohit_kar_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.haghe_maskan_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.ayabo_zahab_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.bon_kharo_bar_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.yarane_ghaza_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.haghe_taahol_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.haghe_shir_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.komakhazine_mahdekoodak_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.komakhazine_varzesh_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.komakhazine_mobile_amount)
            total += self.calculate_hr_item_in_insurance_time(self.hr_letter.mazaya_mostamar_gheyre_naghdi_amount)

            total += self.mazaya_gheyr_mostamar

            total += self.sayer_ezafat

            total += Decimal(self.padash_total)

            total += Decimal(self.haghe_sanavat_total)

            total += Decimal(self.saved_leaves_total)

            return total
        else:
            return 0

    @property
    def check_insurance(self):
        if self.contract.insurance and self.list_of_pay.use_in_calculate:
            insurance_start = self.contract.insurance_add_date
            if insurance_start.__le__(self.list_of_pay.start_date):
                return True, self.real_worktime
            elif insurance_start.__gt__(self.list_of_pay.start_date) and \
                    insurance_start.__lt__(self.list_of_pay.end_date):
                insurance_day = self.list_of_pay.end_date.day - insurance_start.day + 1
                absences = self.absence_not_included(insurance_start)
                insurance_day = insurance_day - absences - int(self.cumulative_absence) - \
                                int(self.cumulative_illness) - int(self.cumulative_without_salary)
                return True, insurance_day
            elif insurance_start.__ge__(self.list_of_pay.end_date):
                return False, 0
        else:
            return False, 0

    def absence_not_included(self, start_date):
        end_date = self.list_of_pay.end_date
        leaves = self.workshop_personnel.leave.filter(
            Q(is_verified=True) &
            Q(leave_type__in=['i', 'w', 'a'])
        )
        leave_count = 0
        for leave in leaves:
            if leave.from_date.__ge__(start_date) and leave.to_date.__le__(end_date):
                leave_count += leave.final_by_day
            elif leave.from_date.__le__(start_date) and leave.to_date.__ge__(end_date):
                duration = end_date.day - start_date.day
                leave_count += duration
            elif leave.from_date.__le__(start_date) and leave.to_date.__ge__(start_date) and \
                    leave.to_date.__le__(end_date):
                duration = leave.to_date.day - start_date.day + 1
                leave_count += duration
            elif leave.from_date.__ge__(start_date) and leave.from_date.__le__(end_date) and \
                    leave.to_date.__ge__(end_date):
                duration = end_date.day - leave.from_date.day + 1
                leave_count += duration

        return leave_count

    @property
    def haghe_bime_bime_shavande(self):
        is_insurance, insurance_worktime = self.check_insurance
        if is_insurance:
            hr = self.get_hr_letter
            return round(self.insurance_total_included * hr.worker_insurance_nerkh)
        else:
            return 0

    @property
    def employer_insurance(self):
        is_insurance, insurance_worktime = self.check_insurance
        if is_insurance:
            hr = self.get_hr_letter
            return round(self.insurance_total_included * hr.employer_insurance_nerkh)
        else:
            return 0

    @property
    def un_employer_insurance(self):
        is_insurance, insurance_worktime = self.check_insurance
        if is_insurance:
            hr = self.get_hr_letter
            return round(self.insurance_total_included * hr.unemployed_insurance_nerkh)
        else:
            return 0

    @property
    def insurance_monthly_benefit(self):
        is_insurance, insurance_worktime = self.check_insurance
        if is_insurance:
            hr = self.get_hr_letter
            benefit = 0
            hr_letter_items = hr.get_hr_items

            if hr.hoghooghe_roozane_nature != 'b' and hr.hoghooghe_roozane_use_insurance:
                benefit += self.hoghoogh_mahane
            if hr.paye_sanavat_nature != 'b' and hr.paye_sanavat_use_insurance:
                benefit += self.sanavat_mahane

            for i in range(0, 23):
                if hr_letter_items[i]['insurance'] and hr_letter_items[i]['nature'] != 'b':
                    if i < 2:
                        benefit += 0
                    else:
                        benefit += self.calculate_hr_item_in_insurance_time(hr_letter_items[i]['amount'])
            if hr.mazaya_mostamar_gheyre_naghdi_use_insurance:
                benefit = benefit + Decimal(self.mazaya_gheyr_mostamar)
            if hr.ezafe_kari_use_insurance:
                benefit = benefit + Decimal(self.ezafe_kari_total)
            if hr.haghe_owlad_use_insurance:
                benefit = benefit + Decimal(self.aele_mandi_in_insurance)
            if hr.shab_kari_use_insurance:
                benefit = benefit + Decimal(self.shab_kari_total)
            if hr.tatil_kari_use_insurance:
                benefit = benefit + Decimal(self.tatil_kari_total)
            if hr.nobat_kari_use_insurance:
                benefit = benefit + self.nobat_kari_sob_shab_total
                benefit = benefit + self.nobat_kari_sob_asr_total
                benefit = benefit + self.nobat_kari_asr_shab_total
                benefit = benefit + self.nobat_kari_sob_asr_shab_total
            if hr.haghe_maamooriat_use_insurance:
                benefit = benefit + Decimal(self.mission_total)
            if hr.haghe_sanavat_use_insurance:
                benefit = benefit + Decimal(self.haghe_sanavat_total)
            if hr.eydi_padash_use_insurance:
                benefit = benefit + Decimal(self.padash_total)

            if self.sayer_ezafat:
                benefit += self.sayer_ezafat

            return benefit
        else:
            return 0

    @property
    def insurance_daily_payment(self):
        is_insurance, insurance_worktime = self.check_insurance
        if is_insurance:
            hr = self.get_hr_letter
            return hr.insurance_pay_day
        else:
            return 0

    @property
    def insurance_monthly_payment(self):
        is_insurance, insurance_worktime = self.check_insurance
        if is_insurance:
            hr = self.get_hr_letter
            return hr.insurance_pay_day * insurance_worktime
        else:
            return 0

    @property
    def absence_and_days(self):
        return self.absence_day + self.illness_leave_day + self.without_salary_leave_day

    @property
    def insurance_worktime(self):
        is_insurance, insurance_worktime = self.check_insurance
        if is_insurance:
            return insurance_worktime
        else:
            return 0

    @property
    def is_month_insurance(self):
        is_insurance, insurance_worktime = self.check_insurance
        return is_insurance

    @property
    def is_month_tax(self):
        is_tax, tax_worktime = self.check_tax
        return is_tax

    @property
    def insurance_included_limit(self):
        return self.workshop_personnel.workshop.hade_aghal_hoghoogh * 7 * self.list_of_pay.month_days

    @property
    def insurance_total_included(self):
        is_insurance, insurance_worktime = self.check_insurance
        if is_insurance:
            total = self.insurance_monthly_benefit + self.insurance_monthly_payment
            if total <= self.insurance_included_limit:
                return total
            else:
                return round(self.insurance_included_limit)
        else:
            return 0

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
            'DSW_ID': str(self.workshop_personnel.workshop.workshop_code),
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
            'DSW_OCP': self.workshop_personnel.title.name,
            'DSW_SDATE': contract.insurance_add_date.__str__().replace('-', ''),
            'DSW_EDATE': quit_job_date,
            'DSW_DD': self.insurance_worktime,
            'DSW_ROOZ': round(self.insurance_daily_payment),
            'DSW_MAH': round(self.insurance_monthly_payment),
            'DSW_MAZ': round(self.insurance_monthly_benefit),
            'DSW_MASH': round(self.insurance_total_included),
            'DSW_TOTL': round(self.total_payment),
            'DSW_BIME': round(self.haghe_bime_bime_shavande),
            'DSW_PRATE': 0,
            'DSW_JOB': self.workshop_personnel.title.code,
            'PER_NATCOD': str(self.workshop_personnel.personnel.national_code),

        }
        return DSKWOR

    '''tax'''

    @property
    def check_tax(self):
        if self.contract.tax and self.list_of_pay.use_in_calculate:
            tax_start = self.contract.tax_add_date
            if tax_start.__le__(self.list_of_pay.start_date):
                return True, self.real_worktime
            elif tax_start.__gt__(self.list_of_pay.start_date) and \
                    tax_start.__lt__(self.list_of_pay.end_date):
                tax_day = self.list_of_pay.end_date.day - tax_start.day + 1
                absences = self.absence_not_included(tax_start)
                tax_day = tax_day - absences - int(self.cumulative_absence) - \
                          int(self.cumulative_illness) - int(self.cumulative_without_salary)
                return True, tax_day
            elif tax_start.__ge__(self.list_of_pay.end_date):
                return False, 0
        else:
            return False, 0

    @property
    def tax_naghdi_un_pension(self):
        hr = self.get_hr_letter
        total = Decimal(0)

        total += self.mission_total
        total += self.shab_kari_total
        total += self.nobat_kari_sob_asr_total
        total += self.nobat_kari_sob_shab_total
        total += self.nobat_kari_asr_shab_total
        total += self.nobat_kari_sob_asr_shab_total

        if hr.haghe_sarparasti_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_sarparasti_amount)
        if hr.haghe_modiriyat_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_modiriyat_amount)
        if hr.haghe_jazb_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_jazb_amount)
        if hr.fogholade_shoghl_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.fogholade_shoghl_amount)
        if hr.haghe_tahsilat_nature == 'u':
            total += Decimal(self.calculate_hr_item_in_tax_time(hr.haghe_tahsilat_amount))
        if hr.fogholade_sakhti_kar_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.fogholade_sakhti_kar_amount)
        if hr.haghe_ankal_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_ankal_amount)
        if hr.fogholade_badi_abohava_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.fogholade_badi_abohava_amount)
        if hr.mahroomiat_tashilat_zendegi_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.mahroomiat_tashilat_zendegi_amount)
        if hr.fogholade_mahal_khedmat_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.fogholade_mahal_khedmat_amount)
        if hr.fogholade_sharayet_mohit_kar_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.fogholade_sharayet_mohit_kar_amount)
        if hr.haghe_maskan_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_maskan_amount)
        if hr.ayabo_zahab_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.ayabo_zahab_amount)
        if hr.bon_kharo_bar_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.bon_kharo_bar_amount)
        if hr.yarane_ghaza_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.yarane_ghaza_amount)
        if hr.haghe_shir_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_shir_amount)
        if hr.haghe_taahol_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_taahol_amount)
        if hr.komakhazine_mahdekoodak_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.komakhazine_mahdekoodak_amount)
        if hr.komakhazine_varzesh_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.komakhazine_varzesh_amount)
        if hr.komakhazine_mobile_nature == 'u':
            total += self.calculate_hr_item_in_tax_time(hr.komakhazine_mobile_amount)

        total += Decimal(self.sayer_ezafat)

        return total

    @property
    def naghdi_un_pension_whit_comma(self):
        return self.with_comma(self.tax_naghdi_un_pension)

    @property
    def tax_naghdi_pension(self):
        is_tax, tax_day = self.check_tax
        total = 0
        total += (self.hoghoogh_roozane * tax_day)

        if self.sanavat_month >= 12:
            total += (self.sanavat_base * tax_day)

        total += self.aele_mandi_in_tax

        hr = self.get_hr_letter
        if hr.haghe_sarparasti_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_sarparasti_amount)
        if hr.haghe_modiriyat_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_modiriyat_amount)
        if hr.haghe_jazb_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_jazb_amount)
        if hr.fogholade_shoghl_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.fogholade_shoghl_amount)
        if hr.haghe_tahsilat_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_tahsilat_amount)
        if hr.fogholade_sakhti_kar_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.fogholade_sakhti_kar_amount)
        if hr.haghe_ankal_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_ankal_amount)
        if hr.fogholade_badi_abohava_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.fogholade_badi_abohava_amount)
        if hr.mahroomiat_tashilat_zendegi_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.mahroomiat_tashilat_zendegi_amount)
        if hr.fogholade_mahal_khedmat_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.fogholade_mahal_khedmat_amount)
        if hr.fogholade_sharayet_mohit_kar_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.fogholade_sharayet_mohit_kar_amount)
        if hr.haghe_maskan_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_maskan_amount)
        if hr.ayabo_zahab_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.ayabo_zahab_amount)
        if hr.bon_kharo_bar_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.bon_kharo_bar_amount)
        if hr.yarane_ghaza_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.yarane_ghaza_amount)
        if hr.haghe_taahol_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_taahol_amount)
        if hr.haghe_shir_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.haghe_shir_amount)
        if hr.komakhazine_mahdekoodak_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.komakhazine_mahdekoodak_amount)
        if hr.komakhazine_varzesh_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.komakhazine_varzesh_amount)
        if hr.komakhazine_mobile_nature == 'p':
            total += self.calculate_hr_item_in_tax_time(hr.komakhazine_mobile_amount)
        return total

    @property
    def naghdi_pension_with_comma(self):
        return self.with_comma(self.tax_naghdi_pension)

    @property
    def tamin_ejtemaee_moafiat(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            return round(Decimal(self.haghe_bime_bime_shavande) * Decimal(self.taamin_ejtemaee))
        else:
            return 0

    @property
    def haghe_bime_moafiat(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            return self.tamin_ejtemaee_moafiat + self.kosoorat_insurance
        else:
            return 0

    @property
    def haghe_bime_moafiat_with_comma(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            return self.with_comma(self.haghe_bime_moafiat)
        else:
            return 0

    @property
    def ezafe_kari_nakhales(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            return self.ezafe_kari_total + self.tatil_kari_total
        else:
            return 0

    @property
    def ezafe_kari_nakhales_with_comma(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            return self.with_comma(self.ezafe_kari_nakhales)
        else:
            return 0

    @property
    def hr_tax_not_included(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            hr = self.get_hr_letter
            total = Decimal(0)
            if not hr.hoghooghe_roozane_use_tax:
                total += (self.hoghoogh_roozane * tax_day)
            if not hr.paye_sanavat_use_tax:
                total += (self.sanavat_base * tax_day)
            if not hr.haghe_owlad_use_tax:
                total += self.aele_mandi_in_tax
            if not hr.ezafe_kari_use_tax:
                total += self.get_ezafe_kari
            if not hr.tatil_kari_use_tax:
                total += self.get_tatil_kari
            if not hr.shab_kari_use_tax:
                total += self.get_shab_kari
            if not hr.nobat_kari_use_tax:
                total += self.nobat_kari_sob_asr_total
                total += self.nobat_kari_sob_shab_total
                total += self.nobat_kari_asr_shab_total
                total += self.nobat_kari_sob_asr_shab_total
            if not hr.haghe_sarparasti_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.haghe_sarparasti_amount)
            if not hr.haghe_modiriyat_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.haghe_modiriyat_amount)
            if not hr.haghe_jazb_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.haghe_jazb_amount)
            if not hr.fogholade_shoghl_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.fogholade_shoghl_amount)
            if not hr.haghe_tahsilat_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.haghe_tahsilat_amount)
            if not hr.fogholade_sakhti_kar_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.fogholade_sakhti_kar_amount)
            if not hr.haghe_ankal_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.haghe_ankal_amount)
            if not hr.fogholade_badi_abohava_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.fogholade_badi_abohava_amount)
            if not hr.mahroomiat_tashilat_zendegi_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.mahroomiat_tashilat_zendegi_amount)
            if not hr.fogholade_mahal_khedmat_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.fogholade_mahal_khedmat_amount)
            if not hr.fogholade_sharayet_mohit_kar_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.fogholade_sharayet_mohit_kar_amount)
            if not hr.haghe_maskan_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.haghe_maskan_amount)
            if not hr.ayabo_zahab_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.ayabo_zahab_amount)
            if not hr.bon_kharo_bar_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.bon_kharo_bar_amount)
            if not hr.yarane_ghaza_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.yarane_ghaza_amount)
            if not hr.haghe_taahol_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.haghe_taahol_amount)
            if not hr.haghe_shir_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.haghe_shir_amount)
            if not hr.komakhazine_mahdekoodak_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.komakhazine_mahdekoodak_amount)
            if not hr.komakhazine_varzesh_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.komakhazine_varzesh_amount)
            if not hr.komakhazine_mobile_use_tax:
                total += self.calculate_hr_item_in_tax_time(hr.komakhazine_mobile_amount)

            return total
        else:
            return self.total_payment

    @property
    def total_sayer_moafiat(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            total = 0
            total += self.sayer_moafiat
            if self.list_of_pay.workshop.eydi_padash_identification == 'm':
                total += self.calculate_monthly_eydi_moafiat
            elif self.list_of_pay.workshop.eydi_padash_identification == 'y' and self.list_of_pay.month == 12:
                total += self.calculate_yearly_eydi_moafiat
            total += self.hr_tax_not_included

            return total
        else:
            return 0

    @property
    def moaf_sum(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            total = 0
            total += self.hazine_made_137
            total += self.total_sayer_moafiat
            total += Decimal(self.get_hagh_sanavat_and_save_leaves)
            total += Decimal(self.haghe_bime_moafiat)
            total += self.manategh_tejari_moafiat
            total += self.ejtenab_maliat_mozaaf

            return round(total)
        else:
            return 0

    @property
    def gheyre_naghdi_moafiat(self):
        is_tax, tax_day = self.check_tax
        total_gheyre_naghdi = self.mazaya_gheyr_mostamar + self.gheyre_naghdi_tax_pension
        mytax = self.get_tax_row
        tax_rows = mytax.tax_row.all()
        tax_row = tax_rows.get(from_amount=Decimal(0))
        tax_moaf = tax_row.to_amount / 6 / 12 * tax_day / self.list_of_pay.month_days
        if tax_moaf >= total_gheyre_naghdi:
            return total_gheyre_naghdi
        elif tax_moaf < total_gheyre_naghdi:
            return tax_moaf

    @property
    def moafiat_sum(self):
        return self.moaf_sum + self.gheyre_naghdi_moafiat

    @property
    def tax_included_payment(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            total_naghdi = self.tax_naghdi_un_pension + self.tax_naghdi_pension + self.ezafe_kari_nakhales + \
                           self.padash_total + self.get_hagh_sanavat_and_save_leaves

            included_naghdi = total_naghdi - self.moaf_sum
            total_gheyre_naghdi = self.mazaya_gheyr_mostamar + self.gheyre_naghdi_tax_pension
            included_gheyre_naghdi = total_gheyre_naghdi - self.gheyre_naghdi_moafiat
            return included_naghdi + included_gheyre_naghdi
        else:
            return 0

    @property
    def get_year_payment(self):
        items = ListOfPayItem.objects.filter(Q(list_of_pay__year=self.list_of_pay.year) &
                                             Q(list_of_pay__month__lte=self.list_of_pay.month) &
                                             Q(workshop_personnel=self.workshop_personnel) &
                                             Q(list_of_pay__ultimate=True) &
                                             Q(list_of_pay__use_in_calculate=True))
        year_payment = Decimal(0)
        for item in items:
            year_payment = year_payment + Decimal(item.tax_included_payment)
        return year_payment

    @property
    def get_last_tax(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            items = ListOfPayItem.objects.filter(Q(list_of_pay__year=self.list_of_pay.year) &
                                                 Q(list_of_pay__month__lte=self.list_of_pay.month) &
                                                 Q(workshop_personnel=self.workshop_personnel) &
                                                 Q(list_of_pay__ultimate=True) &
                                                 Q(list_of_pay__use_in_calculate=True))
            tax = Decimal(0)
            for item in items:
                tax += item.total_tax
            return tax
        else:
            return 0

    @property
    def get_tax_row(self):
        company_id = self.workshop_personnel.workshop.company.id
        date = self.list_of_pay.end_date
        taxs = WorkshopTax.objects.filter(company_id=company_id)
        if len(taxs) == 0:
            raise ValidationError('در این شرکت جدول معافیت مالیات ثبت نشده')
        month_tax = None
        for tax in taxs:
            if tax.from_date.__le__(date) and tax.to_date.__ge__(date):
                month_tax = tax
        if month_tax:
            return month_tax
        else:
            raise ValidationError('جدول معافیت مالیات در این تاریخ موجود نیست')

    @property
    def calculate_month_tax(self):
        hr = self.get_hr_letter
        if hr.include_made_86:
            tax = self.tax_included_payment / 10
        else:
            items = ListOfPayItem.objects.filter(Q(list_of_pay__year=self.list_of_pay.year) &
                                                 Q(list_of_pay__month__lte=self.list_of_pay.month) &
                                                 Q(workshop_personnel=self.workshop_personnel) &
                                                 Q(list_of_pay__ultimate=True) &
                                                 Q(list_of_pay__use_in_calculate=True))
            month_is_tax, month_tax_day = self.check_tax
            tax_worktime = month_tax_day / self.list_of_pay.month_days

            for item in items:
                is_tax, tax_day = item.check_tax
                if is_tax:
                    tax_worktime += (tax_day / item.list_of_pay.month_days)
            month_count = Decimal(tax_worktime / 12)
            tax = 0
            year_amount = Decimal(self.get_year_payment) + Decimal(self.tax_included_payment)
            mytax = self.get_tax_row
            tax_rows = mytax.tax_row.all()
            tax_row = tax_rows.get(from_amount=Decimal(0))
            start = year_amount

            while start > Decimal(0):
                from_amount = tax_row.from_amount * month_count
                if tax_row.from_amount == 0:
                    from_amount = 0

                if year_amount <= (tax_row.to_amount * month_count):
                    tax += round(round(year_amount - from_amount) * tax_row.ratio / 100)
                    start = 0
                    return round(tax) - round(self.get_last_tax)

                elif year_amount > (tax_row.to_amount * month_count):
                    if tax_row.is_last:
                        print('is last')
                        part_tax = (year_amount - from_amount) * tax_row.ratio / 100
                        tax += round(part_tax)
                        start = 0
                    else:
                        part_tax = ((tax_row.to_amount * month_count) - from_amount) \
                                   * tax_row.ratio / 100
                        if from_amount == 0:
                            part_tax = 0
                        tax += round(part_tax)
                        start -= ((tax_row.to_amount * month_count) - from_amount)

                        next_from_amount = tax_row.to_amount + Decimal(1)
                        tax_row = tax_rows.get(from_amount=next_from_amount)
        final_tax = round(tax) - round(self.get_last_tax)
        return final_tax if final_tax >= 0 else 0

    @property
    def calculate_yearly_eydi_tax(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            hr = self.get_hr_letter
            if hr.eydi_padash_use_tax:
                year_worktime = 0
                items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                                     & Q(list_of_pay__year=self.list_of_pay.year)
                                                     & Q(list_of_pay__ultimate=True)
                                                     & Q(list_of_pay__use_in_calculate=True))
                for item in items:
                    tax, day = item.check_tax
                    year_worktime += day
                mytax = self.get_tax_row
                tax_rows = mytax.tax_row.all()
                tax_row = tax_rows.get(from_amount=Decimal(0))
                moafiat_limit = tax_row.to_amount / 12 * year_worktime / 365
                eydi = self.padash_total
                moaf = round(moafiat_limit) - round(eydi)
                if moaf <= 0:
                    eydi_tax = -moaf
                else:
                    eydi_tax = 0

                return eydi_tax
            else:
                return 0
        else:
            return 0

    @property
    def calculate_yearly_eydi_moafiat(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            year_worktime = 0
            items = ListOfPayItem.objects.filter(Q(workshop_personnel=self.workshop_personnel)
                                                 & Q(list_of_pay__year=self.list_of_pay.year)
                                                 & Q(list_of_pay__ultimate=True)
                                                 & Q(list_of_pay__use_in_calculate=True))
            for item in items:
                tax, day = item.check_tax
                year_worktime += day

            mytax = self.get_tax_row
            tax_rows = mytax.tax_row.all()
            tax_row = tax_rows.get(from_amount=Decimal(0))
            moafiat_limit = tax_row.to_amount / 12 * year_worktime / 365
            eydi = self.padash_total
            moaf = round(eydi) - round(moafiat_limit)
            if moaf <= 0:
                return round(eydi)
            else:
                return round(moafiat_limit)
        else:
            return 0

    @property
    def calculate_monthly_eydi_tax(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            hr = self.get_hr_letter
            if hr.eydi_padash_use_tax:
                mytax = self.get_tax_row
                tax_rows = mytax.tax_row.all()
                tax_row = tax_rows.get(from_amount=Decimal(0))
                moafiat_limit = tax_row.to_amount / 12 / 12 / self.list_of_pay.month_days * tax_day
                eydi = self.padash_total
                moaf = moafiat_limit - Decimal(eydi)
                if moaf <= 0:
                    eydi_tax = -moaf
                else:
                    eydi_tax = 0

                return eydi_tax
            else:
                return 0
        else:
            return 0

    @property
    def calculate_monthly_eydi_moafiat(self):
        is_tax, tax_day = self.check_tax
        if is_tax:
            mytax = self.get_tax_row
            tax_rows = mytax.tax_row.all()
            tax_row = tax_rows.get(from_amount=Decimal(0))
            moafiat_limit = tax_row.to_amount / 12 / 12 / self.list_of_pay.month_days * tax_day
            eydi = self.padash_total
            moaf = round(eydi) - round(moafiat_limit)
            if moaf <= 0:
                return round(eydi)
            else:
                return round(moafiat_limit)
            return eydi_tax
        else:
            return 0

    def save(self, *args, **kwargs):
        if not self.id:
            self.sanavat_base, self.sanavat_month = self.get_sanavt_info
            self.set_info_from_workshop()
            self.aele_mandi_child = self.get_aele_mandi_info
        if self.calculate_payment:
            self.set_info_from_workshop()
            self.aele_mandi_child = self.get_aele_mandi_info
            self.real_worktime = self.normal_worktime - self.absence_sum - self.without_salary_sum - self.illness_sum
            self.hr_letter = self.get_hr_letter
            self.total_payment = round(self.get_total_payment)
            if self.contract_row:
                self.contract_row.use_in_insurance_list = True

            self.total_tax = self.calculate_month_tax

        self.calculate_payment = False
        super().save(*args, **kwargs)
