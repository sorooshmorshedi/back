from rest_framework import serializers

from accounts.defaultAccounts.serializers import DefaultAccountSerializer
from distributions.models.distributor_model import Distributor
from users.serializers import UserSimpleSerializer


class DistributorListRetrieveSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    defaultAccounts = DefaultAccountSerializer(many=True)

    class Meta:
        model = Distributor
        fields = '__all__'


class DistributorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        exclude = ('financial_year', )
