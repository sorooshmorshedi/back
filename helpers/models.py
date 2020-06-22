import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('backward_financial_year',)


class BaseManager(models.Manager):

    def inFinancialYear(self, financial_year=None):
        from helpers.functions import get_current_user
        user = get_current_user()

        if not financial_year:
            financial_year = user.active_financial_year

        qs = super().get_queryset()
        if self.model._meta.backward_financial_year:
            return qs.filter(financial_year__id__lte=financial_year.id)
        else:
            return qs.filter(financial_year=financial_year.id)


class BaseModel(models.Model):
    class Meta:
        abstract = True
        permissions = ()
        default_permissions = ()
        ordering = ['pk']
        backward_financial_year = False

    objects = BaseManager()


def POSTAL_CODE(**kwargs):
    return models.CharField(
        **kwargs,
        max_length=10,
        validators=[RegexValidator(regex='^.{10}$', message='طول کد پستی باید 10 رقم باشد', code='nomatch')]
    )


def PHONE(**kwargs):
    return models.CharField(
        **kwargs,
        max_length=11,
        validators=[RegexValidator(regex='^.{11}$', message='طول شماره موبایل باید 11 رقم باشد', code='nomatch')]
    )


EXPLANATION = models.CharField(max_length=255, blank=True, null=True)


def is_valid_melli_code(value):
    if not re.search(r'^\d{10}$', value):
        is_valid = False
    else:
        check = int(value[9])
        s = sum([int(value[x]) * (10 - x) for x in range(9)]) % 11
        is_valid = (2 > s == check) or (s >= 2 and check + s == 11)

    if not is_valid:
        raise ValidationError("کد ملی وارد شده صحیح نیست")


def MELLI_CODE(**kwargs):
    return models.CharField(
        **kwargs,
        max_length=10,
        validators=[is_valid_melli_code]
    )


def DECIMAL(**kwargs):
    return models.DecimalField(max_digits=24, decimal_places=0, default=0, **kwargs)
