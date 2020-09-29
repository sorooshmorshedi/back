import random
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import jdatetime
from django.contrib.auth.models import AbstractUser, Permission, UserManager
from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django.shortcuts import get_object_or_404
from django_jalali.db import models as jmodels
from rest_framework.exceptions import ValidationError, PermissionDenied
from companies.models import Company, FinancialYear
from helpers.models import BaseModel, BaseManager
from helpers.sms import Sms


class Role(BaseModel):
    company = models.ForeignKey(Company, related_name='roles', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')

    class Meta(BaseModel.Meta):
        permission_basename = 'role'
        permissions = (
            ('get.role', 'مشاهده نقش'),
            ('create.role', 'تعریف نقش'),
            ('update.role', 'ویرایش نقش'),
            ('delete.role', 'حذف نقش'),

            ('getOwn.role', 'مشاهده نقش خود'),
            ('updateOwn.role', 'ویرایش نقش خود'),
            ('deleteOwn.role', 'حذف نقش خود'),
        )


class MyUserManager(UserManager, BaseManager):
    pass


class User(AbstractUser, BaseModel):
    superuser = models.ForeignKey('self', on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    def get_superuser(self):
        return self.superuser or self

    active_company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='usersActiveCompany', null=True,
                                       blank=True)
    active_financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT, related_name='users', null=True,
                                              blank=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=11)

    roles = models.ManyToManyField(Role, related_name='users', blank=True)

    modules = ArrayField(models.CharField(max_length=30), default=list, blank=True)

    objects = MyUserManager()

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]+$',
                message='نام کاربری باید از حدوف و اعداد انگلیسی تشکیل شود'
            )
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
        default_permissions = ()

        permission_basename = 'user'
        permissions = (
            ('get.user', 'مشاهده کاربر'),
            ('create.user', 'تعریف کاربر'),
            ('update.user', 'ویرایش کاربر'),
            ('delete.user', 'حذف کاربر'),
            ('changePassword.user', 'تغییر کلمه عبور کاربران'),

            ('getOwn.user', 'مشاهده کاربران خود'),
            ('updateOwn.user', 'ویرایش کاربران خود'),
            ('deleteOwn.user', 'حذف کاربران خود'),
            ('changePasswordOwn.user', 'تغییر کلمه عبور کاربران خود'),

        )

    def has_perm(self, permission_codename, company=None):
        if not self.is_active:
            return False
        if self.is_superuser:
            return True

        if not company:
            company = self.active_company

        queryset = self.roles.filter(permissions__codename=permission_codename)

        # Allow all users to get list of companies
        permission_parts = permission_codename.split('.')
        if permission_parts[0] == 'get' and permission_parts[1] == Company._meta.permission_basename:
            return queryset.exists()

        return queryset.filter(company=company).exists()

    def has_object_perm(self, instance: BaseModel, permission_codename, company=None, raise_exception=False):
        has_perm = self.has_perm(permission_codename, company)
        if not has_perm and instance.created_by == self:
            operation = permission_codename.split('.')[0]
            permission_codename.replace(operation, "{}Own".format(operation))
            has_perm = self.has_perm(permission_codename, company)

        if not has_perm and raise_exception:
            raise PermissionDenied()

        return has_perm


class PhoneVerification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verificationCodes', null=True, blank=True)
    code = models.CharField(max_length=12)
    phone = models.CharField(max_length=11)

    created_at = jmodels.jDateTimeField(auto_now=True)
    updated_at = jmodels.jDateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return (self.created_at + timedelta(minutes=5)) < jdatetime.datetime.utcnow()

    def __str__(self):
        return "user: {}, phone: {}, code: {}, datetime: {}".format(self.user, self.phone, self.code, self.created_at)

    class Meta(BaseModel.Meta):
        get_latest_by = 'id'

    @staticmethod
    def send_verification_code(phone, has_user):
        code = random.randint(1000, 9999)
        user = None
        if has_user:
            user = get_object_or_404(User, phone=phone)

        PhoneVerification.objects.create(
            user=user,
            phone=phone,
            code=code
        )

        Sms.send(phone, "کد تایید شما در سامانه سبحان: {}".format(code))

    @staticmethod
    def check_verification(phone, code, raise_exception=False):
        phone_verification = PhoneVerification.objects.filter(phone=phone, code=code).earliest()
        if phone_verification:
            if not phone_verification.is_expired:
                return phone_verification
            elif raise_exception:
                raise ValidationError("کد تایید شما منقضی شده است")
        elif raise_exception:
            raise ValidationError("شماره یا کد تایید اشتباه است")
        return None


class City(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    class Meta(BaseModel.Meta):
        default_permissions = ()
        permissions = (
            ('get.city', 'مشاهده شهر'),
            ('create.city', 'تعریف شهر'),
            ('update.city', 'ویرایش شهر'),
            ('delete.city', 'حذف شهر'),
        )
