from rest_framework import serializers

from helpers.functions import get_current_user
from helpers.serializers import validate_required_fields
from wares.models import Unit, Warehouse, Ware, WareInventory, SalePriceType, SalePrice


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ('financial_year',)


class SalePriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalePriceType
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


def get_salePrices(obj: Ware):
    sale_prices = [{
        'unit': sale_price.unit.id,
        'conversion_factor': sale_price.conversion_factor,
        'prices': {}
    } for sale_price in obj.salePrices.all()]

    for sale_price in obj.salePrices.all():
        sale_price_dict = [d for d in sale_prices if d['unit'] == sale_price.unit.id][0]
        sale_price_dict['prices'][sale_price.type.id] = sale_price.price

    return sale_prices


class WareSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.code + ' - ' + obj.name

    class Meta:
        model = Ware
        fields = '__all__'
        read_only_fields = ('code', 'financial_year',)

    def validate(self, attrs):
        level = attrs.get('level')
        if level == Ware.WARE:
            validate_required_fields(attrs, ('warehouse', 'parent', 'pricingType'))
        return attrs


class WareInventoryListSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(many=False, read_only=True)

    class Meta:
        model = WareInventory
        fields = '__all__'


class SalePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalePrice
        fields = '__all__'


class WareRetrieveSerializer(WareSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    inventory = serializers.SerializerMethodField()
    salePrices = serializers.SerializerMethodField()

    def get_salePrices(self, obj):
        return get_salePrices(obj)

    def get_inventory(self, obj: Ware):
        qs = obj.inventory.filter(financial_year=get_current_user().active_financial_year).all()
        return WareInventoryListSerializer(qs, many=True).data

    class Meta(WareSerializer.Meta):
        pass


class WareListSerializer(WareSerializer):
    warehouse = WarehouseSimpleSerializer(read_only=True)
    salePrices = serializers.SerializerMethodField()

    def get_salePrices(self, obj):
        return get_salePrices(obj)

    class Meta:
        model = Ware
        fields = ('id', 'code', 'name', 'level', 'warehouse', 'parent', 'salePrices')
