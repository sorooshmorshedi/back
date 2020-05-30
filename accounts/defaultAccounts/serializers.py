from rest_framework import serializers

from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer
from accounts.accounts.validators import AccountValidator
from accounts.defaultAccounts.models import DefaultAccount


class DefaultAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultAccount
        read_only_fields = ('id', 'programingName',)
        exclude = ('financial_year', )

    def validate(self, data):
        AccountValidator.tafsili(data)

        return data


class DefaultAccountListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True)
    floatAccount = FloatAccountSerializer(read_only=True)
    costCenter = FloatAccountSerializer(read_only=True)

    class Meta:
        model = DefaultAccount
        fields = '__all__'
