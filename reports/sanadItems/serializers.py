from rest_framework import serializers

from accounts.accounts.models import Account, FloatAccount
from companies.models import FinancialYear
from sanads.models import SanadItem, Sanad
from sanads.serializers import FactorSanadSerializer, AdjustmentSanadSerializer, LadingSanadSerializer, \
    OilCompanyLadingSanadSerializer, StatusChangeSanadSerializer, TransactionSanadSerializer, \
    ImprestSettlementSanadSerializer
from users.serializers import UserSimpleSerializer


class FinancialYearSanadItemReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = ('id', 'name')


class SanadSanadItemReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanad
        fields = ('id', 'local_id', 'code', 'date', 'explanation', 'is_auto_created',
                  'factor',
                  'adjustment',
                  'lading',
                  'oilCompanyLading',
                  'statusChange',
                  'transaction',
                  'imprestSettlement',
                  )

    factor = FactorSanadSerializer(read_only=True, many=False)
    adjustment = AdjustmentSanadSerializer(read_only=True, many=False)
    lading = LadingSanadSerializer(read_only=True, many=False)
    oilCompanyLading = OilCompanyLadingSanadSerializer(read_only=True, many=False)
    statusChange = StatusChangeSanadSerializer(read_only=True, many=False)
    transaction = TransactionSanadSerializer(read_only=True, many=False)
    imprestSettlement = ImprestSettlementSanadSerializer(read_only=True, many=False)


class AccountSanadItemReportSerializer(serializers.ModelSerializer):
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


class FloatAccountSanadItemReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloatAccount
        fields = ('id', 'name')


class SanadItemReportSerializer(serializers.ModelSerializer):
    financial_year = FinancialYearSanadItemReportSerializer()
    sanad = SanadSanadItemReportSerializer(many=False, read_only=True)
    account = AccountSanadItemReportSerializer(many=False, read_only=True)
    floatAccount = FloatAccountSanadItemReportSerializer(many=False, read_only=True)
    costCenter = FloatAccountSanadItemReportSerializer(many=False, read_only=True)

    previous_bed = serializers.IntegerField()
    previous_bes = serializers.IntegerField()
    previous_remain = serializers.SerializerMethodField()
    previous_remain_type = serializers.SerializerMethodField()

    comulative_bed = serializers.SerializerMethodField()
    comulative_bes = serializers.SerializerMethodField()

    remain = serializers.SerializerMethodField()
    remain_type = serializers.SerializerMethodField()

    created_by = UserSimpleSerializer(many=False, read_only=True)

    def get_comulative_bed(self, obj):
        bed = obj.comulative_bed
        if self.consider_previous_remain:
            bed += obj.previous_bed
        return bed

    def get_comulative_bes(self, obj):
        bes = obj.comulative_bes
        if self.consider_previous_remain:
            bes += obj.previous_bes
        return bes

    def get_previous_remain(self, obj):
        return abs(obj.previous_bed - obj.previous_bes)

    def get_previous_remain_type(self, obj):
        return self.calc_remain_type(obj.previous_bed, obj.previous_bes)

    def get_remain(self, obj):
        remain = obj.comulative_bed - obj.comulative_bes
        if self.consider_previous_remain:
            remain = remain + obj.previous_bed - obj.previous_bes
        return abs(remain)

    def get_remain_type(self, obj):
        bed = obj.comulative_bed
        bes = obj.comulative_bes
        if self.consider_previous_remain:
            bed += obj.previous_bed
            bes += obj.previous_bes

        return self.calc_remain_type(bed, bes)

    def calc_remain_type(self, bed, bes):
        if bed > bes:
            return 'بد'
        elif bed < bes:
            return 'بس'
        else:
            return ' - '

    @property
    def consider_previous_remain(self):
        return self.context.get('consider_previous_remain', True)

    class Meta:
        model = SanadItem
        fields = (
            'id', 'account', 'sanad', 'explanation', 'bed', 'bes', 'comulative_bed', 'comulative_bes', 'remain',
            'remain_type', 'previous_bed', 'previous_bes', 'previous_remain', 'previous_remain_type', 'financial_year',
            'created_by', 'floatAccount', 'costCenter'
        )
