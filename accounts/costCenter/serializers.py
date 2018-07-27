from rest_framework import serializers
from accounts.costCenter.models import CostCenter, CostCenterGroup


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = ('id', 'name', 'explanation', 'group')


class CostCenterGroupSerializer(serializers.ModelSerializer):
    costCenters = CostCenterSerializer(many=True, read_only=True)

    class Meta:
        model = CostCenterGroup
        fields = ('id', 'name', 'explanation', 'costCenters')

