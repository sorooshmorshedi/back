import django_filters
from django.db.models import F
from django_filters import rest_framework as filters, CharFilter
from django_jalali.db import models as jmodels

from cheques.models.ChequeModel import Cheque
from cheques.models.ChequebookModel import Chequebook
from contracting.models import Tender, Contract, Statement, Supplement
from factors.models import Factor, Adjustment
from factors.models.transfer_model import Transfer
from factors.models.warehouse_handling import WarehouseHandling
from factors.models.factor import FactorItem, FactorsAggregatedSanad
from helpers.filters import BASE_FIELD_FILTERS, filter_created_by_name
from sanads.models import Sanad
from transactions.models import Transaction
from wares.models import SalePrice, SalePriceChange, WareSalePriceChange


class TransactionFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'id': ['exact'],
            'contract_received': ['exact'],
            'contract_guarantee': ['exact'],
            'code': BASE_FIELD_FILTERS,
            'account': ['exact'],
            'account__name': ['exact', 'icontains'],
            'floatAccount': ['exact'],
            'date': BASE_FIELD_FILTERS,
            'explanation': ['icontains'],
            'type': ['exact'],
            'sanad__bed': BASE_FIELD_FILTERS,
            'imprestSettlement': ['isnull'],
            'imprestSettlement__is_settled': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ChequeFilter(filters.FilterSet):
    class Meta:
        model = Cheque
        fields = {
            'id': ['exact'],
            'serial': ['icontains'],
            'explanation': ['icontains'],
            'date': ['gte', 'lte'],
            'due': BASE_FIELD_FILTERS,
            'value': ['exact'],
            'status': BASE_FIELD_FILTERS,
            'bankName': ['icontains'],
            'type': ['exact'],
            'is_paid': ['exact'],
            'chequebook__id': ['exact'],
            'chequebook__explanation': ['icontains'],
            'chequebook__account__name': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ChequebookFilter(filters.FilterSet):
    class Meta:
        model = Chequebook
        fields = {
            'id': ['exact'],
            'account__name': ['icontains'],
            'serial': ['icontains'],
            'serial_from': ['icontains'],
            'serial_to': ['icontains'],
            'explanation': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class SanadFilter(filters.FilterSet):
    created_by__name = CharFilter(method=filter_created_by_name)
    created_by__name__icontains = CharFilter(method=filter_created_by_name)

    class Meta:
        model = Sanad
        fields = {
            'id': ['exact', 'in'],
            'local_id': ['exact', 'in'],
            'code': BASE_FIELD_FILTERS,
            'bed': BASE_FIELD_FILTERS,
            'bes': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
            'is_auto_created': ['exact'],
            'is_defined': ['exact'],
            'created_by__name': ['icontains']
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class FactorFilter(filters.FilterSet):
    isPaid = filters.BooleanFilter(method='filterIsPaid')

    class Meta:
        model = Factor
        fields = {
            'id': ['exact'],
            'temporary_code': ['icontains'],
            'code': ['icontains'],
            'isPaid': ['exact'],
            'date': ['gte', 'lte'],
            'time': ['gte', 'lte'],
            'account__name': ['icontains'],
            'explanation': ['icontains'],
            'sanad__bed': ['icontains'],
            'sanad': ['exact'],
            'type': ['exact', 'in'],
            'is_defined': ['exact'],
            'is_loaded': ['exact'],
            'path': ['in'],
            'visitor': ['in', 'exact'],
            'is_pre_factor': ['exact'],
            'has_auto_sanad': ['exact'],
            'aggregatedSanad': ['exact', 'isnull'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }

    def filterIsPaid(self, queryset, name, value):
        if value:
            return queryset.filter(sanad__bed=F('paidValue'))
        else:
            return queryset


class FactorsAggregatedSanadFilter(filters.FilterSet):
    class Meta:
        model = FactorsAggregatedSanad
        fields = {
            'id': ['exact'],
            'code': BASE_FIELD_FILTERS,
            'date': ['gte', 'lte'],
            'explanation': ['icontains'],
            'sanad': ['exact'],
            'type': ['exact', 'in'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class TransferFilter(filters.FilterSet):
    class Meta:
        model = Transfer
        fields = {
            'id': ['exact'],
            # 'code': ['gte', 'lte', 'exact'],
            'date': ['gte', 'lte'],
            'explanation': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class FactorItemFilter(filters.FilterSet):
    class Meta:
        model = FactorItem
        fields = {
            'ware': ['exact'],
            'warehouse': ['exact'],
            'warehouse__name': BASE_FIELD_FILTERS,
            'factor__type': ['exact', 'in'],
            'id': ['exact'],
            'factor__code': BASE_FIELD_FILTERS,
            'factor__is_defined': ['exact'],
            'factor__date': BASE_FIELD_FILTERS,
            'factor__account': ['exact'],
            'factor__account__name': BASE_FIELD_FILTERS,
            'factor__floatAccount': ['exact'],
            'factor__costCenter': ['exact'],
            'count': ['exact'],
            'fee': ['exact'],
            'factor__explanation': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class AdjustmentFilter(filters.FilterSet):
    class Meta:
        model = Adjustment
        fields = {
            'id': ['exact'],
            'type': ['exact'],
            'code': ['gte', 'lte', 'exact'],
            'date': ['gte', 'lte'],
            'explanation': ['icontains'],
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class WarehouseHandlingFilter(filters.FilterSet):
    class Meta:
        model = WarehouseHandling
        fields = {
            'id': BASE_FIELD_FILTERS,
            'code': BASE_FIELD_FILTERS,
            'start_date': BASE_FIELD_FILTERS,
            'counting_date': BASE_FIELD_FILTERS,
            'submit_date': BASE_FIELD_FILTERS,
            'warehouse__name': BASE_FIELD_FILTERS,
            'handler': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class SalePriceFilter(filters.FilterSet):
    class Meta:
        model = SalePrice
        fields = {
            'id': BASE_FIELD_FILTERS,
            'type': ('exact',),
            'type__name': BASE_FIELD_FILTERS,
            'ware': ('exact',),
            'ware__name': BASE_FIELD_FILTERS,
            'ware__code': BASE_FIELD_FILTERS,
            'mainUnit': ('exact',),
            'mainUnit__name': BASE_FIELD_FILTERS,
            'unit': ('exact',),
            'unit__name': BASE_FIELD_FILTERS,
            'conversion_factor': BASE_FIELD_FILTERS,
            'price': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class SalePriceChangeFilter(filters.FilterSet):
    class Meta:
        model = SalePriceChange
        fields = {
            'is_increase': ('exact',),
            'is_percent': ('exact',),
            'rate': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class WareSalePriceChangeFilter(filters.FilterSet):
    class Meta:
        model = WareSalePriceChange
        fields = {
            'salePriceChange': ('exact',),
            'salePrice__ware__name': BASE_FIELD_FILTERS,
            'salePrice__ware__code': BASE_FIELD_FILTERS,
            'salePrice__type__name': BASE_FIELD_FILTERS,
            'salePrice__mainUnit__name': BASE_FIELD_FILTERS,
            'salePrice__unit__name': BASE_FIELD_FILTERS,
            'salePrice__conversion_factor': BASE_FIELD_FILTERS,
            'salePrice__price': BASE_FIELD_FILTERS,
            'previous_price': BASE_FIELD_FILTERS,
            'new_price': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class TenderFilter(filters.FilterSet):
    class Meta:
        model = Tender
        fields = {
            'id': ('exact',),
            'code': BASE_FIELD_FILTERS,
            'title': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
            'province': BASE_FIELD_FILTERS,
            'city':BASE_FIELD_FILTERS,
            'classification': ('exact',),
            'bidder': BASE_FIELD_FILTERS,
            'bidder_address': BASE_FIELD_FILTERS,
            'bidder_postal_code': BASE_FIELD_FILTERS,
            'received_deadline': BASE_FIELD_FILTERS,
            'send_offer_deadline': BASE_FIELD_FILTERS,
            'opening_date':BASE_FIELD_FILTERS,
            'offer_expiration': BASE_FIELD_FILTERS,
            'transaction__code': BASE_FIELD_FILTERS,

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ContractFilter(filters.FilterSet):
    class Meta:
        model = Contract
        fields = {
            'id': ('exact',),
            'tender': ('exact',),
            'title': BASE_FIELD_FILTERS,
            'contractor': ('exact',),
            'code': BASE_FIELD_FILTERS,
            'amount': BASE_FIELD_FILTERS,
            'inception': BASE_FIELD_FILTERS,
            'registration': BASE_FIELD_FILTERS,
            'max_change_amount': BASE_FIELD_FILTERS,
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
            'doing_job_well': BASE_FIELD_FILTERS,
            'insurance_payment': BASE_FIELD_FILTERS,
            'other': BASE_FIELD_FILTERS,
            'received_transaction__code': BASE_FIELD_FILTERS,
            'guarantee_document_transaction__code': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class StatementFilter(filters.FilterSet):
    class Meta:
        model = Statement
        fields = {
            'id': ('exact',),
            'code': BASE_FIELD_FILTERS,
            'type': ('exact',),
            'contract': ('exact',),
            'value': BASE_FIELD_FILTERS,
            'previous_statement_value': BASE_FIELD_FILTERS,
            'serial': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
            'explanation':BASE_FIELD_FILTERS,
            'present_statement_value': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class SupplementFilter(filters.FilterSet):
    class Meta:
        model = Supplement
        fields = {
            'id': ('exact',),
            'contract': ('exact',),
            'new_contract_date': BASE_FIELD_FILTERS,
            'explanation': ['icontains'],
            'increase': ('exact',),
            'value': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
            'code': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


