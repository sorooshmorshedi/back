from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from wares.models import Unit, Warehouse, WareLevel, Ware


class UnitSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return str(obj.id) + ' - ' + obj.name

    class Meta:
        model = Unit
        fields = ('id', 'name', 'explanation', 'title')


class WarehouseSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return str(obj.id) + ' - ' + obj.name

    class Meta:
        model = Warehouse
        fields = ('id', 'name', 'explanation', 'title')


class WareSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.code + ' - ' + obj.name

    class Meta:
        model = Ware
        fields = '__all__'

    def validate(self, data):
        return data


class WareListRetrieveSerializer(WareSerializer):
    unit = UnitSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)

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



