import re

import jdatetime
from django.db.models.deletion import ProtectedError
from django_jalali.db import models as jmodels
from django.core.validators import RegexValidator
from django.db import models
import django.db.models.options as options
from rest_framework.exceptions import ValidationError

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

        method = method.upper()
        if method == 'POST':
            operation = "create"
        elif method == 'GET':
            operation = "get"
        elif method == 'PUT':
            operation = "update"
        elif method == 'DELETE':
            operation = "delete"
        else:
            operation = method

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
    is_auto_created = models.BooleanField(default=False)

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

    def delete(self, *args, **kwargs):
        try:
            result = super(BaseModel, self).delete(*args, **kwargs)
        except ProtectedError as e:
            raise ValidationError('ابتدا داده های وابسته را حذف نمایید')

        return result


class ConfirmationMixin(models.Model):
    first_confirmed_at = jmodels.jDateTimeField(null=True, default=None)
    first_confirmed_by = models.ForeignKey('users.User', on_delete=models.PROTECT,
                                           related_name='first_%(class)sConfirmer', null=True)

    second_confirmed_at = jmodels.jDateTimeField(null=True, default=None)
    second_confirmed_by = models.ForeignKey('users.User', on_delete=models.PROTECT,
                                            related_name='second_%(class)sConfirmer', null=True)

    class Meta:
        abstract = True

    @property
    def has_first_confirm_permission(self):
        user = get_current_user()
        first_confirm_permission_codename = "firstConfirm.{}".format(self._meta.permission_basename)
        return user.has_object_perm(self, first_confirm_permission_codename)

    @property
    def has_second_confirm_permission(self):
        user = get_current_user()
        second_confirm_permission_codename = "secondConfirm.{}".format(self._meta.permission_basename)
        return user.has_object_perm(self, second_confirm_permission_codename)

    @property
    def has_first_confirmation(self):
        return self.first_confirmed_at is not None

    @property
    def has_second_confirmation(self):
        return self.second_confirmed_at is not None

    def can_confirm(self):

        if self.first_confirmed_at is None:
            if self.has_first_confirm_permission or self.has_second_confirm_permission:
                return True
        else:
            if self.has_second_confirm_permission:
                return True

        return False

    def confirm(self):
        user = get_current_user()
        if not self.has_first_confirmation:
            self.first_confirmed_by = user
            self.first_confirmed_at = jdatetime.datetime.now()
        else:
            self.second_confirmed_by = user
            self.second_confirmed_at = jdatetime.datetime.now()
        self.save()

    def cancelConfirm(self):
        if self.has_second_confirmation:
            self.second_confirmed_by = None
            self.second_confirmed_at = None
        else:
            self.first_confirmed_by = None
            self.first_confirmed_at = None
        self.save()


def DATE(**kwargs):
    return jmodels.jDateField(**kwargs)


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
