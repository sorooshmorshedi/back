from rest_framework import serializers

from accounts.accounts.models import Account
from factors.models import FactorItem, Factor
from factors.serializers import FactorCreateUpdateSerializer, FactorItemSerializer
from reports.lists.serializers import WarehouseSimpleSerializer
from wares.models import Ware


class AccountInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'code', 'name')


class FactorWithAccountCreateUpdateSerializer(FactorCreateUpdateSerializer):
    account = AccountInventorySerializer(many=False, read_only=True)

    class Meta:
        model = Factor
        fields = ('id', 'code', 'date', 'type', 'account', 'explanation', 'is_definite', 'definition_date')


class WareInventorySerializer(serializers.ModelSerializer):
    factor = FactorWithAccountCreateUpdateSerializer(many=False, read_only=True)
    input = serializers.SerializerMethodField()
    output = serializers.SerializerMethodField()
    remain = serializers.SerializerMethodField()

    def get_input(self, obj):
        if obj.factor.type in (*Factor.BUY_GROUP, Factor.INPUT_ADJUSTMENT):
            if obj.factor.type in (Factor.BACK_FROM_SALE, Factor.INPUT_ADJUSTMENT):
                value = obj.calculated_value
                fee = '-'
            else:
                value = obj.value
                fee = obj.fee
            return {
                'count': obj.count,
                'fee': fee,
                'value': value
            }
        return {
            'count': '-',
            'fee': '-',
            'value': '-'
        }

    def get_output(self, obj: FactorItem):
        from wares.models import Ware
        if obj.ware.pricingType == Ware.WEIGHTED_MEAN and obj.remain_count:
            fee = round(obj.remain_value / obj.remain_count, 2)
        else:
            fee = '-'
        if obj.factor.type in (*Factor.SALE_GROUP, Factor.OUTPUT_ADJUSTMENT, Factor.CONSUMPTION_WARE):
            return {
                'count': obj.count,
                'fee': fee,
                'value': obj.calculated_value
            }
        return {
            'count': '-',
            'fee': '-',
            'value': '-'
        }

    def get_remain(self, obj):
        from wares.models import Ware
        if obj.ware.pricingType == Ware.WEIGHTED_MEAN and obj.remain_count:
            fee = round(obj.remain_value / obj.remain_count, 2)
        else:
            fee = '-'
        return {
            'count': obj.remain_count,
            'fee': fee,
            'value': obj.remain_value
        }

    class Meta:
        model = FactorItem
        fields = '__all__'


class AllWaresInventorySerializer(serializers.ModelSerializer):
    input = serializers.SerializerMethodField()
    output = serializers.SerializerMethodField()
    remain = serializers.SerializerMethodField()

    def get_input(self, obj):
        return {
            'count': obj.input_count,
            'fee': '-',
            'value': obj.input_value
        }

    def get_output(self, obj):
        factorItem = obj.factorItems.first
        if factorItem and obj.pricingType == Ware.WEIGHTED_MEAN and factorItem.remain_count:
            fee = factorItem.remain_value / factorItem.remain_count
        else:
            fee = '-'
        return {
            'count': obj.output_count,
            'fee': fee,
            'value': obj.output_value
        }

    def get_remain(self, obj):
        remain_count = obj.input_count - obj.output_count
        remain_value = obj.input_value - obj.output_value
        if obj.pricingType == Ware.WEIGHTED_MEAN and remain_count:
            fee = remain_value / remain_count
        else:
            fee = '-'
        return {
            'count': remain_count,
            'fee': fee,
            'value': remain_value
        }

    class Meta:
        model = Ware
        fields = ('id', 'code', 'name', 'input', 'output', 'remain')


class WarehouseInventorySerializer(serializers.ModelSerializer):
    factor = FactorWithAccountCreateUpdateSerializer(many=False, read_only=True)
    warehouse = WarehouseSimpleSerializer(many=False, read_only=True)
    input = serializers.SerializerMethodField()
    output = serializers.SerializerMethodField()
    remain = serializers.SerializerMethodField()

    cumulative_count = serializers.SerializerMethodField()

    def get_cumulative_count(self, obj):
        return {
            'input': obj.cumulative_input_count or 0,
            'output': obj.cumulative_output_count or 0,
        }

    def get_input(self, obj):
        if obj.factor.type in Factor.INPUT_GROUP:
            return obj.count
        return 0

    def get_output(self, obj):
        if obj.factor.type in Factor.OUTPUT_GROUP:
            return obj.count
        return 0

    def get_remain(self, obj):
        input_count = obj.cumulative_input_count if obj.cumulative_input_count else 0
        output_count = obj.cumulative_output_count if obj.cumulative_output_count else 0
        return input_count - output_count

    class Meta:
        model = FactorItem
        fields = '__all__'


class AllWarehousesInventorySerializer(serializers.ModelSerializer):
    input = serializers.IntegerField()
    output = serializers.IntegerField()
    remain = serializers.IntegerField()

    class Meta:
        model = Ware
        fields = ('id', 'name', 'input', 'output', 'remain')
