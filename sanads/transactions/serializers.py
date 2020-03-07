from rest_framework import serializers

from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer
from accounts.defaultAccounts.serializers import DefaultAccountListRetrieveSerializer
from cheques.serializers import ChequeListRetrieveSerializer
from sanads.sanads.models import newSanadCode
from sanads.sanads.serializers import SanadSerializer
from sanads.transactions.models import *


class TransactionItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = '__all__'
        read_only_fields = ('financial_year',)

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data or not data['floatAccount']:
                raise serializers.ValidationError(
                    "حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['account'].floatAccountGroup not in list(data['floatAccount'].floatAccountGroups.all()):
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        return data


class TransactionItemListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    type = DefaultAccountListRetrieveSerializer(read_only=True, many=False)
    cheque = ChequeListRetrieveSerializer(read_only=True, many=False)

    class Meta:
        model = TransactionItem
        fields = '__all__'


class TransactionCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('financial_year', 'code', 'sanad')

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data:
                raise serializers.ValidationError(
                    "حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['account'].floatAccountGroup not in list(data['floatAccount'].floatAccountGroups.all()):
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        return data


class TransactionListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    items = TransactionItemListRetrieveSerializer(read_only=True, many=True)
    sanad_code = serializers.IntegerField(source="sanad.code")

    class Meta:
        model = Transaction
        fields = '__all__'
