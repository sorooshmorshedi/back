from rest_framework import serializers

from _dashtbashi.models import Driver, Car, Driving
from wares.models import Unit, Warehouse, WareLevel, Ware, WareInventory


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        read_only_fields = ('financial_year',)


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ('financial_year',)


class DrivingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driving
        fields = '__all__'
        read_only_fields = ('financial_year',)


class DrivingListRetrieveSerializer(serializers.ModelSerializer):
    driver = DriverSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    title = serializers.SerializerMethodField()

    def get_title(self, obj: Driving):
        return "{} : {}".format(obj.driver.name, obj.car.car_number)

    class Meta:
        model = Driving
        fields = '__all__'
        read_only_fields = ('financial_year',)
