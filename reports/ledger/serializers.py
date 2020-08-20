from rest_framework import serializers

from accounts.accounts.models import Account
from sanads.models import SanadItem, Sanad


class SanadLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanad
        fields = ('code', 'date', )


class AccountLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('code', 'name')


class SanadItemLedgerSerializer(serializers.ModelSerializer):
    sanad = SanadLedgerSerializer(many=False, read_only=True)
    account = AccountLedgerSerializer(many=False, read_only=True)

    class Meta:
        model = SanadItem
        fields = ('account', 'sanad', 'explanation', 'bed', 'bes')

