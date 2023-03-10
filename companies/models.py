from django.contrib.postgres.fields import ArrayField
from django_jalali.db import models as jmodels
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework.exceptions import ValidationError

from helpers.bale import Bale
from helpers.functions import date_to_str
from helpers.models import BaseModel, POSTAL_CODE, EXPLANATION, BaseManager, upload_to


class Company(BaseModel):
    name = models.CharField(max_length=150)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    sabt_number = models.CharField(max_length=20, blank=True, null=True)
    phone1 = models.CharField(max_length=20, blank=True, null=True)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    postal_code = POSTAL_CODE(blank=True, null=True)
    eghtesadi_code = models.CharField(max_length=20, blank=True, null=True)
    shenase = models.CharField(max_length=20, blank=True, null=True)
    explanation = EXPLANATION()

    logo = models.FileField(upload_to=upload_to, null=True, blank=True, default=None)

    superuser = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='companies_as_superuser')

    users = models.ManyToManyField(
        'users.User',
        through='companies.CompanyUser',
        through_fields=('company', 'user'),
        related_name='companies'
    )

    modules = ArrayField(models.CharField(max_length=30), default=list, blank=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    @property
    def last_financial_year(self):
        try:
            return self.financial_years.order_by('-id')[0]
        except (ObjectDoesNotExist, IndexError):
            return None

    class Meta(BaseModel.Meta):
        permission_basename = 'company'
        permissions = (
            ('get.company', '???????????? ????????'),
            ('create.company', '?????????? ????????'),
            ('update.company', '???????????? ????????'),
            ('delete.company', '?????? ????????'),

            ('getOwn.company', '???????????? ???????? ?????? ??????'),
            ('updateOwn.company', '???????????? ???????? ?????? ??????'),
            ('deleteOwn.company', '?????? ???????? ?????? ??????'),
        )

    def delete(self, *args, **kwargs):
        if self.usersActiveCompany.all().count() != 0:
            raise ValidationError("?????? ???????? ???????? ???????? ???? ?????????????? ???????? ??????")
        return super().delete(*args, **kwargs)


class FinancialYear(BaseModel):
    ADVARI = 'a'
    DAEMI = 'd'

    WAREHOUSE_SYSTEMS = (
        (ADVARI, '????????????'),
        (DAEMI, '??????????')
    )

    name = models.CharField(max_length=150)
    start = jmodels.jDateField()
    end = jmodels.jDateField()
    warehouse_system = models.CharField(max_length=2, choices=WAREHOUSE_SYSTEMS)

    explanation = models.CharField(max_length=255, blank=True, verbose_name="??????????????")

    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='financial_years')
    openingSanad = models.ForeignKey('sanads.Sanad', on_delete=models.SET_NULL,
                                     related_name='financialYearAsOpeningSanad', null=True, blank=True)

    temporaryClosingSanad = models.ForeignKey('sanads.Sanad', on_delete=models.SET_NULL,
                                              related_name='financialYearAsTemporaryClosingSanad', null=True,
                                              blank=True)
    currentEarningsClosingSanad = models.ForeignKey('sanads.Sanad', on_delete=models.SET_NULL,
                                                    related_name='financialYearAsCurrentEarningsClosingSanad',
                                                    null=True, blank=True)
    permanentsClosingSanad = models.ForeignKey('sanads.Sanad', on_delete=models.SET_NULL,
                                               related_name='financialYearAsPermanentsClosingSanad', null=True,
                                               blank=True)

    # Advari Fields
    are_factors_sorted = models.BooleanField(default=True)

    def __str__(self):
        return "{} {} ({})".format(self.company, self.name, self.id)

    class Meta(BaseModel.Meta):
        unique_together = ('company', 'name')
        permission_basename = 'financialYear'
        ordering = ('-id',)
        permissions = (
            ('get.financialYear', '???????????? ?????? ????????'),
            ('create.financialYear', '?????????? ?????? ????????'),
            ('update.financialYear', '???????????? ?????? ????????'),
            ('delete.financialYear', '?????? ?????? ????????'),

            ('move.financialYear', '???????????? ?????? ????????'),
            ('close.financialYear', '???????? ?????? ????????'),
            ('cancelClosing.financialYear', '?????? ???????? ?????? ????????'),

            ('getOwn.financialYear', '???????????? ?????? ?????? ???????? ??????'),
            ('updateOwn.financialYear', '???????????? ?????? ?????? ???????? ??????'),
            ('deleteOwn.financialYear', '?????? ?????? ?????? ???????? ??????'),

            ('moveOwn.financialYear', '???????????? ?????? ?????? ???????? ??????'),
            ('closeOwn.financialYear', '???????? ?????? ?????? ???????? ??????'),
            ('cancelClosingOwn.financialYear', '?????? ???????? ?????? ?????? ???????? ??????'),
        )

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def is_closed(self):
        return self.temporaryClosingSanad is not None

    @property
    def is_advari(self):
        return self.warehouse_system == self.ADVARI

    def get_opening_sanad(self):
        from sanads.models import Sanad

        if not self.openingSanad:
            sanad, created = Sanad.objects.get_or_create(
                financial_year=self,
                code=1,
                defaults={
                    'date': self.start,
                }
            )

            is_sanad_ok = True
            if sanad.is_auto_created:
                if sanad.type != Sanad.OPENING:
                    is_sanad_ok = False
            elif sanad.items.all().count() != 0:
                is_sanad_ok = False

            if not is_sanad_ok:
                raise ValidationError('?????? ?????????? ???? ?????? ???????? ???????? ???? ???????? ????????')

            self.openingSanad = sanad
            self.save()
        else:
            sanad = self.openingSanad

        sanad.date = self.start
        sanad.is_auto_created = True
        sanad.type = Sanad.OPENING
        sanad.explanation = "?????? ????????????????"
        sanad.define()
        sanad.save()

        return sanad

    def check_closing_sanads(self):
        from sanads.models import Sanad
        from sanads.models import newSanadCode

        closing_sanads = [
            'temporaryClosingSanad',
            'currentEarningsClosingSanad',
            'permanentsClosingSanad'
        ]

        for sanad_name in closing_sanads:
            sanad = getattr(self, sanad_name)
            if not sanad:
                sanad = Sanad.objects.create(
                    financial_year=self,
                    code=newSanadCode(self),
                    date=self.end,
                    is_auto_created=True,
                    type=Sanad.CLOSING
                )
                setattr(self, sanad_name, sanad)

        self.save()

    def delete_closing_sanads(self):
        self.temporaryClosingSanad.delete()
        self.currentEarningsClosingSanad.delete()
        self.permanentsClosingSanad.delete()

    def check_date(self, date, raise_exception=True):
        is_valid = self.start <= date <= self.end
        if raise_exception:
            if not is_valid:
                raise ValidationError({
                    "non_field_errors": ["?????????? ???????? ???? ???????? ?????? ???????? ????????. ( ???? {} ???? {})".format(
                        date_to_str(self.start),
                        date_to_str(self.end),
                    )],
                    "date": date_to_str(date)
                })
        return is_valid


class CompanyUser(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companyUsers')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='companyUsers')

    financialYears = models.ManyToManyField(FinancialYear, related_name='companyUsers')

    roles = models.ManyToManyField('users.Role', related_name='companyUsers', blank=True)

    class Meta(BaseModel.Meta):
        unique_together = (('company', 'user'),)
        permission_basename = 'user'

    def __str__(self):
        return "{} {} ({})".format(self.company.name, self.user.username, self.id)


class CompanyUserInvitation(BaseModel):
    PENDING = 'p'
    ACCEPTED = 'a'
    REJECTED = 'r'

    STATUSES = (
        (PENDING, '???? ???????????? ??????????'),
        (ACCEPTED, '?????????? ??????'),
        (REJECTED, '???? ??????')
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companyUserInvitations')

    username = models.CharField(max_length=150)

    financialYears = models.ManyToManyField(FinancialYear, related_name='companyUserInvitations')

    roles = models.ManyToManyField('users.Role', related_name='companyUserInvitations', blank=True)

    confirmation_code = models.CharField(max_length=20)

    status = models.CharField(max_length=1, choices=STATUSES, default=PENDING)

    class Meta(BaseModel.Meta):
        permission_basename = 'user'

    def __str__(self):
        return "{} {} ({})".format(self.company.name, self.username, self.id)


class FinancialYearOperation(BaseModel):
    MOVE = 'm'
    CLOSE = 'c'
    CLOSE_AND_MOVE = 'cm'
    CANCEL_CLOSE = 'cc'

    OPERATIONS = (
        (MOVE, '????????????'),
        (CLOSE, '????????'),
        (CLOSE_AND_MOVE, '???????? ?? ????????????'),
        (CANCEL_CLOSE, '?????? ????????')
    )

    fromFinancialYear = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='operations')
    toFinancialYear = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, blank=True, null=True)

    operation = models.CharField(max_length=2, choices=OPERATIONS)
