from rest_framework import serializers

from _dashtbashi.models import Lading
from accounts.accounts.serializers import AccountRetrieveSerializer, FloatAccountSerializer, AccountListSerializer
from accounts.accounts.validators import AccountValidator
from cheques.models.StatusChangeModel import StatusChange
from factors.models import Factor, Adjustment
from imprests.models import ImprestSettlement

from sanads.models import *
from transactions.models import Transaction
from users.serializers import UserSimpleSerializer


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
    account = AccountListSerializer(read_only=True, many=False)
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


class FactorSanadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = ('id', 'type')


class TransactionSanadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'type')


class AdjustmentSanadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjustment
        fields = ('id', 'type')


class LadingSanadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lading
        fields = ('id',)


class OilCompanyLadingSanadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lading
        fields = ('id',)


class StatusChangeSanadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='cheque.id')
    type = serializers.CharField(source='cheque.type')

    class Meta:
        model = StatusChange
        fields = ('id', 'type')


class ImprestSettlementSanadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='transaction.id')

    class Meta:
        model = ImprestSettlement
        fields = ('id',)


class SanadListRetrieveSerializer(SanadSerializer):
    items = SanadItemListRetrieveSerializer(read_only=True, many=True)
    created_by = UserSimpleSerializer()

    # this might be a performance problem
    factor = FactorSanadSerializer(read_only=True, many=False)
    adjustment = AdjustmentSanadSerializer(read_only=True, many=False)
    lading = LadingSanadSerializer(read_only=True, many=False)
    oilCompanyLading = OilCompanyLadingSanadSerializer(read_only=True, many=False)
    statusChange = StatusChangeSanadSerializer(read_only=True, many=False)
    transaction = TransactionSanadSerializer(read_only=True, many=False)
    imprestSettlement = ImprestSettlementSanadSerializer(read_only=True, many=False)

    class Meta(SanadSerializer.Meta):
        fields = '__all__'
