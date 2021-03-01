from rest_framework import serializers
from distributions.models.distribution_model import Distribution
from distributions.serializers.car_serializers import CarListRetrieveSerializer
from factors.serializers import FactorListRetrieveSerializer


class DistributionListRetrieveSerializer(serializers.ModelSerializer):
    factors = FactorListRetrieveSerializer()
    car = CarListRetrieveSerializer()

    class Meta:
        model = Distribution
        fields = '__all__'


class DistributionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        exclude = ('financial_year', 'code')
