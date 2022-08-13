from payroll.models import Workshop, Contract, Personnel, PersonnelFamily, ContractRow, HRLetter
from rest_framework import serializers


class WorkShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


class PersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnel
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class ContractRowSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractRow
        fields = '__all__'


class PersonnelFamilySerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonnelFamily
        fields = '__all__'


class HRLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = HRLetter
        fields = '__all__'


