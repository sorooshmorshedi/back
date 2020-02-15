from rest_framework import serializers

from accounts.accounts.models import *
from accounts.costCenters.serializers import CostCenterGroupSerializer


class FloatAccountSerializer(serializers.ModelSerializer):
    syncFloatAccountGroups = serializers.ListField(allow_empty=True, default=[])

    class Meta:
        model = FloatAccount
        fields = '__all__'


class FloatAccountGroupSerializer(serializers.ModelSerializer):
    floatAccounts = FloatAccountSerializer(many=True, read_only=True)

    class Meta:
        model = FloatAccountGroup
        fields = '__all__'


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


class IndependentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndependentAccount
        fields = ('id', 'name', 'explanation')


class AccountCreateUpdateSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        if type(obj) == Account:
            return obj.code + ' - ' + obj.name
        return ''

    class Meta:
        model = Account
        exclude = ('code', 'level')

    def validate(self, data):

        parent = data.get('patent', None)

        if parent:
            if parent.level == Account.MOEIN:
                floatAccountGroup = data.get('floatAccountGroup', None)
                if floatAccountGroup:
                    raise serializers.ValidationError("تنها حساب سطح آخر (تفضیلی) می تواند دارای گروه حساب شناور باشد")
                costCenterGroup = data.get('costCenterGroup', None)
                if costCenterGroup:
                    raise serializers.ValidationError("تنها حساب سطح آخر (تفضیلی) می تواند دارای گروه مرکز هزینه باشد")

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


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب اشخاص باید سطح آخر باشد")

        return data


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب بانک باید سطح آخر باشد")

        return data


class AccountListRetrieveCreateUpdateSerializer(AccountCreateUpdateSerializer):
    floatAccountGroup = FloatAccountGroupSerializer(read_only=True)
    costCenterGroup = CostCenterGroupSerializer(read_only=True)
    type = AccountTypeSerializer(read_only=True)
    person = PersonSerializer(read_only=True, many=False)
    bank = BankSerializer(read_only=True, many=False)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset \
            .prefetch_related('floatAccountGroup') \
            .prefetch_related('costCenterGroup') \
            .prefetch_related('type') \
            .prefetch_related('person') \
            .prefetch_related('bank')
        return queryset

    class Meta(AccountCreateUpdateSerializer.Meta):
        pass


# Other
class TypeReportAccountCreateUpdateSerializer(AccountCreateUpdateSerializer):
    remain = serializers.IntegerField()

    class Meta(AccountCreateUpdateSerializer.Meta):
        fields = ('id', 'title', 'remain')
