import random
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import jdatetime
from django.contrib.auth.models import AbstractUser, Permission, UserManager
from django.contrib.postgres.fields.array import ArrayField
from django.db import models
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

    active_company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='usersActiveCompany', null=True,
                                       blank=True)
    active_financial_year = models.ForeignKey(FinancialYear, on_delete=models.SET_NULL, related_name='users', null=True,
                                              blank=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=11)

    # this field is not required, because it moved to CompanyUser
    roles = models.ManyToManyField(Role, related_name='users', blank=True)

    # this field is required for cave users
    modules = ArrayField(models.CharField(max_length=30), default=list, blank=True)

    max_companies = models.IntegerField(default=0)
    max_users = models.IntegerField(default=0)

    secret_key = models.CharField(max_length=32, null=True, blank=True, default=None)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    objects = MyUserManager()

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

    def get_superuser(self):
        return self.superuser or self

    def has_perm(self, permission_codename, company=None):
        if not self.is_active:
            return False

        company = company or self.active_company

        if not company:
            return True

        if self == company.superuser:
            return True

        company_user = self.companyUsers.all().filter(company=company).first()
        if not company_user:
            return False

        queryset = company_user.roles.filter(permissions__codename=permission_codename)

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
    def send_verification_code(phone):
        code = random.randint(1000, 9999)
        user = User.objects.filter(phone=phone).first()

        PhoneVerification.objects.create(
            user=user,
            phone=phone,
            code=code
        )

        res = Sms.send(phone, "کد تایید شما در سامانه سبحان: {}".format(code))
        print(res)

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
    name = models.CharField(max_length=255)

    class Meta(BaseModel.Meta):
        default_permissions = ()
        permissions = (
            ('create.city', 'تعریف شهر'),

            ('get.city', 'مشاهده شهر'),
            ('update.city', 'ویرایش شهر'),
            ('delete.city', 'حذف شهر'),

            ('getOwn.city', 'مشاهده شهر های خود'),
            ('updateOwn.city', 'ویرایش شهر های خود'),
            ('deleteOwn.city', 'حذف شهر های خود'),
        )


class Notification(BaseModel):
    SEND_BY_USER = 'su'
    REMINDER = 'sr'
    SEND_BY_SYSTEM = 'ss'
    SEND_BY_ADMIN = 'sa'

    TYPES = (
        (SEND_BY_USER, 'ارسال شده توسط کاربر'),
        (REMINDER, 'یاداور'),
        (SEND_BY_SYSTEM, 'ارسال شده توسط سامانه'),
        (SEND_BY_ADMIN, 'ارسال شده توسط ادمین')
    )

    type = models.CharField(max_length=2, choices=TYPES)

    title = models.CharField(max_length=255, blank=True, null=True)
    # explanation is html, so should showed in <pre> tag (so we can use js editor in admin to create explanation)
    explanation = models.TextField(blank=True, null=True)
    show_pop_up = models.BooleanField(default=False)

    is_sent = models.BooleanField(default=False)

    has_schedule = models.BooleanField(default=False)
    send_date = jmodels.jDateField(blank=True, null=True)
    send_time = models.TimeField(blank=True, null=True)

    send_notification = models.BooleanField(default=False)
    notification_title = models.CharField(max_length=255, blank=True, null=True)
    notification_explanation = models.TextField(blank=True, null=True)
    notification_link = models.CharField(max_length=255, blank=True, null=True)

    send_sms = models.BooleanField(default=False)
    sms_text = models.CharField(max_length=500, blank=True, null=True)

    receivers = models.ManyToManyField(User)

    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    class Meta(BaseModel.Meta):
        permissions = (
            ('send.notification', 'ارسال اعلان به سایر کاربران شرکت'),
        )

    def create_user_notifications(self):
        for receiver in self.receivers.all():
            self.userNotifications.create(
                user=receiver,
                status=UserNotification.NOT_READ,
            )
        self.is_sent = True
        self.save()


class UserNotification(BaseModel):
    PENDING = 'p'
    READ = 'r'
    NOT_READ = 'ur'

    STATUSES = (
        (PENDING, 'در انتظار ارسال'),
        (READ, 'خوانده شده'),
        (NOT_READ, 'خوانده نشده')
    )

    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='userNotifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    status = models.CharField(choices=STATUSES, max_length=2)

    notification_status = models.CharField(choices=STATUSES, max_length=2, blank=True, null=True)
    sms_status = models.CharField(choices=STATUSES, max_length=2, blank=True, null=True)

    def __str__(self):
        return "{} -> {} ({})".format(self.notification, self.user, self.id)
