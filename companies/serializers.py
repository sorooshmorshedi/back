from rest_framework import serializers

from companies.models import Company, FinancialYear


class FinancialYearSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialYear
        fields = '__all__'

    def validate(self, attrs):
        # todo: validate company id
        return attrs


class CompanySerializer(serializers.ModelSerializer):
    financial_year = serializers.SerializerMethodField()
    financial_years = FinancialYearSerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'

    def get_financial_year(self, company):
        financial_year = company.get_financial_year()
        return FinancialYearSerializer(financial_year).data

