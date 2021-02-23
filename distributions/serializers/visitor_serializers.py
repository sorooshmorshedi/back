from rest_framework import serializers
from distributions.models import Visitor
from distributions.serializers.commission_range_serializers import CommissionRangeCreateUpdateSerializer
from users.serializers import UserSimpleSerializer


class VisitorListRetrieveSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    commissionRange = CommissionRangeCreateUpdateSerializer()

    class Meta:
        model = Visitor
        fields = '__all__'


class VisitorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        exclude = ('financial_year', 'code')
