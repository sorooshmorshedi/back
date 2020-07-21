import re

from django_jalali.db import models as jmodels
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
import django.db.models.options as options

from helpers.functions import get_current_user

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('backward_financial_year', 'permission_basename')


class BaseManager(models.Manager):

    def hasAccess(self, method, permission_basename=None, financial_year=None):
        user = get_current_user()

        if hasattr(self.model, 'financial_year'):
            queryset = self.inFinancialYear(financial_year)
        else:
            queryset = super().get_queryset()

        if not permission_basename:
            permission_basename = self.model._meta.permission_basename

        if not permission_basename:
            raise Exception("Please set permission_basename in model Meta class")

        operation = ""
        method = method.upper()
        if method == 'POST':
            operation = "create"
        if method == 'GET':
            operation = "get"
        if method == 'PUT':
            operation = "update"
        if method == 'DELETE':
            operation = "delete"

        if (
                not user.has_perm("{}.{}".format(operation, permission_basename))
                and user.has_perm("{}Own.{}".format(operation, permission_basename))
        ):
            queryset = queryset.filter(created_by=user)

        return queryset

    def inFinancialYear(self, financial_year=None):
        from helpers.functions import get_current_user
        qs = super().get_queryset()

        user = get_current_user()

        if not financial_year:
            financial_year = user.active_financial_year

        if self.model._meta.backward_financial_year:
            return qs.filter(financial_year__id__lte=financial_year.id)
        else:
            return qs.filter(financial_year=financial_year.id)


class BaseModel(models.Model):
    created_by = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True)
    created_at = jmodels.jDateTimeField(auto_now=True, null=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True
        permissions = ()
        default_permissions = ()
        ordering = ['pk']
        backward_financial_year = False
        permission_basename = None

    objects = BaseManager()

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.created_by = get_current_user()
        super().save(*args, **kwargs)


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


def EXPLANATION():
    return models.CharField(max_length=255, blank=True, null=True)


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
    return models.DecimalField(max_digits=24, decimal_places=6, default=0, **kwargs)
