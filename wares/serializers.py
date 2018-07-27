from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from wares.models import Unit, WareHouse, WareLevel, Ware


class UnitSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return str(obj.id) + ' - ' + obj.name

    class Meta:
        model = Unit
        fields = ('id', 'name', 'explanation', 'title')


class WareHouseSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return str(obj.id) + ' - ' + obj.name

    class Meta:
        model = WareHouse
        fields = ('id', 'name', 'explanation', 'title')


class WareSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.code + ' - ' + obj.name

    class Meta:
        model = Ware
        fields = (
            'id',
            'name',
            'price',
            'code',
            'explanation',
            'is_disabled',
            'min_sale',
            'max_sale',
            'min_inventory',
            'max_inventory',
            'created_at',
            'updated_at',
            'category',
            'title',
            'wareHouse',
            'unit',
            'supplier',
            'pricing_type',
        )

    def validate(self, data):
        return data


class WareListRetrieveSerializer(WareSerializer):
    unit = UnitSerializer(read_only=True)
    wareHouse = WareHouseSerializer(read_only=True)

    class Meta(WareSerializer.Meta):
        pass


class WareLevelSerializer(serializers.ModelSerializer):
    children = serializers.ListSerializer(read_only=True, child=RecursiveField())
    title = serializers.SerializerMethodField()
    # wares = WareSerializer(many=True, read_only=True)

    def get_title(self, obj):
        return obj.code + ' - ' + obj.name

    class Meta:
        model = WareLevel
        fields = ('id', 'code', 'name', 'explanation', 'children', 'title', 'parent', 'level')



