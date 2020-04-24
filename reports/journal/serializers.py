from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from accounts.accounts.models import Account
from sanads.models import SanadItem, Sanad


class SanadJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanad
        fields = ('code', 'date',)


class AccountJournalSerializer(serializers.ModelSerializer):
    parent = RecursiveField(allow_null=True)

    class Meta:
        model = Account
        fields = ('code', 'name', 'parent')


class SanadItemJournalSerializer(serializers.ModelSerializer):
    sanad = SanadJournalSerializer(many=False, read_only=True)
    account = AccountJournalSerializer(many=False, read_only=True)

    class Meta:
        model = SanadItem
        fields = ('account', 'sanad', 'explanation', 'bed', 'bes')

