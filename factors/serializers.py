import datetime

from django.db.models import Max, Q
from rest_framework import serializers

from accounts.accounts.serializers import AccountRetrieveSerializer, FloatAccountSerializer, AccountListSerializer
from accounts.accounts.validators import AccountValidator
from factors.adjustment_sanad import AdjustmentSanad
from factors.models import Expense, Factor, Adjustment
from factors.models.factor import FactorExpense, FactorPayment, FactorItem, FactorsAggregatedSanad
from factors.models.transfer_model import Transfer
from factors.models.warehouse_handling import WarehouseHandling, WarehouseHandlingItem
from factors.views.definite_factor import DefiniteFactor
from helpers.functions import get_current_user
from sanads.serializers import SanadSerializer
from transactions.models import Transaction
from users.serializers import UserSimpleSerializer
from wares.models import WareInventory, Ware, Warehouse
from wares.serializers import WareRetrieveSerializer, WarehouseSerializer, WareListSerializer, \
    WarehouseSimpleSerializer, UnitSerializer
from django.utils.timezone import now


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    def validate(self, data):
        AccountValidator.tafsili(data)
        return data


class ExpenseListRetrieveSerializer(ExpenseSerializer):
    account = AccountRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)

    class Meta(ExpenseSerializer.Meta):
        pass


class FactorExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorExpense
        fields = '__all__'
        read_only_fields = ['id', 'financial_year']


class FactorExpenseListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)
    expense = ExpenseListRetrieveSerializer(read_only=True, many=False)

    class Meta:
        model = FactorExpense
        fields = '__all__'


class FactorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = '__all__'
        read_only_fields = ['id', 'temporary_code', 'code', 'definition_date', 'financial_year']
        extra_kwargs = {
            "account": {
                "error_messages": {
                    "required": "نام حساب را وارد نکرده اید"
                }
            }
        }

    def validate(self, data):
        AccountValidator.tafsili(data)
        return super(FactorCreateUpdateSerializer, self).validate(data)


class FactorItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorItem
        fields = '__all__'
        read_only_fields = ['id', 'financial_year']

    def validate(self, attrs):
        ware = attrs.get('ware')
        warehouse = attrs.get('warehouse')

        if not ware.is_service and not warehouse:
            raise serializers.ValidationError("انبار اجباری می باشد")

        return super(FactorItemSerializer, self).validate(attrs)

    def update(self, instance, validated_data):
        return super(FactorItemSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        return super(FactorItemSerializer, self).create(validated_data)


class FactorItemRetrieveSerializer(serializers.ModelSerializer):
    ware = WareListSerializer(read_only=True, many=False)
    unit = UnitSerializer(read_only=True, many=False)
    warehouse = WarehouseSimpleSerializer(read_only=True, many=False)

    factorItem = serializers.SerializerMethodField()
    preFactorItem = serializers.SerializerMethodField()

    def get_factorItem(self, obj: FactorItem):
        factor_item = getattr(obj, 'factorItem', None)
        if factor_item:
            return {
                'id': factor_item.id,
                'order': factor_item.order,
                'factor_id': factor_item.factor_id,
                'factor_type': factor_item.factor.type,
                'factor_temporary_code': factor_item.factor.temporary_code,
            }
        else:
            return None

    def get_preFactorItem(self, obj: FactorItem):
        pre_factor_item = getattr(obj, 'preFactorItem', None)
        if pre_factor_item:
            return {
                'id': pre_factor_item.id,
                'order': pre_factor_item.order,
                'factor__id': pre_factor_item.factor_id,
                'factor__is_pre_factor': pre_factor_item.factor.is_pre_factor,
                'factor__type': pre_factor_item.factor.type,
                'factor__temporary_code': pre_factor_item.factor.temporary_code,
            }
        else:
            return None

    class Meta:
        model = FactorItem
        fields = (
            'id', 'order', 'ware', 'unit', 'warehouse', 'unit_count', 'count', 'fee', 'discountValue',
            'discountPercent', 'explanation', 'tax_value', 'tax_percent', 'fees', 'factorItem', 'preFactorItem', 'meta',
        )


class TransactionSerializerForPayment(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class FactorPaymentWithTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializerForPayment(read_only=True, many=False)

    class Meta:
        model = FactorPayment
        fields = '__all__'


class BackFactorSerializer(serializers.ModelSerializer):
    items = FactorItemRetrieveSerializer(read_only=True, many=True)

    class Meta:
        model = Factor
        fields = '__all__'


class FactorListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)
    expenses = FactorExpenseListRetrieveSerializer(read_only=True, many=True)
    items = FactorItemRetrieveSerializer(read_only=True, many=True)
    payments = FactorPaymentWithTransactionSerializer(read_only=True, many=True)
    sanad = SanadSerializer(read_only=True, many=False)
    created_by = UserSimpleSerializer(read_only=True)
    backFactor = BackFactorSerializer(read_only=True)

    class Meta:
        model = Factor
        fields = '__all__'


class FactorPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorPayment
        fields = '__all__'
        read_only_fields = ('financial_year',)


class TransferListRetrieveSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    created_by = UserSimpleSerializer(many=False, read_only=True)

    def get_items(self, obj):
        input_items = obj.input_factor.items.order_by('id') \
            .prefetch_related('warehouse')

        output_items = obj.output_factor.items.order_by('id') \
            .prefetch_related('warehouse')

        items = []
        for i in range(len(input_items)):
            input_item = input_items[i]
            output_item = output_items[i]

            ware = WareRetrieveSerializer(input_item.ware).data
            unit = UnitSerializer(input_item.unit).data
            explanation = input_item.explanation
            output_warehouse = WarehouseSerializer(output_item.warehouse).data
            input_warehouse = WarehouseSerializer(input_item.warehouse).data

            items.append({
                'ware': ware,
                'unit': unit,
                'unit_count': input_item.unit_count,
                'count': input_item.count,
                'explanation': explanation,
                'output_warehouse': output_warehouse,
                'input_warehouse': input_warehouse,
            })

        return items

    class Meta:
        model = Transfer
        fields = '__all__'


class TransferCreateUpdateSerializer(serializers.ModelSerializer):
    items = serializers.ListField()

    class Meta:
        model = Transfer
        fields = ('id', 'explanation', 'date', 'time', 'items')

    @staticmethod
    def sync(instance: Transfer, validated_data):

        output_factor = instance.output_factor
        input_factor = instance.input_factor

        explanation = validated_data.get('explanation', '')

        if instance.financial_year.is_advari and instance.is_defined:
            input_factor.definition_date = datetime.datetime.combine(instance.date.togregorian(), instance.time)
            output_factor.definition_date = datetime.datetime.combine(instance.date.togregorian(), instance.time)

        input_factor.date = instance.date
        input_factor.explanation = instance.explanation
        input_factor.save()

        output_factor.date = instance.date
        output_factor.explanation = instance.explanation
        output_factor.save()

        input_items_data = []
        output_items_data = []
        for item in validated_data['items']:
            input_items_data.append({**item, 'warehouse': item['input_warehouse']})
            output_items_data.append({**item, 'warehouse': item['output_warehouse']})

        input_factor.verify_items(input_items_data)
        output_factor.verify_items(output_items_data)

        if instance.is_defined:
            DefiniteFactor.updateFactorInventory(input_factor, revert=True)
            DefiniteFactor.updateFactorInventory(output_factor, revert=True)

        input_factor.items.all().delete()
        output_factor.items.all().delete()

        for item in validated_data['items']:
            input_warehouse = Warehouse.objects.get(pk=item['input_warehouse'])
            output_warehouse = Warehouse.objects.get(pk=item['output_warehouse'])

            item_data = {
                'financial_year': instance.financial_year,
                'explanation': item.get('explanation', ''),
                'count': item['count'],
                'unit_count': item['unit_count'],
                'unit_id': item['unit'],
                'ware_id': item['ware'],
            }

            # move ware out
            output_factor_item = output_factor.items.create(
                **item_data,
                fee=0,
                warehouse=output_warehouse
            )

            if instance.is_defined:
                DefiniteFactor._updateInventory(output_factor_item, revert=False)

            # move wares in
            output_factor_item.refresh_from_db()
            fee = 0
            total_count = 0
            for output_fee in output_factor_item.fees:
                fee += output_fee['fee'] * output_fee['count']
                total_count += output_fee['count']
            if total_count != 0:
                fee /= total_count

            input_factor_item = input_factor.items.create(
                **item_data,
                fee=fee,
                warehouse=input_warehouse,
            )

            if instance.is_defined:
                DefiniteFactor._updateInventory(input_factor_item, revert=False)

        transfer_data = {
            'input_factor': input_factor,
            'output_factor': output_factor,
            'date': validated_data['date'],
            'time': validated_data['time'],
            'explanation': explanation,
        }

        instance.update(**transfer_data)

        validated_data.pop('items')

        return instance

    def create(self, validated_data):
        financial_year = self.context['financial_year']
        date = validated_data['date']
        time = validated_data['time']
        explanation = validated_data.get('explanation', '')

        factor_data = {
            'financial_year': financial_year,
            'date': date,
            'time': time,
            'explanation': explanation,
            'is_auto_created': True
        }
        input_factor = Factor.objects.create(
            **factor_data,
            type=Factor.INPUT_TRANSFER,
            temporary_code=Factor.get_new_temporary_code(Factor.INPUT_TRANSFER),
        )
        input_factor.save()
        output_factor = Factor.objects.create(
            **factor_data,
            type=Factor.OUTPUT_TRANSFER,
            temporary_code=Factor.get_new_temporary_code(Factor.OUTPUT_TRANSFER),
        )
        output_factor.save()

        code = Transfer.objects.aggregate(Max('code'))['code__max']
        if code:
            code += 1
        else:
            code = 1

        transfer_data = {
            'financial_year': financial_year,
            'input_factor': input_factor,
            'output_factor': output_factor,
            'date': date,
            'time': time,
            'explanation': explanation,
            'code': code
        }

        transfer = Transfer.objects.create(**transfer_data)

        self.sync(transfer, validated_data)

        return transfer

    def update(self, instance: Transfer, validated_data):
        input_factor = instance.input_factor
        output_factor = instance.output_factor

        date = validated_data['date']
        explanation = validated_data.get('explanation', '')
        factor_data = {
            'date': date,
            'time': now(),
            'explanation': explanation,
        }
        input_factor.update(**factor_data)
        output_factor.update(**factor_data)

        self.sync(instance, validated_data)

        return instance


class AdjustmentListRetrieveSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    sanad = SanadSerializer(read_only=True, many=False)
    created_by = UserSimpleSerializer(many=False, read_only=True)

    def get_items(self, obj):
        return FactorItemRetrieveSerializer(
            obj.factor.items.order_by('id').prefetch_related('ware').prefetch_related('warehouse'),
            many=True
        ).data

    class Meta:
        model = Adjustment
        fields = '__all__'


class AdjustmentCreateUpdateSerializer(serializers.ModelSerializer):
    items = serializers.ListField()

    class Meta:
        model = Adjustment
        exclude = ('financial_year', 'factor', 'code')

    def sync(self, instance: Adjustment, validated_data):
        user = get_current_user()
        financial_year = user.active_financial_year
        adjustment_type = instance.type

        is_defining = self.context.get('is_defining', False)

        # Sync factor
        factor = instance.factor

        if instance.is_defined or is_defining:
            DefiniteFactor.updateFactorInventory(factor, revert=True)

        factor_items_data = []
        for item in validated_data.get('items'):
            ware = Ware.objects.get(pk=item['ware'])
            fee = None
            if adjustment_type == Factor.INPUT_ADJUSTMENT:
                ware_last_factor_item = FactorItem.objects.inFinancialYear().filter(
                    ~Q(fee=0),
                    ware=ware,
                    factor__type__in=Factor.INPUT_GROUP,
                ).first()
                if ware_last_factor_item:
                    fee = ware_last_factor_item.fee
                else:
                    raise serializers.ValidationError("هیچ فاکتوری برای {} ثبت نشده است".format(ware.name))
            elif adjustment_type == Factor.OUTPUT_ADJUSTMENT:
                fee = 0

            factor_items_data.append({
                'financial_year': financial_year,
                'count': item['count'],
                'unit_count': item['unit_count'],
                'unit_id': item['unit'],
                'fee': fee,
                'ware': ware,
                'warehouse': Warehouse.objects.get(pk=item['warehouse'])

            })

        factor.verify_items(list(map(lambda o: {
            'count': o['count'],
            'fee': o['fee'],
            'ware': o['ware'].id,
            'warehouse': o['warehouse'].id,
        }, factor_items_data)))
        factor.items.all().delete()

        if financial_year.is_advari:
            factor.definition_date = instance.date.togregorian()
        factor.date = instance.date
        factor.explanation = instance.explanation
        factor.save()

        for item_data in factor_items_data:
            factor.items.create(**item_data)

        if instance.is_defined or is_defining:
            DefiniteFactor.updateFactorInventory(factor)

            # Sync sanad
            AdjustmentSanad(instance).update()

    def create(self, validated_data, **kwargs):
        financial_year = self.context['financial_year']
        adjustment_type = validated_data.get('type')
        date = validated_data['date']
        time = validated_data['time']
        explanation = validated_data.get('explanation', '')

        if financial_year.is_advari:
            definition_date = datetime.datetime.combine(date.togregorian(), time)
        else:
            definition_date = now()

        factor_data = {
            'financial_year': financial_year,
            'temporary_code': Factor.get_new_temporary_code(adjustment_type),
            'code': Factor.get_new_code(adjustment_type),
            'date': date,
            'time': time,
            'explanation': explanation,
            'is_defined': True,
            'definition_date': definition_date,
            'is_auto_created': True,
            'type': adjustment_type
        }
        factor = Factor.objects.create(**factor_data)
        factor.save()

        code = Adjustment.objects.filter(type=adjustment_type).aggregate(Max('code'))['code__max']
        if code:
            code += 1
        else:
            code = 1

        adjustment_data = {
            'type': adjustment_type,
            'code': code,
            'date': date,
            'time': time,
            'financial_year': financial_year,
            'factor': factor,
            'explanation': explanation
        }
        adjustment = Adjustment.objects.create(**adjustment_data)

        self.sync(adjustment, validated_data)

        return adjustment

    def update(self, instance: Adjustment, validated_data):
        date = validated_data['date']
        time = validated_data['time']
        explanation = validated_data.get('explanation', '')

        factor_data = {
            'date': date,
            'time': time,
            'explanation': explanation,
        }
        instance.factor.update(**factor_data)

        adjustment_data = {
            'date': date,
            'time': time,
            'explanation': explanation
        }
        instance.update(**adjustment_data)

        self.sync(instance, validated_data)

        return super().update(instance, validated_data)


class WarehouseHandlingItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseHandlingItem
        fields = '__all__'
        read_only_fields = ['id', 'financial_year']


class WarehouseHandlingItemListRetrieveSerializer(serializers.ModelSerializer):
    ware = WareListSerializer(many=False, read_only=True)
    unit = serializers.SerializerMethodField()

    def get_unit(self, obj: WarehouseHandlingItem):
        return obj.ware.main_unit.name

    class Meta:
        model = WarehouseHandlingItem
        fields = '__all__'
        read_only_fields = ['id', 'financial_year']


class WarehouseHandlingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseHandling
        fields = '__all__'
        read_only_fields = ['id', 'financial_year']


class WarehouseHandlingListRetrieveSerializer(serializers.ModelSerializer):
    items = WarehouseHandlingItemListRetrieveSerializer(many=True, read_only=True)
    warehouse = WarehouseSimpleSerializer(many=False, read_only=True)
    created_by = UserSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = WarehouseHandling
        fields = '__all__'
        read_only_fields = ['id', 'financial_year']


class FactorsAggregatedSanadCreateUpdateSerializer(serializers.ModelSerializer):
    factors = serializers.PrimaryKeyRelatedField(many=True, queryset=Factor.objects.all())

    class Meta:
        model = FactorsAggregatedSanad
        fields = '__all__'
        read_only_fields = ['id', 'financial_year']


class FactorsAggregatedSanadRetrieveSerializer(serializers.ModelSerializer):
    factors = FactorListRetrieveSerializer(many=True)
    sanad = SanadSerializer()

    class Meta:
        model = FactorsAggregatedSanad
        fields = '__all__'


class FactorsAggregatedSanadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorsAggregatedSanad
        fields = '__all__'
