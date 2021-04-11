from rest_framework import serializers
from home.models import Option, DefaultText


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'
        read_only_fields = ('name', 'codename')


class DefaultTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultText
        fields = '__all__'
        read_only_fields = ('financial_year', 'usage', 'name', 'key')
