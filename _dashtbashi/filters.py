import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from _dashtbashi.models import LadingBillSeries, Remittance, Lading, OilCompanyLading, LadingBillNumber, \
    OilCompanyLadingItem, OtherDriverPayment
from helpers.filters import BASE_FIELD_FILTERS


class LadingFilter(filters.FilterSet):
    class Meta:
        model = Lading
        fields = {
            'driving': ['exact'],
            'driving__driver__name': BASE_FIELD_FILTERS,
            'driving__car__owner': BASE_FIELD_FILTERS,

            'remittance': ['exact'],
            'is_paid': ['exact'],
            'id': BASE_FIELD_FILTERS,
            'remittance__code': BASE_FIELD_FILTERS,

            'contractor__name': ['exact', 'icontains'],
            'ware__name': BASE_FIELD_FILTERS,

            'billNumber__number': BASE_FIELD_FILTERS,
            'billNumber__series__serial': BASE_FIELD_FILTERS,

            'bill_price': BASE_FIELD_FILTERS,
            'cargo_tip_price': BASE_FIELD_FILTERS,
            'driver_tip_price': BASE_FIELD_FILTERS,
            'lading_bill_difference': BASE_FIELD_FILTERS,
            'lading_number': BASE_FIELD_FILTERS,
            'lading_date': BASE_FIELD_FILTERS,
            'lading_total_value': BASE_FIELD_FILTERS,
            'lading_bill_total_value': BASE_FIELD_FILTERS,

            'association__name': BASE_FIELD_FILTERS,
            'association_price': BASE_FIELD_FILTERS,

            'receive_type': BASE_FIELD_FILTERS,

            'origin__name': ['exact', 'icontains'],
            'destination__name': ['exact', 'icontains'],

            'origin_amount': BASE_FIELD_FILTERS,
            'destination_amount': BASE_FIELD_FILTERS,

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class LadingBillSeriesFilter(filters.FilterSet):
    class Meta:
        model = LadingBillSeries
        fields = {
            'id': BASE_FIELD_FILTERS,
            'serial': BASE_FIELD_FILTERS,
            'from_bill_number': BASE_FIELD_FILTERS,
            'to_bill_number': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class LadingBillNumberFilter(filters.FilterSet):
    class Meta:
        model = LadingBillNumber
        fields = {
            'series__serial': BASE_FIELD_FILTERS,
            'number': BASE_FIELD_FILTERS,
            'is_revoked': ['exact'],
            'revoked_at': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class RemittanceFilter(filters.FilterSet):
    class Meta:
        model = Remittance
        fields = {
            'id': BASE_FIELD_FILTERS,
            'code': BASE_FIELD_FILTERS,
            'issue_date': BASE_FIELD_FILTERS,
            'amount': BASE_FIELD_FILTERS,
            'origin__name': ['exact', 'icontains'],
            'destination__name': ['exact', 'icontains'],
            'contractor__name': ['exact', 'icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class OilCompanyLadingFilter(filters.FilterSet):
    class Meta:
        model = OilCompanyLading
        fields = {
            'id': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
            'list_date': BASE_FIELD_FILTERS,
            'export_date': BASE_FIELD_FILTERS,
            'gross_price': BASE_FIELD_FILTERS,
            'insurance_price': BASE_FIELD_FILTERS,
            'complication_price': BASE_FIELD_FILTERS,
            'total_value': BASE_FIELD_FILTERS,
            'company_commission': BASE_FIELD_FILTERS,
            'car_income': BASE_FIELD_FILTERS,
            'weight': BASE_FIELD_FILTERS,
            'month': BASE_FIELD_FILTERS,

            'driving__car': ['exact'],
            'driving__driver': ['exact'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class OilCompanyLadingItemFilter(filters.FilterSet):
    class Meta:
        model = OilCompanyLadingItem
        fields = {
            'id': BASE_FIELD_FILTERS,

            'gross_price': BASE_FIELD_FILTERS,
            'insurance_price': BASE_FIELD_FILTERS,

            'tax_value': BASE_FIELD_FILTERS,
            'tax_percent': BASE_FIELD_FILTERS,

            'complication_value': BASE_FIELD_FILTERS,
            'complication_percent': BASE_FIELD_FILTERS,

            'origin__name': BASE_FIELD_FILTERS,
            'destination__name': BASE_FIELD_FILTERS,
            'weight': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,

            'company_commission_percent': BASE_FIELD_FILTERS,

            'company_commission': BASE_FIELD_FILTERS,
            'car_income': BASE_FIELD_FILTERS,
            'complication_price': BASE_FIELD_FILTERS,
            'total_value': BASE_FIELD_FILTERS,

            'oilCompanyLading__month': BASE_FIELD_FILTERS,
            'oilCompanyLading__driving__car': ['exact'],
            'oilCompanyLading__driving__driver': ['exact'],

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class OtherDriverPaymentFilter(filters.FilterSet):
    class Meta:
        model = OtherDriverPayment
        fields = {
            'id': BASE_FIELD_FILTERS,
            'code': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
            'driving__driver__name': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }
