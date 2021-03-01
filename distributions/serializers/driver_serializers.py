from rest_framework import serializers
from distributions.models.driver_model import Driver
from users.serializers import UserSimpleSerializer


class DriverListRetrieveSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Driver
        fields = '__all__'


class DriverCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        exclude = ('financial_year', )
