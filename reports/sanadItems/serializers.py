from rest_framework import serializers

from accounts.accounts.models import Account
from sanads.models import SanadItem, Sanad


class SanadLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanad
        fields = ('code', 'date',)


class AccountLedgerSerializer(serializers.ModelSerializer):
    level0_name = serializers.CharField(source="parent.parent.parent.name")
    level0_code = serializers.CharField(source="parent.parent.parent.code")

    level1_name = serializers.CharField(source="parent.parent.name")
    level1_code = serializers.CharField(source="parent.parent.code")

    level2_name = serializers.CharField(source="parent.name")
    level2_code = serializers.CharField(source="parent.code")

    level3_name = serializers.CharField(source="name")
    level3_code = serializers.CharField(source="code")

    class Meta:
        model = Account
        fields = (
            'code', 'name',
            'level0_name', 'level0_code',
            'level1_name', 'level1_code',
            'level2_name', 'level2_code',
            'level3_name', 'level3_code'
        )


class SanadItemLedgerSerializer(serializers.ModelSerializer):
    sanad = SanadLedgerSerializer(many=False, read_only=True)
    account = AccountLedgerSerializer(many=False, read_only=True)

    previous_bed = serializers.IntegerField()
    previous_bes = serializers.IntegerField()
    previous_remain = serializers.SerializerMethodField()
    previous_remain_type = serializers.SerializerMethodField()

    comulative_bed = serializers.IntegerField()
    comulative_bes = serializers.IntegerField()

    remain = serializers.SerializerMethodField()
    remain_type = serializers.SerializerMethodField()

    def get_previous_remain(self, obj):
        return abs(obj.previous_bed - obj.previous_bes)

    def get_previous_remain_type(self, obj):
        return self.calc_remain_type(obj.previous_bed, obj.previous_bes)

    def get_remain(self, obj):
        return abs(obj.comulative_bed + obj.previous_bed - obj.comulative_bes - obj.previous_bes)

    def get_remain_type(self, obj):
        return self.calc_remain_type(obj.comulative_bed + obj.previous_bed, obj.comulative_bes + obj.previous_bes)

    def calc_remain_type(self, bed, bes):
        if bed > bes:
            return 'بد'
        elif bed < bes:
            return 'بس'
        else:
            return ' - '

    class Meta:
        model = SanadItem
        fields = (
            'id', 'account', 'sanad', 'explanation', 'bed', 'bes', 'comulative_bed', 'comulative_bes', 'remain',
            'remain_type', 'previous_bed', 'previous_bes', 'previous_remain', 'previous_remain_type'
        )