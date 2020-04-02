from django.utils.functional import cached_property
from rest_framework import serializers

from accounts.accounts.models import FloatAccountGroup, FloatAccount, AccountType, Account, AccountBalance
from sanads.sanads.models import SanadItem


class FloatAccountGroupSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloatAccountGroup
        fields = '__all__'
        read_only_fields = ['financial_year']


class FloatAccountSerializer(serializers.ModelSerializer):
    floatAccountGroups = FloatAccountGroupSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = FloatAccount
        fields = '__all__'
        read_only_fields = ['financial_year']


class FloatAccountGroupSerializer(serializers.ModelSerializer):
    floatAccounts = FloatAccountSerializer(many=True, read_only=True)

    class Meta:
        model = FloatAccountGroup
        fields = '__all__'
        read_only_fields = ['financial_year']


class AccountTypeSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        res = obj.name
        if obj.nature != 'non':
            res += ' - ' \
                   + ('بدهکار' if obj.nature == 'bed' else 'بستانکار')

        usage = [u for u in AccountType.ACCOUNT_TYPE_USAGES if u[0] == obj.usage]
        if len(usage) != 0 and usage[0][0] != 'none':
            res += ' - ' + usage[0][1]

        return res

    class Meta:
        model = AccountType
        fields = '__all__'
        read_only_fields = ['financial_year']


class AccountCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('financial_year', 'code', 'level')

    def validate(self, data):

        account_type = data.get('account_type', None)
        if not account_type:
            raise serializers.ValidationError("نوع حساب مشخص نشده است")

        if account_type == Account.PERSON:
            person_type = data.get('person_type')
            if not person_type:
                raise serializers.ValidationError("لطفا خریدار یا فروشنده را مشخص کنید")

        if self.instance and SanadItem.objects.filter(account=self.instance).exists():
            if self.instance.floatAccountGroup != data.get('floatAccountGroup'):
                raise serializers.ValidationError("گروه حساب شناور برای حساب دارای گردش غیر قابل ویرایش می باشد")
            if self.instance.costCenterGroup != data.get('costCenterGroup'):
                raise serializers.ValidationError("گروه مرکز هزینه برای حساب دارای گردش غیر قابل ویرایش می باشد")

        return data

    def create(self, validated_data):
        data = validated_data.copy()
        account_type = data.get('type', None)
        if account_type:
            data['type'] = data['parent'].type

        return Account.objects.create(**data)

    def update(self, instance, validated_data):
        res = super().update(instance, validated_data)
        if instance.level != 0:
            # update children when account's type changes
            Account.objects.filter(code__startswith=instance.code).update(type=instance.type)
        return res


class AccountListRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    floatAccountGroup = FloatAccountGroupSerializer(read_only=True)
    costCenterGroup = FloatAccountGroupSerializer(read_only=True)
    type = AccountTypeSerializer(read_only=True)

    balance = serializers.SerializerMethodField()

    def get_balance(self, obj: Account):
        bed = bes = 0
        for balance in self.balances:
            if balance.account.code.startswith(obj.code):
                bed += balance.bed
                bes = + balance.bes
        remain = abs(bed - bes)
        return {
            'bed': bed,
            'bes': bes,
            'remain': remain
        }

    def get_title(self, obj):
        return obj.title

    class Meta:
        model = Account
        read_only_fields = ('financial_year', 'code', 'level')
        fields = '__all__'

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset \
            .prefetch_related('floatAccountGroup') \
            .prefetch_related('costCenterGroup') \
            .prefetch_related('type')
        return queryset

    @cached_property
    def balances(self):
        return AccountBalance.objects.inFinancialYear().prefetch_related('account').all()


# Other
class TypeReportAccountSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        if type(obj) == Account:
            return obj.title
        return ''

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['financial_year']

    remain = serializers.IntegerField()
