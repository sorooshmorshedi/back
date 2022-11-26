from contracting.models import Tender, Contract, Statement, Supplement
from rest_framework import serializers


class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = '__all__'


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = '__all__'


class SupplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplement
        fields = '__all__'

    def validate(self, data):
        new_value = data.get('value')
        con = data.get('contract')
        contract_id = con.id
        contract = Contract.objects.get(pk=contract_id)
        max_change = contract.max_change_amount
        old_amount = contract.amount
        change = old_amount / 100 * max_change
        min_amount = old_amount - change
        max_amount = old_amount + change
        if new_value < min_amount or new_value > max_amount:
            raise serializers.ValidationError("مبلغ باید بین %s و %s باشد" % (min_amount, max_amount))
        return super(SupplementSerializer, self).validate(data)


class ContractSerializer(serializers.ModelSerializer):
    supplements = SupplementSerializer(read_only=True, many=True)

    class Meta:
        model = Contract
        fields = '__all__'


class ContractDetailsSerializer(serializers.ModelSerializer):
    statement = StatementSerializer(read_only=True, many=True)
    supplements = SupplementSerializer(read_only=True, many=True)

    class Meta:
        model = Contract
        fields = '__all__'
