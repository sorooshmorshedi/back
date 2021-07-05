import re
from datetime import datetime
from django.utils.timezone import now
from django.db.models.aggregates import Max
from django.db.models.deletion import ProtectedError
from django.db.models.functions.comparison import Coalesce
from django_jalali.db import models as jmodels
from django.core.validators import RegexValidator
from django.db import models
import django.db.models.options as options
from rest_framework.exceptions import ValidationError

from helpers.functions import get_current_user, get_new_child_code

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

        company = None
        if financial_year:
            company = financial_year.company
        else:
            user = get_current_user()

            if not user:
                return super().get_queryset()

            financial_year = user.active_financial_year
            if financial_year:
                company = financial_year.company

        qs = qs.filter(financial_year__company=company)

        if self.model._meta.backward_financial_year:
            return qs.filter(financial_year__id__lte=financial_year.id)
        else:
            return qs.filter(financial_year=financial_year.id)


class BaseModel(models.Model):
    created_by = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, related_name='+')
    created_at = jmodels.jDateTimeField(auto_now=True, null=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True, null=True)
    is_auto_created = models.BooleanField(default=False)

    class Meta:
        abstract = True
        permissions = ()
        default_permissions = ()
        ordering = ['-pk']
        backward_financial_year = False
        permission_basename = None
        get_latest_by = 'pk'

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


class LocalIdMixin(models.Model):
    local_id = models.BigIntegerField(null=True, blank=True, default=None)

    @property
    def financial_year(self):
        raise NotImplementedError()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.local_id = self.__class__.objects.inFinancialYear(self.financial_year).aggregate(
                local_id=Coalesce(Max('local_id'), 0)
            )['local_id'] + 1
        super().save(*args, **kwargs)


class TreeMixin(models.Model):

    @property
    def CODE_LENGTHS(self):
        raise NotImplementedError()

    explanation = models.CharField(max_length=255, blank=True, null=True)

    level = models.IntegerField()
    code = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    class Meta:
        abstract = True

    def get_new_child_code(self):
        last_child_code = None

        last_child = self.children.order_by('-code').first()
        if last_child:
            last_child_code = last_child.code

        return get_new_child_code(
            self.code,
            self.CODE_LENGTHS[self.level + 1],
            last_child_code
        )

    @classmethod
    def get_new_code(cls):
        code = cls.objects.inFinancialYear().filter(level=0).aggregate(
            last_code=Max('code')
        )['last_code']

        if code:
            code = int(code) + 1
        else:
            code = 0

        if code < 9:
            code += 10

        if code >= 99:
            from rest_framework import serializers
            raise serializers.ValidationError("تعداد عضو های این سطح پر شده است")

        return str(code)


class DefinableManager(BaseManager):

    def definites(self, financial_year=None):
        return self.inFinancialYear(financial_year).filter(is_defined=True)

    def indefinites(self, financial_year=None):
        return self.inFinancialYear(financial_year).filter(is_defined=False)


class DefinableMixin(models.Model):
    is_defined = models.BooleanField(default=False)
    defined_by = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, related_name='+')
    definition_date = models.DateTimeField(blank=True, null=True)

    objects = DefinableManager()

    class Meta:
        abstract = True

    def define(self, date=None):
        if not self.is_defined:
            self.is_defined = True
            self.defined_by = get_current_user()
            self.definition_date = date or now()
            self.save()

    def indefine(self):
        self.is_defined = False
        self.defined_by = None
        self.definition_date = None
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
    return models.DecimalField(max_digits=24, decimal_places=6, default=kwargs.pop('default', 0), **kwargs)


def upload_to(instance, filename):
    app = instance._meta.app_label
    model = instance.__class__.__name__
    return "{}/{}/{}-{}".format(app, model, datetime.now().timestamp(), filename)


def manage_files(instance, data, file_fields):
    for file_field in file_fields:
        if data.get('delete_{}'.format(file_field), False):
            getattr(instance, file_field).delete()
            setattr(instance, file_field, None)
