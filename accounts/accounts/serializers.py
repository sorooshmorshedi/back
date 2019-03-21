from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from accounts.accounts.models import *
from accounts.costCenters.serializers import CostCenterGroupSerializer


class FloatAccountSerializer(serializers.ModelSerializer):
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
            res += ' - '\
                + ('بدهکار' if obj.nature == 'bed' else 'بستانکار')

        usage = [u for u in ACCOUNT_TYPE_USAGES if u[0] == obj.usage]
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


class AccountSerializer(serializers.ModelSerializer):
    # children = serializers.ListSerializer(read_only=True, child=RecursiveField())
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.code + ' - ' + obj.name

    class Meta:
        model = Account
        fields = '__all__'

    def validate(self, data):
        CODE_LENGTHS = [1, 3, 5, 9]
        PARENT_PART = [0, 1, 3, 5]
        if len(data['code']) != CODE_LENGTHS[data['level']]:
            raise serializers.ValidationError("کد حساب نا معتبر می باشد")
        if data['level'] != 0:
            if 'parent' not in data.keys():
                raise serializers.ValidationError("حساب های زیر مجموعه گروه، باید پدر داشته باشند")
            if data['parent'].code != data['code'][0:PARENT_PART[data['level']]]:
                raise serializers.ValidationError("کد حساب، با حساب پدر مطابقت ندارد")
            if data['parent'].level != data['level'] - 1:
                raise serializers.ValidationError("سطح حساب، با حساب پدر مطابقت ندارد")
        else:
            if 'parent' in data.keys() and data['parent'] is not None:
                raise serializers.ValidationError("حساب گروه، نمی تواند پدر داشته باشد")

        if 'floatAccountGroup' in data.keys() and data['floatAccountGroup'] is not None and data['level'] != 3:
            raise serializers.ValidationError("تنها حساب سطح آخر (تفضیلی) می تواند دارای گروه حساب شناور باشد")

        if 'costCenterGroup' in data.keys() and data['costCenterGroup'] is not None and data['level'] != 3:
            raise serializers.ValidationError("تنها حساب سطح آخر (تفضیلی) می تواند دارای گروه مرکز هزینه باشد")

        return data

    def create(self, validated_data):
        data = validated_data.copy()
        if data['level'] != 0 and ('type' not in data.keys() or ('type' in data.keys() and data['type'] is None)):
            data['type'] = data['parent'].type

        return Account.objects.create(**data)

    def update(self, instance, validated_data):
        res = super().update(instance, validated_data)
        if instance.level != 0:
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


class AccountListRetrieveSerializer(AccountSerializer):
    floatAccountGroup = FloatAccountGroupSerializer(read_only=True)
    costCenterGroup = CostCenterGroupSerializer(read_only=True)
    type = AccountTypeSerializer(read_only=True)
    person = PersonSerializer(read_only=True, many=False)
    bank = BankSerializer(read_only=True, many=False)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset\
            .prefetch_related('floatAccountGroup')\
            .prefetch_related('costCenterGroup')\
            .prefetch_related('type')\
            .prefetch_related('person')\
            .prefetch_related('bank')
        return queryset

    class Meta(AccountSerializer.Meta):
        pass


# Other
class TypeReportAccountSerializer(AccountSerializer):
    remain = serializers.IntegerField()

    class Meta(AccountSerializer.Meta):
        fields = ('id', 'title', 'remain')

