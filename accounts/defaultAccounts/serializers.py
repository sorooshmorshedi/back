from rest_framework import serializers

from accounts.accounts.serializers import AccountListRetrieveCreateUpdateSerializer
from accounts.defaultAccounts.models import DefaultAccount


class DefaultAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultAccount
        fields = ('id', 'name', 'explanation', 'account', 'usage')

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")

        return data


class DefaultAccountListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveCreateUpdateSerializer(read_only=True)

    class Meta:
        model = DefaultAccount
        fields = '__all__'


