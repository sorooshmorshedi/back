from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from companies.models import CompanyUserInvitation, CompanyUser
from companies.serializers import FinancialYearSerializer, CompanySerializer
from users.models import Role, User, City


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
    financialYears = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    has_two_factor_authentication = serializers.SerializerMethodField()

    def get_roles(self, obj: User):
        return RoleWithPermissionListSerializer(
            CompanyUser.objects.filter(user=obj, company=obj.active_company).first().roles.all(),
            many=True
        ).data

    def get_financialYears(self, obj: User):
        return FinancialYearSerializer(
            CompanyUser.objects.filter(user=obj, company=obj.active_company).first().financialYears.all(),
            many=True
        ).data

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
