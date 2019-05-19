from rest_framework import serializers

from accounts.accounts.models import Account
from factors.models import FactorItem, Factor
from factors.serializers import FactorSerializer


class AccountInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'code', 'name')


class FactorWithAccountSerializer(FactorSerializer):
    account = AccountInventorySerializer(many=False, read_only=True)

    class Meta:
        model = Factor
        fields = ('id', 'code', 'date', 'type', 'isPaid', 'account', 'explanation', 'is_definite', 'definition_date')


class FactorItemInventorySerializer(serializers.ModelSerializer):
    factor = FactorWithAccountSerializer(many=False, read_only=True)
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
        if obj.factor.type in Factor.BUY_GROUP:
            return {
                'count': obj.count,
                'fee': obj.fee,
                'value': obj.value
            }
        return {
            'count': '-',
            'fee': '-',
            'value': '-'
        }

    def get_output(self, obj):
        from wares.models import Ware
        if obj.ware.pricingType == Ware.WEIGHTED_MEAN and obj.remain_count:
            fee = obj.remain_value / obj.remain_count
        else:
            fee = '-'
        if obj.factor.type in Factor.SALE_GROUP:
            return {
                'count': obj.count,
                'fee': fee,
                'value': obj.calculated_output_value
            }
        return {
            'count': '-',
            'fee': '-',
            'value': '-'
        }

    def get_remain(self, obj):
        from wares.models import Ware
        if obj.ware.pricingType == Ware.WEIGHTED_MEAN and obj.remain_count:
            fee = obj.remain_value / obj.remain_count
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
