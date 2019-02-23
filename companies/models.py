from django.db import models
from django_jalali.db import models as jmodels


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

    def get_financial_year(self):
        return self.financial_years.get(is_active=True)


class FinancialYear(models.Model):
    name = models.CharField(unique=True, max_length=150)
    start = jmodels.jDateField()
    end = jmodels.jDateField()
    is_active = models.BooleanField(default=0)
    explanation = models.CharField(max_length=255, blank=True, verbose_name="توضیحات")

    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='financial_years')

    objects = models.Manager()
