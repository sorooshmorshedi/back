from django.contrib.auth import get_user_model
from rest_framework import serializers

from companies.serializers import FinancialYearSerializer, CompanySerializer


class UserSerializer(serializers.ModelSerializer):
    active_company = CompanySerializer()
    active_financial_year = FinancialYearSerializer()

    class Meta:
        model = get_user_model()
        exclude = ('password', )

