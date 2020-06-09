import random
from datetime import timedelta
import jdatetime
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.shortcuts import get_object_or_404
from django_jalali.db import models as jmodels
from rest_framework.exceptions import ValidationError

from companies.models import Company, FinancialYear
from helpers.sms import Sms


class Role(models.Model):
    company = models.ForeignKey(Company, related_name='roles', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')

    class Meta:
        default_permissions = ()
        permissions = (
            ('get.role', 'مشاهده نقش'),
            ('create.role', 'تعریف نقش'),
            ('update.role', 'ویرایش نقش'),
            ('delete.role', 'حذف نقش'),
        )


class User(AbstractUser):
    active_company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='usersActiveCompany',
                                       blank=True, null=True)
    active_financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT, related_name='users',
                                              blank=True, null=True)

    phone = models.CharField(max_length=11)

    roles = models.ManyToManyField(Role, related_name='users')

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
        default_permissions = ()
        permissions = (
            ('get.user', 'مشاهده کاربر'),
            ('create.user', 'تعریف کاربر'),
            ('update.user', 'ویرایش کاربر'),
            ('delete.user', 'حذف کاربر'),

            ('changePassword.user', 'تغییر کلمه عبور کاربران'),
        )

    def has_perm(self, permission_codename, company=None):
        if not self.is_active:
            return False
        if self.is_superuser:
            return True

        if not company:
            company = self.active_company

        return self.roles.filter(company=company, permissions__codename=permission_codename).exists()


class PhoneVerification(models.Model):
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

    class Meta:
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
