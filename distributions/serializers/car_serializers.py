from rest_framework import serializers

from distributions.models.car_model import Car
from distributions.serializers.distributor_serializers import DistributorListRetrieveSerializer
from distributions.serializers.driver_serializers import DriverListRetrieveSerializer


class CarListRetrieveSerializer(serializers.ModelSerializer):
    driver = DriverListRetrieveSerializer()
    distributor = DistributorListRetrieveSerializer()

    class Meta:
        model = Car
        fields = '__all__'


class CarCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        exclude = ('financial_year', )
