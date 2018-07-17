from rest_framework import serializers

from sanad.models import RPType


class RPTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RPType
        fields = ('pk', 'name', 'exp', 'account', 'type')

