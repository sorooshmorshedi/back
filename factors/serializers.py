from rest_framework import serializers

from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer, AccountSerializer
from factors.models import *
from sanads.sanads.serializers import SanadSerializer
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

    hasTax = serializers.SerializerMethodField()
    isPaid = serializers.SerializerMethodField()

    def get_isPaid(self, obj):
        return obj.paidValue == obj.totalSum

    def get_hasTax(self, obj):
        return obj.taxValue != 0 or obj.taxPercent != 0

    class Meta:
        model = Factor
        fields = '__all__'
        read_only_fields = ('id', 'code', )
        extra_kwargs = {
            "account": {
                "error_messages": {
                    "required": "نام حساب را وارد نکرده اید"
                }
            }
        }

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data or not data['floatAccount']:
                raise serializers.ValidationError("حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['account'].floatAccountGroup not in list(data['floatAccount'].floatAccountGroups.all()):
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")
        return data


class FactorItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FactorItem
        fields = '__all__'

    def validate(self, data):
        return data


class FactorItemRetrieveSerializer(FactorItemSerializer):
    ware = WareListRetrieveSerializer(read_only=True, many=False)
    warehouse = WarehouseSerializer(read_only=True, many=False)
    is_editable = serializers.SerializerMethodField()

    def get_is_editable(self, obj):
        return obj.get_is_editable()

    class Meta(FactorItemSerializer.Meta):
        pass


class TransactionSerializerForPayment(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class FactorPaymentWithTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializerForPayment(read_only=True, many=False)

    class Meta:
        model = FactorPayment
        fields = '__all__'


class FactorListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    expenses = FactorExpenseListRetrieveSerializer(read_only=True, many=True)
    items = FactorItemRetrieveSerializer(read_only=True, many=True)
    payments = FactorPaymentWithTransactionSerializer(read_only=True, many=True)
    sanad = SanadSerializer(read_only=True, many=False)

    class Meta:
        model = Factor
        fields = '__all__'


class FactorPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FactorPayment
        fields = '__all__'


class NotPaidFactorsSerializer(FactorSerializer):
    account = AccountSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    payments = FactorPaymentSerializer(read_only=True, many=True)
    sum = serializers.SerializerMethodField()

    def get_sum(self, obj):
        return obj.totalSum

    class Meta:
        model = Factor
        fields = '__all__'


# class WarehouseInventoryListRetrieveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WarehouseInventory
#         fields = '__all__'
