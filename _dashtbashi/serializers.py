from typing import Any

from rest_framework import serializers

from _dashtbashi.models import Driver, Car, Driving, Association, Remittance, Lading, LadingBillSeries, \
    LadingBillNumber, OilCompanyLading, OilCompanyLadingItem, OtherDriverPayment
from accounts.accounts.serializers import AccountRetrieveSerializer
from helpers.serializers import validate_required_fields
from sanads.serializers import SanadSerializer
from transactions.models import Transaction
from transactions.serializers import TransactionListRetrieveSerializer
from users.serializers import CitySerializer, UserSimpleSerializer
from wares.serializers import WareRetrieveSerializer


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        read_only_fields = ('financial_year',)


class CarSerializer(serializers.ModelSerializer):
    car_number_str = serializers.SerializerMethodField()

    @staticmethod
    def get_car_number_str(obj: Car):
        return "{} - - {} - - {}".format(
            obj.car_number_str,
            [owner[1] for owner in Car.OWNERS if owner[0] == obj.owner][0],
            [contract_type[1] for contract_type in Car.CONTRACT_TYPES if contract_type[0] == obj.contract_type][0],
        )

    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ('financial_year',)


class AssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = '__all__'
        read_only_fields = ('financial_year',)


class DrivingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driving
        fields = '__all__'
        read_only_fields = ('financial_year',)


class DrivingListRetrieveSerializer(serializers.ModelSerializer):
    driver = DriverSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    title = serializers.SerializerMethodField()

    def get_title(self, obj: Driving):
        return obj.title

    class Meta:
        model = Driving
        fields = '__all__'
        read_only_fields = ('financial_year',)


class LadingBillNumberCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LadingBillNumber
        fields = '__all__'


class LadingBillSeriesSerializer(serializers.ModelSerializer):
    numbers = LadingBillNumberCreateUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = LadingBillSeries
        fields = '__all__'

    def create(self, validated_data: Any) -> Any:
        instance = super().create(validated_data)
        self.create_lading_bill_numbers(instance)
        return instance

    def update(self, instance: LadingBillSeries, validated_data: Any) -> Any:
        instance = super().update(instance, validated_data)
        instance.numbers.all().delete()
        self.create_lading_bill_numbers(instance)
        return instance

    @staticmethod
    def create_lading_bill_numbers(instance: LadingBillSeries):
        for i in range(instance.from_bill_number, instance.to_bill_number + 1):
            LadingBillNumber.objects.create(
                series=instance,
                number=i
            )


class LadingBillSeriesSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LadingBillSeries
        fields = '__all__'


class LadingBillNumberListSerializer(serializers.ModelSerializer):
    series = LadingBillSeriesSimpleSerializer(read_only=True)

    class Meta:
        model = LadingBillNumber
        fields = '__all__'


class LadingBillNumberRetrieveSerializer(serializers.ModelSerializer):
    series = LadingBillSeriesSerializer(read_only=True)

    class Meta:
        model = LadingBillNumber
        fields = '__all__'


class RemittanceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remittance
        fields = '__all__'
        read_only_fields = ('financial_year',)


class RemittanceListRetrieveSerializer(serializers.ModelSerializer):
    ware = WareRetrieveSerializer(read_only=True)
    origin = CitySerializer(read_only=True)
    destination = CitySerializer(read_only=True)
    contractor = AccountRetrieveSerializer(read_only=True)
    created_by = UserSimpleSerializer(many=False, read_only=True)

    title = serializers.SerializerMethodField()

    def get_title(self, obj: Remittance):
        return "{} - {}".format(obj.code, obj.contractor.name if obj.contractor else '')

    class Meta:
        model = Remittance
        fields = '__all__'
        read_only_fields = ('financial_year',)


class LadingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lading
        fields = '__all__'
        read_only_fields = ('financial_year',)

    def validate(self, attrs):
        remittance = attrs.get('remittance')
        if remittance and remittance.is_finished:
            raise serializers.ValidationError("بارگیری این حواله به پایان رسیده است")

        required_fields = []
        if 'l' in attrs.get('type'):
            required_fields += ['ware', 'contractor', 'lading_number', 'remittance_payment_method', 'driver_tip_payer',
                                'lading_date']

        if 'b' in attrs.get('type'):
            required_fields += ['billNumber', 'bill_price', 'receive_type', 'bill_date']

        validate_required_fields(attrs, required_fields)

        return super(LadingCreateUpdateSerializer, self).validate(attrs)


class LadingListSerializer(serializers.ModelSerializer):
    remittance = RemittanceListRetrieveSerializer(read_only=True)
    driving = DrivingListRetrieveSerializer(read_only=True)
    contractor = AccountRetrieveSerializer(read_only=True)
    ware = WareRetrieveSerializer(read_only=True)
    association = AssociationSerializer(read_only=True)
    billNumber = LadingBillNumberListSerializer(read_only=True)
    origin = CitySerializer(read_only=True)
    destination = CitySerializer(read_only=True)
    sanad = SanadSerializer(read_only=True)
    created_by = UserSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = Lading
        fields = '__all__'
        read_only_fields = ('financial_year',)


class LadingRetrieveSerializer(serializers.ModelSerializer):
    remittance = RemittanceListRetrieveSerializer(read_only=True)
    driving = DrivingListRetrieveSerializer(read_only=True)
    contractor = AccountRetrieveSerializer(read_only=True)
    ware = WareRetrieveSerializer(read_only=True)
    association = AssociationSerializer(read_only=True)
    billNumber = LadingBillNumberRetrieveSerializer(read_only=True)
    origin = CitySerializer(read_only=True)
    destination = CitySerializer(read_only=True)
    sanad = SanadSerializer(read_only=True)
    created_by = UserSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = Lading
        fields = '__all__'
        read_only_fields = ('financial_year',)


class OilCompanyLadingItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OilCompanyLadingItem
        fields = '__all__'
        read_only_fields = ('financial_year',)


class OilCompanyLadingItemListRetrieveSerializer(serializers.ModelSerializer):
    month = serializers.CharField(source='oilCompanyLading.month', read_only=True)
    list_date = serializers.CharField(source='oilCompanyLading.list_date', read_only=True)
    origin = CitySerializer(read_only=True)
    destination = CitySerializer(read_only=True)
    driving = DrivingListRetrieveSerializer(source='oilCompanyLading.driving', read_only=True)

    class Meta:
        model = OilCompanyLadingItem
        fields = '__all__'
        read_only_fields = ('financial_year',)


class OilCompanyLadingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OilCompanyLading
        fields = '__all__'
        read_only_fields = ('financial_year',)


class OilCompanyLadingListRetrieveSerializer(serializers.ModelSerializer):
    items = OilCompanyLadingItemListRetrieveSerializer(read_only=True, many=True)
    car = CarSerializer(read_only=True)
    created_by = UserSimpleSerializer(many=False, read_only=True)
    sanad = SanadSerializer(read_only=True)
    driving = DrivingListRetrieveSerializer()

    class Meta:
        model = OilCompanyLading
        fields = '__all__'
        read_only_fields = ('financial_year',)


class OtherDriverPaymentCreateUpdateSerializer(serializers.ModelSerializer):
    ladings = serializers.PrimaryKeyRelatedField(many=True, queryset=Lading.objects.all())
    imprests = serializers.PrimaryKeyRelatedField(many=True, queryset=Transaction.objects.all())

    class Meta:
        model = OtherDriverPayment
        fields = '__all__'
        read_only_fields = ('code', 'financial_year', 'payment')


class OtherDriverPaymentListRetrieveSerializer(serializers.ModelSerializer):
    driving = DrivingListRetrieveSerializer()
    ladings = LadingListSerializer(many=True)
    imprests = TransactionListRetrieveSerializer(many=True)
    payment = TransactionListRetrieveSerializer(many=False)
    created_by = UserSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = OtherDriverPayment
        fields = '__all__'
