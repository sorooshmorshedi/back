from rest_framework import serializers

from distributions.models.path_model import Path


class PathListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        fields = '__all__'


class PathCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        exclude = ('financial_year', 'code')
