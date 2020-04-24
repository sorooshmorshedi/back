import jdatetime
from django_jalali.db import models as jmodels
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework.exceptions import ValidationError


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

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    @property
    def last_financial_year(self):
        try:
            return self.financial_years.order_by('-id')[0]
        except (ObjectDoesNotExist, IndexError):
            return None

    class Meta:
        permissions = (
            ('get.company', 'مشاهده شرکت'),
            ('create.company', 'تعریف شرکت'),
            ('update.company', 'ویرایش شرکت'),
            ('delete.company', 'حذف شرکت'),
        )


class FinancialYear(models.Model):
    objects = models.Manager()

    name = models.CharField(unique=True, max_length=150)
    start = jmodels.jDateField()
    end = jmodels.jDateField()
    explanation = models.CharField(max_length=255, blank=True, verbose_name="توضیحات")

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

    def __str__(self):
        return "{} {} ({})".format(self.company, self.name, self.id)

    class Meta:
        permissions = (
            ('get.financialYear', 'مشاهده سال مالی'),
            ('create.financialYear', 'تعریف سال مالی'),
            ('update.financialYear', 'ویرایش سال مالی'),
            ('delete.financialYear', 'حذف سال مالی'),

            ('move.financialYear', 'انتقال سال مالی'),
            ('close.financialYear', 'بستن سال مالی'),
            ('cancelClosing.financialYear', 'لغو بستن سال مالی'),
        )

    @property
    def is_closed(self):
        return self.temporaryClosingSanad is not None

    def get_opening_sanad(self):
        from sanads.models import Sanad
        from sanads.models import newSanadCode

        if not self.openingSanad:
            code = newSanadCode(self)
            if code != 1:
                raise ValidationError('ابتدا سند های سال مالی جدید را پاک کنید')

            sanad = Sanad.objects.create(
                financial_year=self,
                code=code,
                createType=Sanad.AUTO,
                date=jdatetime.date.today()
            )
            self.openingSanad = sanad
            self.save()

        return self.openingSanad

    def check_closing_sanads(self):
        from sanads.models import Sanad
        from sanads.models import newSanadCode

        closing_sanads = [
            'temporaryClosingSanad',
            'currentEarningsClosingSanad',
            'permanentsClosingSanad'
        ]
        need_save = False

        for sanad_name in closing_sanads:
            if not getattr(self, sanad_name):
                sanad = Sanad.objects.create(
                    financial_year=self,
                    code=newSanadCode(self),
                    createType=Sanad.AUTO,
                    date=jdatetime.date.today()
                )
                setattr(self, sanad_name, sanad)
                need_save = True

        if need_save:
            self.save()

    def delete_closing_sanads(self):
        self.temporaryClosingSanad.delete()
        self.currentEarningsClosingSanad.delete()
        self.permanentsClosingSanad.delete()
