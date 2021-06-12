from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from companies.models import Company, FinancialYear, CompanyUser, CompanyUserInvitation, FinancialYearOperation


class FinancialYearOperationSerializer(serializers.ModelSerializer):
    from_financial_year_name = serializers.CharField(source='fromFinancialYear.name')
    to_financial_year_name = serializers.CharField(source='toFinancialYear.name', allow_null=True)
    operation = serializers.CharField(source='get_operation_display')
    operator_name = serializers.CharField(source='created_by.name')

    class Meta:
        model = FinancialYearOperation
        fields = '__all__'


class FinancialYearSerializer(serializers.ModelSerializer):
    is_closed = serializers.BooleanField()
    operations = FinancialYearOperationSerializer(many=True)

    class Meta:
        model = FinancialYear
        fields = '__all__'
        read_only_fields = ('company',)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('superuser',)


class CompanyUserListRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj: CompanyUser):
        from users.serializers import UserListRetrieveSerializer
        return UserListRetrieveSerializer(obj.user).data

    class Meta:
        model = CompanyUser
        fields = '__all__'


class CompanyUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = ('financialYears', 'roles')


class CompanyUserInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUserInvitation
        fields = '__all__'
        read_only_fields = ('company',)

    def validate(self, attrs):
        if self.instance and self.instance.status != CompanyUserInvitation.PENDING:
            raise ValidationError(["وضعیت دعوت اجازه این عملیات را نمی دهد."])
        return attrs
