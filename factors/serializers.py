from rest_framework import serializers

from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer
from factors.models import *
from sanads.sanads.models import Sanad
from wares.serializers import WareListRetrieveSerializer, WarehouseSerializer


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        return data


class ExpenseListRetrieveSerializer(ExpenseSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)

    class Meta(ExpenseSerializer.Meta):
        pass


class FactorExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorExpense
        fields = '__all__'


class FactorExpenseListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    expense = ExpenseListRetrieveSerializer(read_only=True, many=False)

    class Meta:
        model = FactorExpense
        fields = '__all__'


class FactorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Factor
        fields = '__all__'

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data or not data['floatAccount']:
                raise serializers.ValidationError("حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['floatAccount'].floatAccountGroup != data['account'].floatAccountGroup:
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")
        return data

    def create(self, validated_data):
        sanad = Sanad(code=Sanad.objects.latest('code').code + 1, date=validated_data['date'], createType='auto')
        sanad.save()
        validated_data['sanad'] = sanad
        res = super(FactorSerializer, self).create(validated_data)
        return res


class FactorItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FactorItem
        fields = '__all__'

    def validate(self, data):
        return data


class FactorItemListRetrieveSerializer(FactorItemSerializer):
    ware = WareListRetrieveSerializer(read_only=True, many=False)
    wareHouse = WarehouseSerializer(read_only=True, many=False)

    class Meta(FactorItemSerializer.Meta):
        pass


class FactorListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    expenses = FactorExpenseListRetrieveSerializer(read_only=True, many=True)
    items = FactorItemListRetrieveSerializer(read_only=True, many=True)

    class Meta:
        model = Factor
        fields = '__all__'

