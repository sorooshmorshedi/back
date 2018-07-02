from rest_framework import serializers
from accounts.costCenter.models import CostCenter, CostCenterGroup


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = ('pk', 'name', 'explanation', 'group')


class CostCenterGroupSerializer(serializers.ModelSerializer):
    costCenters = CostCenterSerializer(many=True, read_only=True)

    class Meta:
        model = CostCenterGroup
        fields = ('pk', 'name', 'explanation', 'costCenters')

