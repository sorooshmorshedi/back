from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from wares.models import Unit, Warehouse, WareLevel, Ware


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


class WareSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.code + ' - ' + obj.name

    class Meta:
        model = Ware
        fields = '__all__'
        read_only_fields = ('code', 'financial_year',)


class WareListRetrieveSerializer(WareSerializer):
    unit = UnitSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)

    class Meta(WareSerializer.Meta):
        pass


class WareLevelSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.code + ' - ' + obj.name

    class Meta:
        model = WareLevel
        fields = '__all__'
        read_only_fields = ('code', 'financial_year',)
