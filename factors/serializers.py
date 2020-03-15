from rest_framework import serializers

from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer
from accounts.accounts.validators import AccountValidator
from factors.models import *
from sanads.sanads.serializers import SanadSerializer
from wares.serializers import WareListRetrieveSerializer, WarehouseSerializer
from django.utils.timezone import now


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    def validate(self, data):
        AccountValidator.tafsili(data)
        return data


class ExpenseListRetrieveSerializer(ExpenseSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
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
    account = AccountListRetrieveSerializer(read_only=True, many=False)
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
        read_only_fields = ['id', 'code', 'financial_year']
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
    sale_price = serializers.DecimalField(max_digits=24, decimal_places=0, allow_null=True, default=None)

    class Meta:
        model = FactorItem
        fields = '__all__'
        read_only_fields = ['id', 'financial_year']

    def validate(self, attrs):
        ware = attrs.get('ware')
        warehouse = attrs.get('warehouse')

        if not ware.isService and not warehouse:
            raise serializers.ValidationError("انبار اجباری می باشد")

        return super(FactorItemSerializer, self).validate(attrs)

    def update(self, instance, validated_data):
        self.updateWarePrice(validated_data)
        return super(FactorItemSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        self.updateWarePrice(validated_data)
        return super(FactorItemSerializer, self).create(validated_data)

    @staticmethod
    def updateWarePrice(validated_data):
        ware = validated_data.get('ware')
        sale_price = validated_data.pop('sale_price')
        if sale_price:
            ware.price = sale_price
            ware.save()


class FactorItemRetrieveSerializer(serializers.ModelSerializer):
    ware = WareListRetrieveSerializer(read_only=True, many=False)
    warehouse = WarehouseSerializer(read_only=True, many=False)

    class Meta:
        model = FactorItem
        fields = '__all__'


class TransactionSerializerForPayment(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class FactorPaymentWithTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializerForPayment(read_only=True, many=False)

    class Meta:
        model = FactorPayment
        fields = '__all__'


class FactorListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)
    expenses = FactorExpenseListRetrieveSerializer(read_only=True, many=True)
    items = FactorItemRetrieveSerializer(read_only=True, many=True)
    payments = FactorPaymentWithTransactionSerializer(read_only=True, many=True)
    sanad = SanadSerializer(read_only=True, many=False)

    class Meta:
        model = Factor
        fields = '__all__'


class FactorPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorPayment
        fields = '__all__'


class NotPaidFactorsCreateUpdateSerializer(FactorCreateUpdateSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)
    payments = FactorPaymentSerializer(read_only=True, many=True)
    sum = serializers.SerializerMethodField()

    def get_sum(self, obj):
        return obj.totalSum

    class Meta:
        model = Factor
        fields = '__all__'


class TransferListRetrieveSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        input_items = obj.input_factor.items.order_by('id') \
            .prefetch_related('warehouse')

        output_items = obj.output_factor.items.order_by('id') \
            .prefetch_related('warehouse')

        items = []
        for i in range(len(input_items)):
            input_item = input_items[i]
            output_item = output_items[i]

            ware = WareListRetrieveSerializer(input_item.ware).data
            count = input_item.count
            explanation = input_item.explanation
            output_warehouse = WarehouseSerializer(output_item.warehouse).data
            input_warehouse = WarehouseSerializer(input_item.warehouse).data

            items.append({
                'ware': ware,
                'count': count,
                'explanation': explanation,
                'output_warehouse': output_warehouse,
                'input_warehouse': input_warehouse,
            })

        return items

    class Meta:
        model = Transfer
        # fields = ('id', 'code', 'explanation', 'date', 'items')
        fields = '__all__'


class TransferCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        financial_year = validated_data['financial_year']
        date = validated_data['date']
        explanation = validated_data.get('explanation', '')
        factor_data = {
            'financial_year': financial_year,
            'date': date,
            'explanation': explanation,
            'is_definite': True,
            'definition_date': now(),
            'time': ''
        }
        input_factor = Factor.objects.create(**factor_data, type=Factor.INPUT_TRANSFER)
        input_factor.save()
        output_factor = Factor.objects.create(**factor_data, type=Factor.OUTPUT_TRANSFER)
        output_factor.save()

        for item in validated_data['items']:
            item_data = {
                'financial_year': financial_year,
                'explanation': explanation,
                'count': item['count'],
                'fee': 0,
                'ware': Ware.objects.get(pk=item['ware'])

            }
            input_factor.items.create(**item_data, warehouse=Warehouse.objects.get(pk=item['input_warehouse']))
            output_factor.items.create(**item_data, warehouse=Warehouse.objects.get(pk=item['output_warehouse']))

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
            'explanation': explanation,
            'code': code
        }

        transfer = Transfer.objects.create(**transfer_data)

        return transfer

    class Meta:
        model = Transfer
        fields = ('id', 'financial_year', 'explanation', 'date', 'items')
