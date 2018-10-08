from rest_framework import serializers

from accounts.accounts.models import Account
from cheques.models import Cheque, Chequebook
from factors.models import Factor
from factors.serializers import FactorSerializer
from sanads.sanads.serializers import SanadSerializer
from sanads.transactions.models import Transaction


class AccountSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TransactionListSerializer(serializers.ModelSerializer):
    account = AccountSimpleSerializer(read_only=True, many=False)
    sanad = SanadSerializer(read_only=True, many=False)

    class Meta:
        model = Transaction
        fields = '__all__'


class ChequeListSerializer(serializers.ModelSerializer):
    account = AccountSimpleSerializer(read_only=True, many=False)

    class Meta:
        model = Cheque
        fields = '__all__'


class ChequebookListSerializer(serializers.ModelSerializer):
    account = AccountSimpleSerializer(read_only=True, many=False)

    class Meta:
        model = Chequebook
        fields = '__all__'


class FactorListSerializer(FactorSerializer):
    sanad = SanadSerializer(read_only=True, many=False)
    account = AccountSimpleSerializer(read_only=True, many=False)

    class Meta:
        model = Factor
        fields = '__all__'

