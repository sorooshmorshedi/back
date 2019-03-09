from rest_framework import serializers
from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer
from accounts.costCenters.serializers import CostCenterSerializer
from factors.models import Factor

from sanads.sanads.models import *
from sanads.transactions.models import Transaction


class SanadItemSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(SanadItemSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = SanadItem
        fields = '__all__'

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data or not data['floatAccount']:
                raise serializers.ValidationError("حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['account'].floatAccountGroup not in list(data['floatAccount'].floatAccountGroups.all()):
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        if 'costCenter' in data and data['costCenter']:
            if data['costCenter'].group != data['account'].costCenterGroup:
                raise serializers.ValidationError("مرکز هزینه انتخاب شده باید مطعلق به گروه مرکز هزینه حساب باشد")

        return data

    def update(self, instance, validated_data):
        if instance.sanad.createType == 'auto':
            raise serializers.ValidationError("سند های خودکار غیر قابل ویرایش می باشند")
        return super(SanadItemSerializer, self).update(instance, validated_data)


class SanadItemListRetrieveSerializer(SanadItemSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = CostCenterSerializer(read_only=True, many=False)

    class Meta(SanadItemSerializer.Meta):
        pass


class SanadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanad
        fields = '__all__'

    def update(self, instance, validated_data):
        if instance.createType == 'auto':
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

    class Meta(SanadSerializer.Meta):
        fields = (
            "id",
            "code",
            "explanation",
            "date",
            "created_at",
            "updated_at",
            "type",
            "createType",
            "bed",
            "bes",
            "factor",
            "transaction",
            "items",
        )


