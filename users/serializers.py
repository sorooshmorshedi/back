from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from companies.serializers import FinancialYearSerializer, CompanySerializer
from users.models import Role


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())

    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ('id', 'company',)


class UserListRetrieveSerializer(serializers.ModelSerializer):
    active_company = CompanySerializer()
    active_financial_year = FinancialYearSerializer()
    roles = RoleSerializer(many=True)

    class Meta:
        model = get_user_model()
        exclude = ('password',)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(default=None, allow_null=True, write_only=True)
    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all())

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password', 'roles')

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all())

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'roles')


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
