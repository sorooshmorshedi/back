from rest_framework import serializers

from accounts.accounts.models import FloatAccountGroup, FloatAccount, AccountType, Account
from sanads.models import SanadItem
from wares.serializers import SalePriceTypeSerializer


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
        fields = ('id', 'title', 'name')


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('financial_year', 'code', 'level', 'type')

    def validate(self, data):

        account_type = data.get('account_type', None)
        if not self.instance and not account_type:
            raise serializers.ValidationError("نوع حساب مشخص نشده است")

        if account_type == Account.PERSON:
            if not data.get('buyer_or_seller'):
                raise serializers.ValidationError("لطفا خریدار یا فروشنده را مشخص کنید")

            if not data.get('person_type'):
                raise serializers.ValidationError("لطفا نوع شخص را مشخص کنید")

        if self.instance and self.instance.has_turnover():
            not_editable_fields = [{
                'name': 'floatAccountGroup',
                'title': 'گروه حساب شناور',
            }, {
                'name': 'costCenterGroup',
                'title': 'گروه مرکز هزینه',
            }]
            for field in not_editable_fields:
                if getattr(self.instance, field['name']) != data.get(field['name']):
                    raise serializers.ValidationError(
                        "{} برای حساب دارای گردش غیر قابل ویرایش می باشد".format(field['title'])
                    )

        return data


class AccountUpdateSerializer(AccountCreateSerializer):
    class Meta:
        model = Account
        exclude = ('financial_year', 'code', 'level', 'type', 'account_type')


class AccountRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    floatAccountGroup = FloatAccountGroupSerializer(read_only=True)
    costCenterGroup = FloatAccountGroupSerializer(read_only=True)
    type = AccountTypeSerializer(read_only=True)

    balance = serializers.SerializerMethodField()
    defaultSalePriceType = SalePriceTypeSerializer()

    def get_balance(self, obj: Account):
        return obj.get_balance()

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


class AccountListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    floatAccountGroup = FloatAccountGroupSerializer(read_only=True)
    costCenterGroup = FloatAccountGroupSerializer(read_only=True)
    type = AccountTypeSerializer(read_only=True)
    defaultSalePriceType = SalePriceTypeSerializer()

    def get_title(self, obj):
        return obj.title

    class Meta:
        model = Account
        read_only_fields = ('financial_year', 'code', 'level')
        fields = (
            'id', 'title', 'floatAccountGroup', 'costCenterGroup', 'type',
            'name', 'code', 'level', 'person_type', 'buyer_or_seller', 'parent', 'account_type',
            'defaultSalePriceType', 'path'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset \
            .prefetch_related('floatAccountGroup') \
            .prefetch_related('costCenterGroup') \
            .prefetch_related('type')
        return queryset


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
