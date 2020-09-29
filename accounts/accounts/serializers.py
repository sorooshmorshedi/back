from django.utils.functional import cached_property
from rest_framework import serializers

from accounts.accounts.models import FloatAccountGroup, FloatAccount, AccountType, Account, AccountBalance
from sanads.models import SanadItem


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
        fields = ('id', 'title', 'name')


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
            if not data.get('buyer_or_seller'):
                raise serializers.ValidationError("لطفا خریدار یا فروشنده را مشخص کنید")

            if not data.get('person_type'):
                raise serializers.ValidationError("لطفا نوع شخص را مشخص کنید")

        if self.instance and SanadItem.objects.filter(account=self.instance).exists():
            if self.instance.floatAccountGroup != data.get('floatAccountGroup'):
                raise serializers.ValidationError("گروه حساب شناور برای حساب دارای گردش غیر قابل ویرایش می باشد")
            if self.instance.costCenterGroup != data.get('costCenterGroup'):
                raise serializers.ValidationError(
                    "گروه مرکز هزینه و درآمد برای حساب دارای گردش غیر قابل ویرایش می باشد")

        return data

    def create(self, validated_data):
        data = validated_data.copy()
        data['type'] = data.get('type', None) or data['parent'].type

        return Account.objects.create(**data)

    def update(self, instance: Account, validated_data):
        old_type = instance.type

        if old_type != validated_data.get('type', old_type) and SanadItem.objects.filter(
                account__code__startswith=instance.code
        ).count() != 0:
            raise serializers.ValidationError("نوع حساب های دارای گردش غیر قابل ویرایش می باشد")

        print(validated_data)
        res = super().update(instance, validated_data)
        if instance.level != 0:
            # update children when account's type changes
            Account.objects.filter(
                code__startswith=instance.code,
                type=old_type
            ).update(type=instance.type)
        return res


class AccountRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    floatAccountGroup = FloatAccountGroupSerializer(read_only=True)
    costCenterGroup = FloatAccountGroupSerializer(read_only=True)
    type = AccountTypeSerializer(read_only=True)

    balance = serializers.SerializerMethodField()

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

    def get_title(self, obj):
        return obj.title

    class Meta:
        model = Account
        read_only_fields = ('financial_year', 'code', 'level')
        fields = (
            'id', 'title', 'floatAccountGroup', 'costCenterGroup', 'type',
            'name', 'code', 'level', 'person_type', 'buyer_or_seller', 'parent', 'account_type'
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
