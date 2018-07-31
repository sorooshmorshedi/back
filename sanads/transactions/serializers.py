from rest_framework import serializers
from accounts.accounts.serializers import AccountListRetrieveSerializer

from sanads.transactions.models import *


class TransactionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionItem
        fields = '__all__'

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data:
                raise serializers.ValidationError("حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['floatAccount'].floatAccountGroup != data['account'].floatAccountGroup:
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        return data


class TransactionItemListRetrieveSerializer(TransactionItemSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)

    class Meta(TransactionItemSerializer.Meta):
        pass


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data:
                raise serializers.ValidationError("حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['floatAccount'].floatAccountGroup != data['account'].floatAccountGroup:
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        return data

    def create(self, validated_data):
        sanad = Sanad(code=Sanad.objects.latest('code').code + 1, date=validated_data['date'])
        sanad.save()
        validated_data['sanad'] = sanad
        res = super(TransactionSerializer, self).create(validated_data)
        return res


class TransactionListRetrieveSerializer(TransactionSerializer):
    items = TransactionItemSerializer(read_only=True, many=True)

    class Meta(TransactionSerializer.Meta):
        pass

