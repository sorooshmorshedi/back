from rest_framework import serializers

from accounts.accounts.models import Account
from cheques.models.ChequeModel import Cheque
from cheques.models.ChequebookModel import Chequebook
from cheques.serializers import ChequebookListRetrieveSerializer
from factors.models import Factor
from factors.models.factor import FactorItem
from factors.serializers import FactorCreateUpdateSerializer
from imprests.serializers import ImprestSettlementSimpleSerializer
from sanads.models import Sanad
from sanads.serializers import SanadSerializer
from transactions.models import Transaction
from users.serializers import UserSimpleSerializer
from wares.models import Ware, Warehouse, SalePrice, SalePriceChange, WareSalePriceChange
from wares.serializers import SalePriceTypeSerializer, WareListSerializer, UnitSerializer


class SanadListSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(many=False)

    class Meta:
        model = Sanad
        fields = '__all__'
        read_only_fields = ('financial_year', 'code', 'local_id')

    def update(self, instance, validated_data):
        if instance.is_auto_created:
            raise serializers.ValidationError("سند های خودکار غیر قابل ویرایش می باشند")
        return super(SanadSerializer, self).update(instance, validated_data)


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
    imprestSettlement = ImprestSettlementSimpleSerializer(read_only=True, many=False)

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


class FactorListCreateUpdateSerializer(FactorCreateUpdateSerializer):
    account = AccountSimpleSerializer(read_only=True, many=False)

    class Meta:
        model = Factor
        fields = '__all__'


class FactorItemListSerializer(serializers.ModelSerializer):
    factor = FactorListCreateUpdateSerializer(read_only=True, many=False)
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


class SalePriceListSerializer(serializers.ModelSerializer):
    ware = WareListSerializer()
    type = SalePriceTypeSerializer()
    mainUnit = UnitSerializer()
    unit = UnitSerializer()

    class Meta:
        model = SalePrice
        fields = '__all__'


class SalePriceChangeListSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = SalePriceChange
        fields = '__all__'


class WareSalePriceChangeListSerializer(serializers.ModelSerializer):
    salePrice = SalePriceListSerializer()

    class Meta:
        model = WareSalePriceChange
        fields = '__all__'
