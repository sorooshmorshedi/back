from rest_framework import serializers
from distributions.models.distribution_model import Distribution
from distributions.serializers.car_serializers import CarListRetrieveSerializer
from factors.models import Factor
from factors.serializers import FactorListRetrieveSerializer
from users.serializers import UserSimpleSerializer


class DistributionRetrieveSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer()
    factors = FactorListRetrieveSerializer(many=True)
    car = CarListRetrieveSerializer()

    class Meta:
        model = Distribution
        fields = '__all__'


class DistributionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = '__all__'


class DistributionCreateUpdateSerializer(serializers.ModelSerializer):
    factors = serializers.PrimaryKeyRelatedField(many=True, queryset=Factor.objects.all())

    class Meta:
        model = Distribution
        exclude = ('financial_year', 'code')
