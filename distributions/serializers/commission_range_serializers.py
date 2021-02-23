from rest_framework import serializers
from distributions.models import CommissionRangeItem, CommissionRange


class CommissionRangeItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionRangeItem
        exclude = ('financial_year',)


class CommissionRangeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionRange
        exclude = ('financial_year',)


class CommissionRangeListRetrieveSerializer(serializers.ModelSerializer):
    items = CommissionRangeItemListSerializer(many=True)

    class Meta:
        model = CommissionRange
        exclude = ('financial_year',)
