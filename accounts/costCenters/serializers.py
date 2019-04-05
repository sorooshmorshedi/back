from rest_framework import serializers
from accounts.costCenters.models import CostCenter, CostCenterGroup


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = '__all__'


class CostCenterGroupSerializer(serializers.ModelSerializer):
    costCenters = CostCenterSerializer(many=True, read_only=True)

    class Meta:
        model = CostCenterGroup
        fields = '__all__'

