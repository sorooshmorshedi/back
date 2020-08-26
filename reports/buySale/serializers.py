from factors.models import FactorItem, Factor
from reports.lists.serializers import FactorListCreateUpdateSerializer, WareSimpleSerializer, WarehouseSimpleSerializer
from rest_framework import serializers


class BuySaleSerializer(serializers.ModelSerializer):
    factor = FactorListCreateUpdateSerializer(read_only=True, many=False)
    ware = WareSimpleSerializer(read_only=True, many=False)
    warehouse = WarehouseSimpleSerializer(read_only=True, many=False)

    value = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()

    count = serializers.SerializerMethodField()

    def get_value(self, obj):
        return self.format_value(obj, obj.value)

    def get_discount(self, obj):
        return obj.discount

    def get_total_value(self, obj):
        return self.format_value(obj, obj.totalValue)

    def get_count(self, obj):
        return self.format_value(obj, obj.count)

    def format_value(self, obj, value):
        if obj.factor.type in (Factor.BACK_FROM_BUY, Factor.BACK_FROM_SALE):
            return -value
        return value

    class Meta:
        model = FactorItem
        fields = '__all__'
