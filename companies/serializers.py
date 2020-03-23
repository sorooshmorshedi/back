from rest_framework import serializers

from companies.models import Company, FinancialYear


class FinancialYearSerializer(serializers.ModelSerializer):
    is_closed = serializers.SerializerMethodField()

    def get_is_closed(self, obj: FinancialYear):
        return obj.is_closed

    class Meta:
        model = FinancialYear
        fields = '__all__'

    def validate(self, attrs):
        # todo: validate company id
        return attrs


class CompanySerializer(serializers.ModelSerializer):
    financial_years = FinancialYearSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'
