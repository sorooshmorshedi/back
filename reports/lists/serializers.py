from rest_framework import serializers

from accounts.accounts.models import Account
from cheques.models.ChequeModel import Cheque
from cheques.models.ChequebookModel import Chequebook
from cheques.serializers import ChequebookListRetrieveSerializer
from factors.models import Factor, FactorItem
from factors.serializers import FactorSerializer
from sanads.sanads.serializers import SanadSerializer
from sanads.transactions.models import Transaction
from wares.models import Ware, Warehouse


class AccountSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class WareSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ware
        fields = '__all__'


class WarehouseSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class TransactionListSerializer(serializers.ModelSerializer):
    account = AccountSimpleSerializer(read_only=True, many=False)
    sanad = SanadSerializer(read_only=True, many=False)

    class Meta:
        model = Transaction
        fields = '__all__'


class ChequeListSerializer(serializers.ModelSerializer):
    account = AccountSimpleSerializer(read_only=True, many=False)
    chequebook = ChequebookListRetrieveSerializer(read_only=True, many=False)
    title = serializers.SerializerMethodField()

    def get_title(self, obj: Cheque):
        if not obj.chequebook:
            return "{} - {} - {}".format(obj.serial, obj.account.title, obj.explanation)
        return "{} - {} - {}".format(obj.serial, obj.chequebook.account.title, obj.chequebook.explanation)

    class Meta:
        model = Cheque
        fields = '__all__'


class ChequebookListSerializer(serializers.ModelSerializer):
    account = AccountSimpleSerializer(read_only=True, many=False)

    class Meta:
        model = Chequebook
        fields = '__all__'


class FactorListSerializer(FactorSerializer):
    account = AccountSimpleSerializer(read_only=True, many=False)
    total_sum = serializers.SerializerMethodField()

    def get_total_sum(self, obj):
        return obj.totalSum

    class Meta:
        model = Factor
        fields = '__all__'


class FactorItemListSerializer(serializers.ModelSerializer):
    factor = FactorListSerializer(read_only=True, many=False)
    ware = WareSimpleSerializer(read_only=True, many=False)
    warehouse = WarehouseSimpleSerializer(read_only=True, many=False)

    value = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()

    def get_value(self, obj):
        return obj.value

    def get_discount(self, obj):
        return obj.discount

    def get_total_value(self, obj):
        return obj.totalValue

    class Meta:
        model = FactorItem
        fields = '__all__'
