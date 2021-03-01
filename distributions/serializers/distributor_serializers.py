from rest_framework import serializers
from distributions.models.distributor_model import Distributor
from users.serializers import UserSimpleSerializer


class DistributorListRetrieveSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Distributor
        fields = '__all__'


class DistributorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        exclude = ('financial_year', )
