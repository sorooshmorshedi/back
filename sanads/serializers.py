from rest_framework import serializers

from accounts.accounts.serializers import AccountListRetrieveSerializer
from sanads.models import RPType


class RPTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RPType
        fields = ('pk', 'name', 'exp', 'account', 'usage')

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")

        return data


class RPTypeListRetrieveSerializer(RPTypeSerializer):
    account = AccountListRetrieveSerializer(read_only=True)


