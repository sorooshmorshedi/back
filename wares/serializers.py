from rest_framework import serializers

from helpers.functions import get_current_user
from wares.models import Unit, Warehouse, WareLevel, Ware, WareInventory


class UnitSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return str(obj.id) + ' - ' + obj.name

    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ('financial_year',)


class WarehouseSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return str(obj.id) + ' - ' + obj.name

    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ('financial_year',)


class WarehouseSimpleSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return str(obj.id) + ' - ' + obj.name

    class Meta:
        model = Warehouse
        fields = ('id', 'name', 'title')


class WareSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.code + ' - ' + obj.name

    class Meta:
        model = Ware
        fields = '__all__'
        read_only_fields = ('code', 'financial_year',)


class WareInventoryListSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(many=False, read_only=True)

    class Meta:
        model = WareInventory
        fields = '__all__'


class WareRetrieveSerializer(WareSerializer):
    unit = UnitSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)
    inventory = serializers.SerializerMethodField()

    def get_inventory(self, obj: Ware):
        qs = obj.inventory.filter(financial_year=get_current_user().active_financial_year).all()
        return WareInventoryListSerializer(qs, many=True).data

    class Meta(WareSerializer.Meta):
        pass


class WareListSerializer(WareSerializer):
    unit_name = serializers.CharField(source='unit.name')
    warehouse = WarehouseSimpleSerializer(read_only=True)

    class Meta:
        model = Ware
        fields = ('id', 'name', 'unit_name', 'warehouse', 'price')


class WareLevelSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.code + ' - ' + obj.name

    class Meta:
        model = WareLevel
        fields = '__all__'
        read_only_fields = ('code', 'financial_year',)
