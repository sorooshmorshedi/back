import re
from datetime import datetime

import jdatetime
from django.db.models.aggregates import Max
from django.db.models.deletion import ProtectedError
from django.db.models.functions.comparison import Coalesce
from django_jalali.db import models as jmodels
from django.core.validators import RegexValidator
from django.db import models
import django.db.models.options as options
from rest_framework.exceptions import ValidationError

from helpers.functions import get_current_user

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('backward_financial_year', 'permission_basename')


class BaseManager(models.Manager):

    def hasAccess(self, method, permission_basename=None, use_financial_year=True, financial_year=None):
        user = get_current_user()

        if not user:
            return super().get_queryset()

        if hasattr(self.model, 'financial_year') and use_financial_year:
            queryset = self.inFinancialYear(financial_year)
        else:
            queryset = super().get_queryset()

        if not permission_basename:
            permission_basename = self.model._meta.permission_basename

        if not permission_basename:
            raise Exception("Please set permission_basename in {} Meta class or pass it to method".format(self))

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

        if user.has_perm("{}.{}".format(operation, permission_basename)):
            return queryset
        else:
            if user.has_perm("{}Own.{}".format(operation, permission_basename)):
                return queryset.filter(created_by=user)

        return queryset.none()

    def inFinancialYear(self, financial_year=None):
        from helpers.functions import get_current_user
        qs = super().get_queryset()

        user = get_current_user()

        if not user:
            return super().get_queryset()

        if not financial_year:
            financial_year = user.active_financial_year

        qs = qs.filter(financial_year__company=financial_year.company)

        if self.model._meta.backward_financial_year:
            return qs.filter(financial_year__id__lte=financial_year.id)
        else:
            return qs.filter(financial_year=financial_year.id)


class BaseModel(models.Model):
    created_by = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, related_name='own_%(class)s')
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
            obj = e.protected_objects[0]
            raise ValidationError({
                'non_field_error': 'ابتدا داده های وابسته را حذف نمایید',
                'related_id': obj.id,
                'related_class': obj.__class__.__name__
            })

        return result

    def update(self, **kwargs) -> None:
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
        self.save()


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


class LocalIdMixin(models.Model):
    local_id = models.BigIntegerField()

    @property
    def financial_year(self):
        raise NotImplementedError()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if not self.local_id:
            self.local_id = self.objects.inFinancialYear(self.financial_year).aggregate(
                local_id=Coalesce(Max('local_id'), 0)
            )['local_id'] + 1

        super().save(*args, **kwargs)


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
    return models.CharField(max_length=255, blank=True, null=True, default="")


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


def upload_to(instance, filename):
    app = instance._meta.app_label
    model = instance.__class__.__name__
    return "{}/{}/{}-{}".format(app, model, datetime.now().timestamp(), filename)


def manage_files(instance, data, file_fields):
    for file_field in file_fields:
        if data.get('delete_{}'.format(file_field), False):
            getattr(instance, file_field).delete()
            setattr(instance, file_field, None)
