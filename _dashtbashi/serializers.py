from typing import Any

from rest_framework import serializers

from _dashtbashi.models import Driver, Car, Driving, Association, Remittance, Lading, LadingBillSeries, \
    LadingBillNumber, OilCompanyLading, OilCompanyLadingItem, OtherDriverPayment
from accounts.accounts.serializers import AccountListRetrieveSerializer
from imprests.serializers import ImprestListRetrieveSerializer
from transactions.models import Transaction
from transactions.serializers import TransactionListRetrieveSerializer
from users.serializers import CitySerializer
from wares.serializers import WareListRetrieveSerializer


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        read_only_fields = ('financial_year',)


class CarSerializer(serializers.ModelSerializer):
    car_number_str = serializers.SerializerMethodField()

    def get_car_number_str(self, obj: Car):
        return obj.car_number_str

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
        return "{} : {}".format(obj.driver.name, obj.car.car_number_str)

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


class LadingBillNumberListRetrieveSerializer(serializers.ModelSerializer):
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
    ware = WareListRetrieveSerializer(read_only=True)
    origin = CitySerializer(read_only=True)
    destination = CitySerializer(read_only=True)
    contractor = AccountListRetrieveSerializer(read_only=True)

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
        return attrs


class LadingListRetrieveSerializer(serializers.ModelSerializer):
    remittance = RemittanceListRetrieveSerializer(read_only=True)
    driving = DrivingListRetrieveSerializer(read_only=True)
    contractor = AccountListRetrieveSerializer(read_only=True)
    ware = WareListRetrieveSerializer(read_only=True)
    association = AssociationSerializer(read_only=True)
    billNumber = LadingBillNumberListRetrieveSerializer(read_only=True)

    class Meta:
        model = Lading
        fields = '__all__'
        read_only_fields = ('financial_year',)


class OilCompanyLadingItemSerializer(serializers.ModelSerializer):
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
    items = OilCompanyLadingItemSerializer(read_only=True, many=True)
    car = CarSerializer(read_only=True)

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
    ladings = LadingListRetrieveSerializer(many=True)
    imprests = ImprestListRetrieveSerializer(many=True)
    payment = TransactionListRetrieveSerializer(many=False)

    class Meta:
        model = OtherDriverPayment
        fields = '__all__'
