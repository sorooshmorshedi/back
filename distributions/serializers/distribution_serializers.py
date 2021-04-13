from rest_framework import serializers
from distributions.models.distribution_model import Distribution
from distributions.serializers.car_serializers import CarListRetrieveSerializer
from factors.models import Factor, FactorItem
from factors.serializers import FactorListRetrieveSerializer
from helpers.functions import add_separator
from users.serializers import UserSimpleSerializer


class DistributionRetrieveSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer()
    factors = FactorListRetrieveSerializer(many=True)
    car = CarListRetrieveSerializer()

    class Meta:
        model = Distribution
        fields = '__all__'


class DistributionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = '__all__'


class DistributionCreateUpdateSerializer(serializers.ModelSerializer):
    factors = serializers.PrimaryKeyRelatedField(many=True, queryset=Factor.objects.all())

    class Meta:
        model = Distribution
        exclude = ('financial_year', 'code')


class DistributionRemittanceSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer()
    car = CarListRetrieveSerializer()
    wares = serializers.SerializerMethodField()

    class Meta:
        model = Distribution
        fields = '__all__'

    def get_wares(self, obj: Distribution):
        rows = []
        factor_items = FactorItem.objects.filter(factor__distribution=obj).all()
        for factor_item in factor_items:
            ware = factor_item.ware

            row = [row for row in rows if row['id'] == ware.id]
            if len(row):
                row = row[0]
            else:
                row = {
                    'id': ware.id,
                    'name': ware.name,
                    'code': ware.code,
                    'salePrices': ware.salePrices.order_by('id'),
                    'count': 0,
                    'string_count': '',
                }
                rows.append(row)

            row['count'] += factor_item.count

        for row in rows:
            salePrices = row.pop('salePrices')
            count = row['count']
            main_unit = salePrices[0].unit
            string_count = "{} {}".format(add_separator(count), main_unit.name)

            if salePrices.count() > 1:
                salePrice = salePrices[1]
                unit_count = count // salePrice.conversion_factor
                remain_count = count % salePrice.conversion_factor

                if unit_count > 0:
                    string_count += " - {} {}".format(add_separator(unit_count), salePrice.unit.name)
                    if remain_count > 0:
                        string_count += " و {} {}".format(add_separator(remain_count), main_unit.name)

            row['string_count'] = string_count

        return rows
