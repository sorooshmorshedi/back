from rest_framework import serializers
from accounts.accounts.serializers import AccountRetrieveSerializer, FloatAccountSerializer
from accounts.accounts.validators import AccountValidator
from factors.models import Factor

from sanads.models import *
from transactions.models import Transaction
from users.serializers import UserListRetrieveSerializer, UserCreateSerializer


class SanadItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanadItem
        fields = '__all__'
        read_only_fields = ('financial_year', 'code')

    def validate(self, data):
        AccountValidator.tafsili(data)

        return data

    def update(self, instance, validated_data):
        if instance.sanad.is_auto_created:
            raise serializers.ValidationError("سند های خودکار غیر قابل ویرایش می باشند")
        return super(SanadItemSerializer, self).update(instance, validated_data)


class SanadItemListRetrieveSerializer(SanadItemSerializer):
    account = AccountRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)

    class Meta(SanadItemSerializer.Meta):
        pass


class SanadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanad
        fields = '__all__'
        read_only_fields = ('financial_year', 'code', 'local_id')

    def update(self, instance, validated_data):
        if instance.is_auto_created:
            raise serializers.ValidationError("سند های خودکار غیر قابل ویرایش می باشند")
        return super(SanadSerializer, self).update(instance, validated_data)


class FactorWithTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = ('id', 'type')


class TransactionWithTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'type')


class SanadListRetrieveSerializer(SanadSerializer):
    items = SanadItemListRetrieveSerializer(read_only=True, many=True)
    factor = FactorWithTypeSerializer(read_only=True, many=False)
    transaction = TransactionWithTypeSerializer(read_only=True, many=False)
    created_by = UserListRetrieveSerializer()

    class Meta(SanadSerializer.Meta):
        fields = '__all__'
