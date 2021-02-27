from rest_framework import serializers

from accounts.accounts.models import Account
from accounts.accounts.serializers import AccountListSerializer, FloatAccountSerializer
from accounts.accounts.validators import AccountValidator
from accounts.defaultAccounts.models import DefaultAccount


class DefaultAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultAccount
        read_only_fields = ('id', 'codename',)
        exclude = ('financial_year',)

    def validate(self, data):
        defaultAccount = self.instance
        account = data.get('account')
        if defaultAccount:
            if int(account.level) != int(defaultAccount.account_level):
                raise serializers.ValidationError("سطح حساب اشتباه می باشد")

        return data


class DefaultAccountListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListSerializer(read_only=True)
    floatAccount = FloatAccountSerializer(read_only=True)
    costCenter = FloatAccountSerializer(read_only=True)

    class Meta:
        model = DefaultAccount
        fields = '__all__'
