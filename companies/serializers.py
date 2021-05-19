from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from companies.models import Company, FinancialYear, CompanyUser, CompanyUserInvitation


class FinancialYearSerializer(serializers.ModelSerializer):
    is_closed = serializers.SerializerMethodField()

    def get_is_closed(self, obj: FinancialYear):
        return obj.is_closed

    class Meta:
        model = FinancialYear
        fields = '__all__'
        read_only_fields = ('company',)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('superuser',)


class CompanyUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj: CompanyUser):
        from users.serializers import UserListRetrieveSerializer
        return UserListRetrieveSerializer(obj.user).data

    class Meta:
        model = CompanyUser
        fields = '__all__'


class CompanyUserInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUserInvitation
        fields = '__all__'
        read_only_fields = ('company',)

    def validate(self, attrs):
        if self.instance and self.instance.status != CompanyUserInvitation.PENDING:
            raise ValidationError(["وضعیت دعوت اجازه این عملیات را نمی دهد."])
        return attrs
