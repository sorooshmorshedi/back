from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_jalali.db import models as jmodels
from accounts.accounts.models import Account, FloatAccount, FloatAccountGroup, FloatAccountRelation
from accounts.defaultAccounts.models import DefaultAccount
from wares.models import Ware, Warehouse, WareLevel, Unit


class Company(models.Model):
    name = models.CharField(unique=True, max_length=150)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    sabt_number = models.CharField(max_length=20, blank=True, null=True)
    phone1 = models.CharField(max_length=20, blank=True, null=True)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    eghtesadi_code = models.CharField(max_length=20, blank=True, null=True)
    shenase = models.CharField(max_length=20, blank=True, null=True)

    permissions = (
        ('get_company', 'Can get company')
    )

    @property
    def last_financial_year(self):
        try:
            return self.financial_years.order_by('-id')[0]
        except (ObjectDoesNotExist, IndexError):
            return None


class FinancialYear(models.Model):
    objects = models.Manager()

    name = models.CharField(unique=True, max_length=150)
    start = jmodels.jDateField()
    end = jmodels.jDateField()
    explanation = models.CharField(max_length=255, blank=True, verbose_name="توضیحات")

    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='financial_years')

    accounts = models.ManyToManyField(Account, related_name='financial_year', blank=True)
    floatAccounts = models.ManyToManyField(FloatAccount, related_name='financial_year', blank=True)
    floatAccountGroups = models.ManyToManyField(FloatAccountGroup, related_name='financial_year', blank=True)
    floatAccountRelations = models.ManyToManyField(FloatAccountRelation, related_name='financial_year', blank=True)
    defaultAccounts = models.ManyToManyField(DefaultAccount, related_name='financial_year', blank=True)

    wares = models.ManyToManyField(Ware, related_name='financial_year', blank=True)
    warehouses = models.ManyToManyField(Warehouse, related_name='financial_year', blank=True)
    wareLevels = models.ManyToManyField(WareLevel, related_name='financial_year', blank=True)
    units = models.ManyToManyField(Unit, related_name='financial_year', blank=True)
