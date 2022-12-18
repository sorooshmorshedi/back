import django_filters
from django.db.models import Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from helpers.filters import BASE_FIELD_FILTERS
from payroll.models import Workshop, Personnel, PersonnelFamily, WorkshopPersonnel, ContractRow, Contract, \
    LeaveOrAbsence, Mission, HRLetter, WorkshopTaxRow, WorkshopTax, ListOfPay, ListOfPayItem, Loan, OptionalDeduction, \
    LoanItem, Adjustment


class WorkshopFilter(filters.FilterSet):
    class Meta:
        model = Workshop
        fields = {
            'id': ('exact',),
            'company': ('exact',),
            'code': BASE_FIELD_FILTERS,
            'name': BASE_FIELD_FILTERS,
            'employer_name': BASE_FIELD_FILTERS,
            'address': ['icontains'],
            'employer_insurance_contribution': ('exact',),
            'postal_code': BASE_FIELD_FILTERS,
            'branch_code': BASE_FIELD_FILTERS,
            'branch_name': BASE_FIELD_FILTERS,
            'is_active': BASE_FIELD_FILTERS,
            'is_verified': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class PersonnelFilter(filters.FilterSet):
    class Meta:
        model = Personnel
        fields = {
            'id': ('exact',),
            'company': ('exact',),
            'name': BASE_FIELD_FILTERS,
            'last_name': BASE_FIELD_FILTERS,
            'father_name': BASE_FIELD_FILTERS,
            'country': BASE_FIELD_FILTERS,
            'nationality': ('exact',),
            'personnel_code': ('exact',),
            'gender': ('exact',),
            'military_service': ('exact',),
            'national_code': ('exact',),
            'identity_code': ('exact',),
            'date_of_birth': BASE_FIELD_FILTERS,
            'date_of_exportation': BASE_FIELD_FILTERS,
            'location_of_birth': ('exact',),
            'location_of_exportation': ('exact',),
            'sector_of_exportation': ('exact',),
            'marital_status': ('exact',),
            'number_of_childes': ('exact',),
            'city_phone_code': ('exact',),
            'phone_number': ('exact',),
            'mobile_number_1': ('exact',),
            'mobile_number_2': ('exact',),
            'address': BASE_FIELD_FILTERS,
            'postal_code': BASE_FIELD_FILTERS,
            'insurance': BASE_FIELD_FILTERS,
            'insurance_code': BASE_FIELD_FILTERS,
            'degree_education': ('exact',),
            'field_of_study': BASE_FIELD_FILTERS,
            'university_type': ('exact',),
            'university_name': ('exact',),
            'account_bank_name': BASE_FIELD_FILTERS,
            'account_bank_number': ('exact',),
            'sheba_number': ('exact',),
            'is_personnel_active': ('exact',),
            'is_personnel_verified': ('exact',),

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class PersonnelFamilyFilter(filters.FilterSet):
    class Meta:
        model = PersonnelFamily
        fields = {
            'id': ('exact',),
            'personnel': ('exact',),
            'name': BASE_FIELD_FILTERS,
            'last_name': BASE_FIELD_FILTERS,
            'national_code': ('exact',),
            'date_of_birth': BASE_FIELD_FILTERS,
            'relative': ('exact',),
            'marital_status': ('exact',),
            'military_service': ('exact',),
            'study_status': ('exact',),
            'physical_condition': ('exact',),
            'is_active': ('exact',),
            'is_verified': ('exact',),
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class WorkshopPersonnelFilter(filters.FilterSet):
    class Meta:
        model = WorkshopPersonnel
        fields = {
            'id': ('exact',),
            'personnel': ('exact',),
            'workshop': ('exact',),
            'work_title': ['icontains'],
            'previous_insurance_history_out_workshop': ('exact',),
            'previous_insurance_history_in_workshop': ('exact',),
            'current_insurance_history_in_workshop': ('exact',),
            'insurance_history_totality': ('exact',),
            'job_position': BASE_FIELD_FILTERS,
            'job_group': BASE_FIELD_FILTERS,
            'job_location': BASE_FIELD_FILTERS,
            'job_location_status': BASE_FIELD_FILTERS,
            'employment_type': ('exact',),
            'contract_type': ('exact',),
            'employee_status': ('exact',),
            'is_verified': BASE_FIELD_FILTERS,

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
            'workshop_personnel': ('exact',),
            'code': BASE_FIELD_FILTERS,
            'insurance': BASE_FIELD_FILTERS,
            'insurance_add_date': BASE_FIELD_FILTERS,
            'contract_from_date': BASE_FIELD_FILTERS,
            'contract_to_date': BASE_FIELD_FILTERS,
            'quit_job_date': BASE_FIELD_FILTERS,
            'is_verified': ('exact',),

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ContractRowFilter(filters.FilterSet):
    class Meta:
        model = ContractRow
        fields = {
            'id': ('exact',),
            'workshop': ('exact',),
            'contract_row': ('exact',),
            'contract_number': ('exact',),
            'registration_date': BASE_FIELD_FILTERS,
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
            'assignor_name': BASE_FIELD_FILTERS,
            'assignor_national_code': ('exact',),
            'assignor_workshop_code': ('exact',),
            'contract_initial_amount': BASE_FIELD_FILTERS,
            'branch': BASE_FIELD_FILTERS,
            'status': ('exact',),
            'is_verified': ('exact',),
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
            'id': ('exact',),
            'contract_row': ('exact',),
            'date': BASE_FIELD_FILTERS,
            'change_date': BASE_FIELD_FILTERS,
            'amount': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


def absence_type_filter(queryset, name, value):
    types = {
        'استحقاقی': 'e',
        'استعلاجی': 'i',
        'بدون_حقوق': 'w',
        'غیبت': 'a',
        'ماده_73': 'm',
        'زایمان': 'c'
    }
    query = queryset.filter(pk=None)
    for type in types:
        if value in type:
            query = queryset.filter(leave_type=types[type])
    return query


class LeaveOrAbsenceFilter(filters.FilterSet):
    leave_type_display = filters.CharFilter(method=absence_type_filter)

    class Meta:
        model = LeaveOrAbsence
        fields = {
            'id': BASE_FIELD_FILTERS,
            'workshop_personnel': ('exact',),
            'leave_type': ('exact',),
            'entitlement_leave_type': ('exact',),
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
            'from_hour': BASE_FIELD_FILTERS,
            'to_hour': BASE_FIELD_FILTERS,
            'explanation': ('exact',),
            'is_verified': BASE_FIELD_FILTERS,

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


def mission_type_filter(queryset, name, value):
    print(value)
    types = {
        'ساعتی': 'h',
        'روزانه': 'd',
    }
    query = queryset.filter(pk=None)
    for type in types:
        if value in type:
            query = queryset.filter(mission_type=types[type])
    return query



class MissionFilter(filters.FilterSet):
    mission_type_display = filters.CharFilter(method=mission_type_filter)

    class Meta:
        model = Mission
        fields = {
            'id': BASE_FIELD_FILTERS,
            'workshop_personnel': ('exact',),
            'mission_type': ('exact',),
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
            'explanation': ('exact',),
            'is_verified': BASE_FIELD_FILTERS,

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class HRLetterFilter(filters.FilterSet):
    class Meta:
        model = HRLetter
        fields = {
            'id': BASE_FIELD_FILTERS,
            'contract': ('exact',),
            'name': BASE_FIELD_FILTERS,
            'is_template': BASE_FIELD_FILTERS,
        }


class ListOfPayFilter(filters.FilterSet):
    class Meta:
        model = ListOfPay
        fields = {
            'id': BASE_FIELD_FILTERS,
            'name': BASE_FIELD_FILTERS,
            'workshop': ('exact',),
            'year': BASE_FIELD_FILTERS,
            'month': BASE_FIELD_FILTERS,
            'ultimate': BASE_FIELD_FILTERS,
            'use_in_calculate': BASE_FIELD_FILTERS,
            'pay_done': BASE_FIELD_FILTERS,
            'pay_form_create_date': BASE_FIELD_FILTERS,
            'bank_pay_date': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ListOfPayItemFilter(filters.FilterSet):
    class Meta:
        model = ListOfPayItem
        fields = {
            'id': BASE_FIELD_FILTERS,
            'list_of_pay': ('exact',),
            'workshop_personnel': ('exact',),
            'contract': ('exact',),
        }


class TaxRowFilter(filters.FilterSet):
    class Meta:
        model = WorkshopTaxRow
        fields = {
            'id': BASE_FIELD_FILTERS,
        }


class TaxMoafFilter(filters.FilterSet):
    class Meta:
        model = WorkshopTax
        fields = {
            'id': BASE_FIELD_FILTERS,
            'name': BASE_FIELD_FILTERS,
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class LoanFilter(filters.FilterSet):
    class Meta:
        model = Loan
        fields = {
            'id': BASE_FIELD_FILTERS,
            'workshop_personnel': ('exact',),
            'amount': BASE_FIELD_FILTERS,
            'pay_done': BASE_FIELD_FILTERS,
            'episode': ('exact',),
            'loan_type': ('exact',),
            'pay_date': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class LoanItemFilter(filters.FilterSet):
    class Meta:
        model = LoanItem
        fields = {
            'id': BASE_FIELD_FILTERS,
            'loan': ('exact',),
            'amount': BASE_FIELD_FILTERS,
            'payed_amount': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class DeductionFilter(filters.FilterSet):
    class Meta:
        model = OptionalDeduction
        fields = {
            'id': BASE_FIELD_FILTERS,
            'workshop_personnel': ('exact',),
            'amount': BASE_FIELD_FILTERS,
            'pay_done': BASE_FIELD_FILTERS,
            'episode': ('exact',),
            'start_date': BASE_FIELD_FILTERS,
            'name': BASE_FIELD_FILTERS,
            'template_name': BASE_FIELD_FILTERS,
            'is_template': ('exact',),
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class TaxFilter(filters.FilterSet):
    class Meta:
        model = ListOfPayItem
        fields = {
            'id': BASE_FIELD_FILTERS,
        }


class WorkshopTaxFilter(filters.FilterSet):
    class Meta:
        model = ListOfPay
        fields = {
            'id': BASE_FIELD_FILTERS,
        }
