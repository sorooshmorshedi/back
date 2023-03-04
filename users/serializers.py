from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from companies.models import CompanyUserInvitation, CompanyUser, Company, FinancialYear
from companies.serializers import FinancialYearSerializer, CompanySerializer
from helpers.functions import get_current_user
from server.settings import DATETIME_FORMAT
from users.models import Role, User, City, UserNotification, Notification


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())

    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ('id', 'company',)


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class PermissionListSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer()
    contentType = content_type

    class Meta:
        model = Permission
        fields = '__all__'


class RoleWithPermissionListSerializer(serializers.ModelSerializer):
    permissions = PermissionListSerializer(many=True)

    class Meta:
        model = Role
        fields = '__all__'


class UserSimpleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj: User):
        return obj.first_name + ' ' + obj.last_name

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'name')


class UserListRetrieveSerializer(serializers.ModelSerializer):
    active_company = CompanySerializer()
    active_financial_year = FinancialYearSerializer()
    roles = serializers.SerializerMethodField()
    financialYears = serializers.SerializerMethodField(method_name='get_financialYears')
    companies = serializers.SerializerMethodField(method_name='get_companies')
    name = serializers.SerializerMethodField()
    has_two_factor_authentication = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()
    unread_notifications_count = serializers.SerializerMethodField()
    pop_up_notifications = serializers.SerializerMethodField()

    def get_pop_up_notifications(self, obj: User):
        qs = obj.notifications.exclude(status=UserNotification.READ).filter(notification__show_pop_up=True)
        return UserNotificationSerializer(qs, many=True).data

    def get_unread_notifications_count(self, obj: User):
        return obj.notifications.exclude(status=UserNotification.READ).count()

    def get_company_user(self, obj: User):
        return CompanyUser.objects.filter(user=obj, company=obj.active_company).first()

    def get_roles(self, obj: User):
        company_user = self.get_company_user(obj)
        if company_user:
            return RoleWithPermissionListSerializer(
                company_user.roles.all(),
                many=True
            ).data
        return []

    def get_financialYears(self, obj: User):
        if obj.active_company:
            return FinancialYearSerializer(
                FinancialYear.objects.filter(company=obj.active_company),
                many=True
            ).data
        return []

    def get_companies(self, obj: User):
        return CompanySerializer(
            Company.objects.filter(superuser=obj),
            many=True
        ).data

    def get_modules(self, obj: User):
        active_company = obj.active_company
        if active_company:
            return obj.active_company.modules
        return obj.modules

    def get_name(self, obj: User):
        return obj.first_name + ' ' + obj.last_name

    def get_has_two_factor_authentication(self, obj: User):
        return obj.secret_key is not None

    class Meta:
        model = get_user_model()
        exclude = ('password', 'secret_key')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(default=None, allow_null=True, write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj: User):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'phone', 'password', 'token')

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class UserInvitationsListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name')

    class Meta:
        model = CompanyUserInvitation
        fields = ('id', 'company_name', 'status')


class UserNotificationSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    title = serializers.CharField(source='notification.title')
    explanation = serializers.CharField(source='notification.explanation')
    created_at = serializers.SerializerMethodField()
    status_codename = serializers.CharField(source='status')

    def get_created_at(self, obj: UserNotification):
        return obj.created_at.strftime(DATETIME_FORMAT)

    class Meta:
        model = UserNotification
        fields = ('id', 'title', 'explanation', 'status', 'created_at', 'status_codename')


class SendNotificationSerializer(serializers.ModelSerializer):
    userNotifications = UserNotificationSerializer(many=True, read_only=True)

    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj: Notification):
        return obj.created_at.strftime(DATETIME_FORMAT)

    class Meta:
        model = Notification
        fields = (
            'id', 'title', 'explanation', 'show_pop_up', 'has_schedule', 'send_date', 'send_time', 'receivers',
            'userNotifications', 'created_at',
        )

    def validate_receivers(self, value):
        if value:
            user = get_current_user()
            is_valid = CompanyUser.objects.filter(company=user.active_company, user__in=value).count() == len(value)
            if not is_valid:
                raise serializers.ValidationError("کاربران انتخاب شده معتبر نمی باشند")
        return value


class ReminderNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'title', 'explanation', 'send_date', 'send_time')

    def validate_receivers(self, value):
        if value:
            user = get_current_user()
            is_valid = user.active_company.filter(users__in=value).count() == len(value)
            if not is_valid:
                raise serializers.ValidationError("کاربران انتخاب شده معتبر نمی باشند")
        return value
