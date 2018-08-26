from rest_framework import serializers
from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer
from accounts.costCenters.serializers import CostCenterSerializer

from sanads.sanads.models import *


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
            if data['floatAccount'].floatAccountGroup != data['account'].floatAccountGroup:
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        if 'costCenter' in data and data['costCenter']:
            if data['costCenter'].group != data['account'].costCenterGroup:
                raise serializers.ValidationError("مرکز هزینه انتخاب شده باید مطعلق به گروه مرکز هزینه حساب باشد")

        return data

    def update(self, instance, validated_data):
        if instance.sanad.createType == 'auto':
            raise serializers.ValidationError("سند های خودکار غیر قابل ویرایش می باشند")


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


class SanadListRetrieveSerializer(SanadSerializer):
    items = SanadItemListRetrieveSerializer(read_only=True, many=True)

    class Meta(SanadSerializer.Meta):
        pass


